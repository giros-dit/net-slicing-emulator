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
#include <linux/spinlock.h>
#include <net/pkt_sched.h>
#include <net/inet_ecn.h>
#include <net/sch_generic.h>
#include <linux/tc_aqm_hctns.h>
#include <linux/tracepoint.h>
#include <linux/netlink.h> 

struct ecn_skb_node {
	struct sk_buff *skb; // Pointer to the packet (what we store) with ECN flag
	struct list_head list; // Wrap the pointer of the skb into a list
};

struct aqm_hctns_sched_data {
    u32 limit;
	struct list_head ecn_list; // Internal List to store ecn_skb_nodes. A list_head stores pointers to the next and previous elements in the list, and the elements can not be skb because they'll corrupt the qdisc.
	spinlock_t lock; // Spinlock to protect the list from concurrent access
};

#define SCH_AQM_HCTNS(sch) ((struct aqm_hctns_sched_data *)qdisc_priv(sch))

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

/*Enqueue or discard packets when arrive to the queue*/
static int aqm_hctns_enqueue(struct sk_buff *skb, struct Qdisc *sch,
			 struct sk_buff **to_free)
{
	struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
	bool has_ecn = skb_has_ecn_ce(skb);

	if (unlikely(READ_ONCE(q->limit) == 0))
		return qdisc_drop(skb, sch, to_free);

	if (likely(sch->q.qlen < READ_ONCE(q->limit))){
		if (has_ecn) {
			/* Store the packet with ECN flag in the internal queue*/
			struct ecn_skb_node *node = kmalloc(sizeof(*node), GFP_ATOMIC); // Allocate dynamic memory for the node
			if (node) {
				node->skb = skb;
				spin_lock_bh(&q->lock); // Lock the list to protect it from concurrent access
				list_add_tail(&node->list, &q->ecn_list);
				spin_unlock_bh(&q->lock); // Unlock the list
			} else {
				trace_printk("Memory allocation failed for ecn_skb_node\n");
				return qdisc_drop(skb, sch, to_free); // Drop the packet if memory allocation fails
			}
		}
		int ret = qdisc_enqueue_tail(skb, sch);
		if (likely(ret == NET_XMIT_SUCCESS)) {
			return ret;
		} else {
			trace_printk("Packet not enqueued, study this failure\n");
			return ret;
		}

	} 

	// If the queue is full and the packet has ECN flag, we drop it
	if (has_ecn)
		return qdisc_drop(skb, sch, to_free);

	/*
	* Else, we drop an ECN packet and enqueue the new packet
	* list_entry allows to get the struct from the list_head pointer, the type of the struct and the name of the list_header within the struct
	*/
	spin_lock_bh(&q->lock);
	if (!list_empty(&q->ecn_list)) {
		struct ecn_skb_node *node = list_entry(q->ecn_list.prev, struct ecn_skb_node, list); // Get the last node in the list
		struct sk_buff *ecn_victim = node->skb; // Get the skb from the node
		if (ecn_victim) {
			list_del(&node->list); // Remove the node from the list
			kfree(node); // Free the node
			spin_unlock_bh(&q->lock); // Unlock the list
			int ret = qdisc_drop(ecn_victim, sch, to_free); // Drop the packet with ECN flag
			if (ret == NET_XMIT_DROP) {
				int ret2 = qdisc_enqueue_tail(skb, sch);
				if (likely(ret2 == NET_XMIT_SUCCESS)) {
					return ret2;
				} else {
					trace_printk("148737843287 Packet not enqueued, study this failure\n");
					return ret2;
				}
			} else {
				trace_printk("Packet with ECN flag not dropped, so lists are not synchronized\n");
				return qdisc_drop(skb, sch, to_free); // Drop the new packet
			}
		}
		spin_unlock_bh(&q->lock); // Unlock the list
		trace_printk("ecn_victim not found\n");
		return qdisc_drop(skb, sch, to_free); // Drop the new packet

	}
	spin_unlock_bh(&q->lock);
	/* If the queue is full and there are no packets with ECN flag, drop the new packet */
	return qdisc_drop(skb, sch, to_free);
}

