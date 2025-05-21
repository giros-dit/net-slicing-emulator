// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * net/sched/sch_aqm_hctns.c AQM scheme for HCTNS.
 *
 * Authors:	Aitor Encinas Alonso, <aitor.encinas.alonso@alumnos.upm.es>
*/

#include <linux/module.h>
#include <linux/skbuff.h>
#include <linux/ip.h>
#include <linux/ipv6.h>
#include <linux/netdevice.h>
#include <linux/list.h>
#include <net/pkt_sched.h>
#include <net/inet_ecn.h>
#include <net/sch_generic.h>
#include <linux/tc_aqm_hctns.h>
#include <linux/tracepoint.h>
#include <linux/netlink.h>
#include <linux/slab.h>

struct aqm_hctns_sched_data {
	u32 ecn_count; // Number of packets with ECN flag
	struct list_head ecn_list; // Internal List to store ecn_skb_nodes. A list_head stores pointers to the next and previous elements in the list, and the elements can not be skb because they'll corrupt the qdisc.
	spinlock_t lock; // Spinlock to protect the list from concurrent access
};

struct ecn_skb_node {
	struct sk_buff *skb; // Pointer to the packet (what we store) with ECN flag
	struct list_head list; // Wrap the pointer of the skb into a list
};


#define SCH_AQM_HCTNS(sch) ((struct aqm_hctns_sched_data *)qdisc_priv(sch))

static struct kmem_cache *ecn_node_cache;

static inline int qdisc_enqueue_tail_aqm_hctns(struct sk_buff *skb, struct Qdisc *sch) {
	struct sk_buff *last = sch->q.tail;
	
	if (last) {
		skb->next = NULL;
		last->next = skb;
		skb->prev = last;
		sch->q.tail = skb;
	} else {
		sch->q.tail = skb;
		sch->q.head = skb;
	}

	sch->q.qlen++;
	qdisc_qstats_backlog_inc(sch, skb); // Increase the backlog
	return NET_XMIT_SUCCESS;
}

static inline struct sk_buff *qdisc_dequeue_head_aqm_hctns(struct Qdisc *sch) {
	struct sk_buff *skb = sch->q.head;

	if (likely(skb != NULL)) {
		sch->q.head = skb->next;
		sch->q.qlen--;
		if (sch->q.head == NULL) 
			sch->q.tail = NULL;
		skb->next->prev = NULL;	
		skb->next = NULL;
	}

	if (likely(skb != NULL)) {
		qdisc_qstats_backlog_dec(sch, skb); // Decrease the backlog
		qdisc_bstats_update(sch, skb); // Update the backlog of the parent qdiscs
	}

	return skb;
}

/*
Extract the ECN of the packet:
First, it looks if the Ethernet EtherType value is IP or IPv6.
Only if the packet is IP or IPv6, we extract the TOS value and see the two last bits (ECN value).
If ECN packet value == 11, the function returns true. Otherwise, returns false.
*/
static bool skb_has_ecn_ce(struct sk_buff *skb) {
	if (skb->protocol == htons(ETH_P_IP)) {
        struct iphdr *iph = ip_hdr(skb);
        return iph && (iph->tos & INET_ECN_MASK) == INET_ECN_CE;
    } else if (skb->protocol == htons(ETH_P_IPV6)) {
        struct ipv6hdr *ip6h = ipv6_hdr(skb);
        return ip6h && (ipv6_get_dsfield(ip6h) & INET_ECN_MASK) == INET_ECN_CE;
    }
    return false;
}

/*Dequeue and drop the ECN victim packet from the qdisc queue*/
static bool aqm_hctns_dequeue_for_drop(struct Qdisc *sch, struct sk_buff *ecn_victim, struct sk_buff **to_free) {
	
	trace_printk("ECN Victim: %p, Previous packet in the qdisc: %p, Next packet in the qdisc: %p\n",
	ecn_victim, ecn_victim->prev, ecn_victim->next);

	if (ecn_victim->prev) {
		// If the victim is neither the first packet in the queue nor the last one
		if (ecn_victim->next) {
			ecn_victim->prev->next = ecn_victim->next;
			ecn_victim->next->prev = ecn_victim->prev;
		// If the victim is the last packet in the queue (i.e., the tail)
		} else {
			ecn_victim->prev->next = NULL;
			sch->q.tail = ecn_victim->prev;
		}
	} else {
		// if the victim is the first packet in the queue (i.e., the head)
		if (ecn_victim->next) {
			ecn_victim->next->prev = NULL;
			sch->q.head = ecn_victim->next;
		// If the victim is the only packet in the queue
		} else {
			sch->q.head = NULL;
			sch->q.tail = NULL;
		}
	}
	
	ecn_victim->next = NULL;
	ecn_victim->prev = NULL;
	sch->q.qlen--;
	qdisc_qstats_backlog_dec(sch, ecn_victim); // Decrease the backlog
	qdisc_tree_reduce_backlog(sch, 1, ecn_victim->len); // Decrease the backlog of the parent qdiscs
	qdisc_drop(ecn_victim, sch, to_free); // Drop the packet with ECN flag
	return true;
}

