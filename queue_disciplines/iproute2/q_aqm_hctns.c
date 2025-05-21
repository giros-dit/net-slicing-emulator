/* SPDX-License-Identifier: GPL-2.0-or-later */
/*
 * q_aqm_hctns.c		AQM HCTNS queue userspace parser for aqm_hctns qdisc
 *
 * Matches kernel module sch_aqm_hctns
 *
 * Authors:	Aitor Encinas Alonso <aitor.encinas.alonso@alumnos.upm.es>
 */

 #include <stdio.h>
 #include <stdlib.h>
 #include <unistd.h>
 #include <string.h>
 #include <linux/tc_aqm_hctns.h>
 
 #include "utils.h"
 #include "tc_util.h"

 static void explain(void)
{
	fprintf(stderr, "Usage: ... aqm_hctns [ limit NUMBER_PACKETS ]\n");
}

 /*
 * aqm_hctns_parse_opt: Parses the options for the aqm_hctns qdisc
 * qu: pointer to the qdisc_util structure
 * argc,argv used for parsing arguments of type limit 1000, argc is the number of arguments and argv a vector of arguments
 * n is a pointer to the Netlink message which will be sent to the kernel
 * dev is the name of the device
 * opt is the structure that will be filled with the parsed options; As default, limit is set to 1000 packets
 */
 static int aqm_hctns_parse_opt(const struct qdisc_util *qu, int argc, char **argv,  struct nlmsghdr *n, const char *dev)
{
    struct tc_aqm_hctns_qopt opt = {
        .limit = 1000, // default if not specified
    };

    while (argc > 0) {
		if (strcmp(*argv, "limit") == 0) { // If the argument is "limit"
			NEXT_ARG(); // Get the value of limit. It moves the pointer to the next argument and decereases argc by 1.
			if (get_size(&opt.limit, *argv)) { // Stores the value of limit in opt.limit. If the operation succeeds, it returns 0 (false)
				fprintf(stderr, "aqm_hctns: invalid limit\n");
				return -1;
			}
		} else {
			fprintf(stderr, "aqm_hctns: unknown argument '%s'\n", *argv);
            explain();
			return -1;
		}
		argc--;
		argv++;
	}
    
	addattr_l(n, 1024, TCA_OPTIONS, &opt, sizeof(opt)); // Add the options to the Netlink message. So that, when the kernel receives the message, it can parse the options and set the values in the kernel module.
	return 0;
}

/*
 * aqm_hctns_print_opt: Prints the options for the aqm_hctns qdisc
 * qu: pointer to the qdisc_util structure
 * f: file pointer to print the options
 * opt: pointer to the rtattr structure that contains the options
 */
static int aqm_hctns_print_opt(const struct qdisc_util *qu, FILE *f, struct rtattr *opt)
{
	struct tc_aqm_hctns_qopt *qopt;

	if (opt == NULL)
		return 0;

	if (RTA_PAYLOAD(opt) < sizeof(*qopt))
		return -1;

	qopt = RTA_DATA(opt);

	fprintf(f, "limit %u ", qopt->limit);
	return 0;
}

struct qdisc_util aqm_hctns_qdisc_util = {
	.id = "aqm_hctns",
	.parse_qopt = aqm_hctns_parse_opt,
	.print_qopt = aqm_hctns_print_opt,
};