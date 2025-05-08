#!/usr/bin/python3

import os.path
import subprocess
import threading
import sys

# configuration type
test = "test/evset-effective-warmup"

def run_test(ccfg,tcfg,level,evsize,csize,report,warmup):
    s_arg    = "%s %s %d %d %d %d %d" % (ccfg, tcfg, level, evsize, csize, 1000, warmup)
    print(test + " " + s_arg)
    subprocess.call(test + " " + s_arg + " >> " + report, shell=True)    

def run_tests(ccfg, tcfg, level, evrange, csize, warmup):

    threads = []
    report = "report/evset-effective-warmup-%s-%d.dat" %(ccfg, warmup)
    for evsize in evrange:
        thread = threading.Thread(target=run_test, args=(ccfg, tcfg, level, evsize, csize, report, warmup))
        threads.append(thread)
        thread.start()
        if len(threads) >= 16:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()

# RUNNING
# run_tests("skewed_L2_2048x16-s2", "list", 2, range(17, 100, 1), 3600000, 0)
# run_tests("skewed_L2_2048x16-s2", "list", 2, range(17, 100, 1), 3600000, 25)
#

# run_tests("skewed_L2_2048x16-s2", "list", 2, range(17, 100, 1), 3600000, 50)
# run_tests("skewed_L2_2048x16-s2", "list", 2, range(1, 100, 1), 3600000, 75)
# run_tests("skewed_L2_2048x16-s2", "list", 2, range(1, 100, 1), 3600000, 95)

# RUNNING
# run_tests("skewed_L2_2048x16-s2", "list", 2, range(17, 100, 1), 3600000, 100)
#

# run_tests("skewed_L2_2048x16-s2-LB-INV1-GRAN", "list", 2, range(1, 300, 1), 3600000, 100)
# run_tests("skewed_L2_2048x16-s2-LB-INV2-GRAN", "list", 2, range(129, 300, 1), 3600000, 100)
# run_tests("skewed_L2_2048x16-s2-LB-INV4-GRAN", "list", 2, range(161, 300, 1), 3600000, 100)

# RUNNING
# run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(49, 100, 1), 3600000, 0)
# run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(36, 100, 1), 3600000, 25)
# run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(33, 100, 1), 3600000, 50)
# run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(5, 100, 1), 3600000, 75)
# run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(1, 100, 1), 3600000, 95)
# run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(49, 100, 1), 3600000, 100)
# 