/*Enqueue or discard packets when arrive to the queue*/
static int aqm_hctns_enqueue(struct sk_buff *skb, struct Qdisc *sch,
			 struct sk_buff **to_free)
{
	struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
	bool has_ecn = skb_has_ecn_ce(skb);
	
	spin_lock_bh(&q->lock);
	unsigned int limit = READ_ONCE(sch->limit);
	unsigned int qlen = sch->q.qlen;


	if (unlikely(limit == 0)) {
		spin_unlock_bh(&q->lock); 
		return qdisc_drop(skb, sch, to_free);
	}

	if (likely(qlen < limit)){
		if (has_ecn) {
			//Store the packet with ECN flag in the internal queue
			struct ecn_skb_node *node = kmem_cache_alloc(ecn_node_cache, GFP_ATOMIC); // Allocate dynamic cache memory for the node
			if (node) {
				node->skb = skb;
				list_add_tail(&node->list, &q->ecn_list);
				q->ecn_count++;
				trace_printk("ecn_count: %d\n", q->ecn_count);
			}
		}

		int ret = qdisc_enqueue_tail_aqm_hctns(skb, sch);
		trace_printk("SKB: %p, prev: %p, next: %p\n, beginning: %p, next %p, last:%p, prev:%p", skb, skb->prev, skb->next, sch->q.head, sch->q.head->next, sch->q.tail, sch->q.tail->prev); 
		trace_printk("Queue length: %u\n", sch->q.qlen);
		spin_unlock_bh(&q->lock); // Unlock the list
		return ret;
	}
	

	// If the queue is full and the packet has ECN flag, we drop it
	if (qlen >= limit && has_ecn){
		spin_unlock_bh(&q->lock); // Unlock the list
		return qdisc_drop(skb, sch, to_free);
	}

	/*
	* Else, we drop an ECN packet and enqueue the new packet
	* list_entry allows to get the struct from the list_head pointer, the type of the struct and the name of the list_header within the struct
	*/
	if (q->ecn_count > 0) {
		struct ecn_skb_node *node = list_entry(q->ecn_list.prev, struct ecn_skb_node, list); // Get the last node in the list
		struct sk_buff *ecn_victim = node->skb; // Get the skb from the node
		trace_printk("ECN Victim: %p, Previous packet in the qdisc: %p, Next packet in the qdisc: %p\n",ecn_victim, ecn_victim->prev, ecn_victim->next);
		if (ecn_victim) {
			list_del(&node->list); // Remove the node from the list
			q->ecn_count--;
			bool in_queue = aqm_hctns_dequeue_for_drop(sch, ecn_victim, to_free); // Dequeue the ECN packet
			kmem_cache_free(ecn_node_cache, node); // Free the node
			trace_printk("Delete ECN packet to enqueue non-ECN packet; qlen: %u, ecn_count: %u, packet: %p\n", sch->q.qlen, q->ecn_count, ecn_victim);
			int ret = qdisc_enqueue_tail_aqm_hctns(skb, sch); // Enqueue the new packet
			trace_printk("Queue length: %u\n", sch->q.qlen);
			spin_unlock_bh(&q->lock); // Unlock the list
			return ret;	
		}
		trace_printk("ecn_victim not found\n");
		spin_unlock_bh(&q->lock); // Unlock the list
		return qdisc_drop(skb, sch, to_free); // Drop the new packet
	}

	spin_unlock_bh(&q->lock); // Unlock the list
	/* If the queue is full and there are no packets with ECN flag, drop the new packet */
	return qdisc_drop(skb, sch, to_free); // Drop the new packet
}

