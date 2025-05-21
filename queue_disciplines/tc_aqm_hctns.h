#ifndef __LINUX_TC_AQM_HCTNS_H
#define __LINUX_TC_AQM_HCTNS_H

#include <linux/types.h>

struct tc_aqm_hctns_qopt {
    __u32 limit; //Maximum number of packets queued
};

#endif
