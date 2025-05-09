#!/usr/bin/python3

import os.path
import subprocess
import threading
import sys

# configuration type
test = "test/evset-effective"

def run_test(ccfg,tcfg,level,evsize,csize,report):
    s_arg    = "%s %s %d %d %d %d" % (ccfg, tcfg, level, evsize, csize, 1000)
    print(test + " " + s_arg)
    subprocess.call(test + " " + s_arg + " >> " + report, shell=True)    

def run_tests(ccfg, tcfg, level, evrange, csize):

    threads = []
    report = "report/evset-effective-%s.dat" %(ccfg)
    for evsize in evrange:
        thread = threading.Thread(target=run_test, args=(ccfg, tcfg, level, evsize, csize, report))
        threads.append(thread)
        thread.start()
        if len(threads) >= 20:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()

# Figure 3
print("Running Experiments and gathering data for Figure 3: Skew Sensitivity")
run_tests("L2_2048x16",        "list", 2, range(1, 33, 1), 3600000)
run_tests("skewed_L2_2048x16-s2", "list", 2, range(1, 100, 1), 3600000)
run_tests("skewed_L2_2048x16-s4", "list", 2, range(1, 200, 1), 3600000)
run_tests("skewed_L2_2048x16-s8", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s16", "list", 2, range(1, 300, 1), 3600000)

# Figure 4
print("Running Experiments and gathering data for Figure 4: Skew Sensitivity across Load Balancing")
run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s4-LB", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s8-LB", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s16-LB", "list", 2, range(1, 300, 1), 3600000)

# Figure 5
print("Running Experiments and gathering data for Figure 5: Invalid ways and Global Eviction")
run_tests("skewed_L2_2048x16-s2-INV1-GRAN", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-INV4-GRAN", "list", 2, range(1, 100, 1), 3600000)
run_tests("L2_2048x16-INV1-GRAN", "list", 2, range(1, 300, 1), 3600000)
run_tests("L2_2048x16-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
run_tests("L2_2048x16-INV4-GRAN", "list", 2, range(1, 300, 1), 3600000)

# Figure 6
print("Running Experiments and gathering data for Figure 6: Invalid ways and Global Eviction with Load Balancing")
run_tests("skewed_L2_2048x16-s2-LB-INV1", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV2", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV4", "list", 2, range(1, 300, 1), 3600000)

# Figure 7
print("Running Experiments and gathering data for Figure 7: Invalid ways with Load Balancing")
run_tests("skewed_L2_2048x16-s2-LB-INV1", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV2", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV4", "list", 2, range(1, 300, 1), 3600000)

# Figure 8
print("Running Experiments and gathering data for Figure 8: Associativity Sensitivity")
run_tests("skewed_L2_1024x32-s2", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_512x64-s2", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_256x128-s2", "list", 2, range(1, 300, 1), 3600000)

# Figure 9
print("Running Experiments and gathering data for Figure 9: Associativity Sensitivity with Load Balancing, Invalid ways and Global Eviction")
run_tests("skewed_L2_1024x32-s2-LB-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_512x64-s2-LB-INV2-GRAN", "list", 2, range(1, 350, 1), 3600000)
run_tests("skewed_L2_256x128-s2-LB-INV2-GRAN", "list", 2, range(1, 350, 1), 3600000)

# Figure 10
print("Running Experiments and gathering data for Figure 10: Replacement Policy Sensitivity")
run_tests("skewed_L2_256x128-s2-random", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_512x64-s2-random", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_256x128-s2-srrip", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_512x64-s2-srrip", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_256x128-s2-plru", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_512x64-s2-plru", "list", 2, range(1, 300, 1), 3600000)

# Figure 11
print("Running Experiments and gathering data for Figure 11: Global Replacement Policy Sensitivity")
run_tests("skewed_L2_2048x16-s2-LB-INV1-GRRIP", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV2-GRRIP", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV4-GRRIP", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV1-GRAN", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV4-GRAN", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV1-GPLRU", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV2-GPLRU", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV4-GPLRU", "list", 2, range(1, 300, 1), 3600000)

# Figure 13
print("Running Experiments and gathering data for Figure 13: Cache Size Sensitivity")
run_tests("skewed_L2_256x64-s2", "list", 2, range(65, 300, 1), 3600000)
run_tests("skewed_L2_1024x64-s2", "list", 2, range(65, 300, 1), 3600000)
run_tests("skewed_L2_24576x64-s2", "list", 2, range(65, 300, 1), 3600000)
run_tests("skewed_L2_128x128-s2", "list", 2, range(65, 300, 1), 3600000)
run_tests("skewed_L2_512x128-s2", "list", 2, range(65, 300, 1), 3600000)
run_tests("skewed_L2_12288x128-s2", "list", 2, range(65, 300, 1), 3600000)