static struct sk_buff *aqm_hctns_dequeue(struct Qdisc *sch) {
	struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
	spin_lock_bh(&q->lock);
	struct sk_buff *skb = qdisc_dequeue_head_aqm_hctns(sch);

	if (skb && skb_has_ecn_ce(skb) && q->ecn_count > 0) {
		
		struct ecn_skb_node *node = list_entry(q->ecn_list.next, struct ecn_skb_node, list);
		if (node->skb == skb) {
			list_del(&node->list); // Remove the node from the list
			q->ecn_count--;
			kmem_cache_free(ecn_node_cache, node); // Free the node
			trace_printk("ecn_count: %d\n", q->ecn_count);
		} else {
			trace_printk("ecn_victim not found dequeueing: %p vs %p\n", node->skb, skb);
		}	
	} 

	trace_printk("Queue length: %u, packet dequeued: %p\n", sch->q.qlen, skb);
	spin_unlock_bh(&q->lock);
	return skb;
}

static void aqm_hctns_reset(struct Qdisc *sch) {
    struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
	struct ecn_skb_node *node, *tmp;

	spin_lock_bh(&q->lock);
	list_for_each_entry_safe(node, tmp, &q->ecn_list, list) {
		list_del(&node->list);
		kmem_cache_free(ecn_node_cache, node);
	}

	spin_unlock_bh(&q->lock);
	// Reset the qdisc queue
	q->ecn_count = 0;
	qdisc_reset_queue(sch);
}

static int aqm_hctns_init(struct Qdisc *sch, struct nlattr *opt, struct netlink_ext_ack *extack) {

	struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
	INIT_LIST_HEAD(&q->ecn_list);
	spin_lock_init(&q->lock); // Initialize the spinlock
	q->ecn_count = 0;

    if (opt) {
        struct tc_aqm_hctns_qopt *ctl = nla_data(opt);
		if (nla_len(opt) < sizeof(*ctl))
			return -EINVAL;
        WRITE_ONCE(sch->limit, ctl->limit);
    } else {
		u32 limit = qdisc_dev(sch)->tx_queue_len;
		WRITE_ONCE(sch->limit, limit);
	}

    return 0;
}

static int aqm_hctns_dump(struct Qdisc *sch, struct sk_buff *skb) {
    struct tc_aqm_hctns_qopt opt = { .limit = READ_ONCE(sch->limit) };

    return nla_put(skb, TCA_OPTIONS, sizeof(opt), &opt);
}


static void aqm_hctns_destroy(struct Qdisc *sch)
{
    struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
	struct ecn_skb_node *node, *tmp;

	spin_lock_bh(&q->lock);
	list_for_each_entry_safe(node, tmp, &q->ecn_list, list) {
		list_del(&node->list);
		kmem_cache_free(ecn_node_cache, node);
	}
	spin_unlock_bh(&q->lock);

	q->ecn_count = 0;
	qdisc_reset_queue(sch);
}

struct Qdisc_ops aqm_hctns_qdisc_ops __read_mostly = {
	.id		    =	"aqm_hctns",
	.priv_size	=	sizeof(struct aqm_hctns_sched_data),
	.enqueue	=	aqm_hctns_enqueue,
	.dequeue	=	aqm_hctns_dequeue,
	.peek		=	qdisc_peek_head,
	.init		=	aqm_hctns_init,
	.destroy	=	aqm_hctns_destroy,
	.reset		=	aqm_hctns_reset,
	.change		=	aqm_hctns_init,
	.dump		=	aqm_hctns_dump,
	.owner		=	THIS_MODULE,
};
MODULE_ALIAS("sch_aqm_hctns");

static int __init aqm_hctns_module_init(void)
{
	ecn_node_cache = kmem_cache_create("ecn_node_cache", sizeof(struct ecn_skb_node), 0, 0, NULL);
	
	if (!ecn_node_cache)
		return -ENOMEM;

	if (register_qdisc(&aqm_hctns_qdisc_ops)) {
		kmem_cache_destroy(ecn_node_cache);
		return -EINVAL;
	}
	trace_printk("ecn_node_cache created\n");
	return 0;
}

static void __exit aqm_hctns_module_exit(void)
{
	unregister_qdisc(&aqm_hctns_qdisc_ops);
	kmem_cache_destroy(ecn_node_cache);
}

module_init(aqm_hctns_module_init)
module_exit(aqm_hctns_module_exit)
MODULE_AUTHOR("Aitor Encinas Alonso");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("AQM for HCTNS qdisc");