static struct sk_buff *aqm_hctns_dequeue(struct Qdisc *sch) {
	struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);

	struct sk_buff *skb = qdisc_dequeue_head(sch);

	if (skb && skb_has_ecn_ce(skb)) {
		spin_lock_bh(&q->lock);
		/* Delete the packet with ECN flag in the internal list*/
		if (!list_empty(&q->ecn_list)) {
			struct ecn_skb_node *node = list_entry(q->ecn_list.next, struct ecn_skb_node, list); // Get the first node in the list
			if (node->skb == skb){
				list_del(&node->list); // Remove the node from the list
				spin_unlock_bh(&q->lock); // Unlock the list
				kfree(node); // Free the node
			} else {
				spin_unlock_bh(&q->lock);
				trace_printk("Packet with ECN flag not found in the list, so lists are not synchronized\n");
			} 
		} else {
		spin_unlock_bh(&q->lock);
		trace_printk("ecn_victim not found dequeuing\n");
		}
	}
	return skb;
}

static void aqm_hctns_reset(struct Qdisc *sch) {
    struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
	struct ecn_skb_node *node, *tmp;

	spin_lock_bh(&q->lock);
	list_for_each_entry_safe(node, tmp, &q->ecn_list, list) {
		list_del(&node->list); 
		kfree(node);
	}
	spin_unlock_bh(&q->lock);
	// Reset the qdisc queue
	qdisc_reset_queue(sch);
}

static int aqm_hctns_init(struct Qdisc *sch, struct nlattr *opt, struct netlink_ext_ack *extack) {
	struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
	INIT_LIST_HEAD(&q->ecn_list);
	spin_lock_init(&q->lock); // Initialize the spinlock

    if (opt) {
        struct tc_aqm_hctns_qopt *ctl = nla_data(opt);
		if (nla_len(opt) < sizeof(*ctl))
			return -EINVAL;
        WRITE_ONCE(q->limit, ctl->limit);
    } else {
		u32 limit = qdisc_dev(sch)->tx_queue_len;
		WRITE_ONCE(q->limit, limit);
	}

    return 0;
}

static int aqm_hctns_change(struct Qdisc *sch, struct nlattr *opt, struct netlink_ext_ack *extack) {

	struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);

    if (!opt)
        return -EINVAL;

    struct tc_aqm_hctns_qopt *ctl = nla_data(opt);
    
	if (nla_len(opt) < sizeof(*ctl))
		return -EINVAL;

	WRITE_ONCE(q->limit, ctl->limit);
    return 0;
}

static int aqm_hctns_dump(struct Qdisc *sch, struct sk_buff *skb) {
	struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
    struct tc_aqm_hctns_qopt opt = { .limit = READ_ONCE(q->limit) };

    return nla_put(skb, TCA_OPTIONS, sizeof(opt), &opt);
}


static void aqm_hctns_destroy(struct Qdisc *sch)
{
    struct aqm_hctns_sched_data *q = SCH_AQM_HCTNS(sch);
	struct ecn_skb_node *node, *tmp;

	spin_lock_bh(&q->lock);
	list_for_each_entry_safe(node, tmp, &q->ecn_list, list) {
		list_del(&node->list); 
		kfree(node);
	}
	spin_unlock_bh(&q->lock);

	qdisc_reset_queue(sch);
}

struct Qdisc_ops aqm_hctns_qdisc_ops __read_mostly = {
	.id		    =	"aqm_hctns",
	.priv_size	=	sizeof(struct aqm_hctns_sched_data),
	.enqueue	=	aqm_hctns_enqueue,
	.dequeue	=	aqm_hctns_dequeue,
	.peek		=	qdisc_peek_dequeued,
	.init		=	aqm_hctns_init,
	.destroy	=	aqm_hctns_destroy,
	.reset		=	aqm_hctns_reset,
	.change		=	aqm_hctns_change,
	.dump		=	aqm_hctns_dump,
	.owner		=	THIS_MODULE,
};
MODULE_ALIAS("sch_aqm_hctns");

static int __init aqm_hctns_module_init(void)
{
	return register_qdisc(&aqm_hctns_qdisc_ops);
}
static void __exit aqm_hctns_module_exit(void)
{
	unregister_qdisc(&aqm_hctns_qdisc_ops);
}

module_init(aqm_hctns_module_init)
module_exit(aqm_hctns_module_exit)
MODULE_AUTHOR("Aitor Encinas Alonso");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("AQM for HCTNS qdisc");


