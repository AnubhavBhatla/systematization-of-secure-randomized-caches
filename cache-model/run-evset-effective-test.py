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

# run_tests("L2_2048x16",        "list", 2, range(1, 33, 1), 3600000)
# run_tests("skewed_L2_512x16",  "list", 2, range(12, 99, 3), 20000)
# run_tests("skewed_L2_2048x8",  "list", 2, range( 6, 50, 2), 20000)
# run_tests("skewed_L2_2048x12", "list", 2, range( 9, 75, 3), 28000)

# DONE - Skews
# run_tests("skewed_L2_2048x16-s2", "list", 2, range(49, 100, 1), 3600000)
# run_tests("skewed_L2_2048x16-s4", "list", 2, range(153, 200, 1), 3600000)
# run_tests("skewed_L2_2048x16-s8", "list", 2, range(225, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s16", "list", 2, range(348, 400, 1), 3600000)
# DONE

# DONE - Skews with Load Balancing
# run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(200, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s4-LB", "list", 2, range(281, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s8-LB", "list", 2, range(225, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s16-LB", "list", 2, range(295, 300, 1), 3600000)
# DONE

# DONE - 2 Skews with Load Balancing and Invalid ways
# run_tests("skewed_L2_2048x16-s2-LB-INV1", "list", 2, range(200, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV2", "list", 2, range(200, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV4", "list", 2, range(65, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV6", "list", 2, range(200, 300, 1), 3600000)
# run_tests("skewed_L2_1024x32-s2-LB-INV6", "list", 2, range(200, 300, 1), 3600000)
# run_tests("skewed_L2_512x64-s2-LB-INV2", "list", 2, range(300, 500, 1), 3600000)
# DONE

# RUNNING - 2 Skews with Invalid ways and Global Eviction but no Load Balancing
# run_tests("skewed_L2_2048x16-s2-INV1-GRAN", "list", 2, range(49, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-INV4-GRAN", "list", 2, range(1, 100, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-INV6-GRAN", "list", 2, range(33, 100, 1), 3600000)

# DONE - No skews with Invalid ways and Global Eviction
# run_tests("L2_2048x16-INV6-GRAN", "list", 2, range(1, 300, 1), 3600000)
# run_tests("L2_1024x32-INV6-GRAN", "list", 2, range(1, 300, 1), 3600000)
# run_tests("L2_512x64-INV6-GRAN", "list", 2, range(1, 300, 1), 3600000)
# run_tests("L2_256x128-INV6-GRAN", "list", 2, range(1, 300, 1), 3600000)
# DONE

# RUNNING - 2 Skews with Load Balancing, Invalid ways and Global Eviction
# DONE run_tests("skewed_L2_2048x16-s2-LB-INV1-GRAN", "list", 2, range(1, 300, 1), 3600000)
# DONE run_tests("skewed_L2_2048x16-s2-LB-INV1-GLRU", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV2-GRAN", "list", 2, range(145, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV2-GLRU", "list", 2, range(177, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV4-GRAN", "list", 2, range(147, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV4-GLRU", "list", 2, range(145, 300, 1), 3600000)
# DONE run_tests("skewed_L2_2048x16-s2-LB-INV6-GRAN", "list", 2, range(1, 300, 1), 3600000)
# DONE run_tests("skewed_L2_2048x16-s2-LB-INV6-GLRU", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_2048x28-s2-LB-INV6-GRAN", "list", 2, range(145, 300, 1), 3600000)
# run_tests("skewed_L2_2048x28-s2-LB-INV6-GLRU", "list", 2, range(145, 300, 1), 3600000)

# DONE - Sensitivity to Associativity
# run_tests("skewed_L2_1024x32-s2", "list", 2, range(49, 300, 1), 3600000)
# run_tests("skewed_L2_512x64-s2", "list", 2, range(177, 300, 1), 3600000)
# run_tests("skewed_L2_256x128-s2", "list", 2, range(332, 400, 1), 3600000)
# DONE

# Running - Senstitivity to Associativity
# run_tests("skewed_L2_1024x32-s2-LB-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_512x64-s2-LB-INV2-GRAN", "list", 2, range(300, 500, 1), 3600000)
# run_tests("skewed_L2_256x128-s2-LB-INV2-GRAN", "list", 2, range(300, 350, 5), 3600000)

# 1run_tests("skewed_L2_1024x32-s2-LB", "list", 2, range(65, 300, 1), 3600000)
# run_tests("skewed_L2_512x64-s2-LB", "list", 2, range(65, 300, 1), 3600000)
# run_tests("skewed_L2_256x128-s2-LB", "list", 2, range(33, 300, 1), 3600000)

# Sensitivity to Cache Size
# run_tests("skewed_L2_1024x16-s2-LB-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_4096x16-s2-LB-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_8192x16-s2-LB-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)

# Replacement policy
# run_tests("skewed_L2_256x128-s2-random", "list", 2, range(273, 300, 1), 3600000)
# run_tests("skewed_L2_512x64-s2-random", "list", 2, range(273, 300, 1), 3600000)

# run_tests("skewed_L2_256x128-s2-srrip", "list", 2, range(273, 300, 1), 3600000)
# run_tests("skewed_L2_512x64-s2-srrip", "list", 2, range(225, 300, 1), 3600000)

# run_tests("skewed_L2_2048x16-s2-LB-INV1-GRRIP", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV2-GRRIP", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV4-GRRIP", "list", 2, range(1, 300, 1), 3600000)

# run_tests("skewed_L2_2048x16-s2-LB-INV1-GRAN", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV4-GRAN", "list", 2, range(1, 300, 1), 3600000)

# run_tests("skewed_L2_2048x16-s2-LB-INV1-GPLRU", "list", 2, range(1, 300, 1), 3600000)
# run_tests("skewed_L2_2048x16-s2-LB-INV2-GPLRU", "list", 2, range(1, 300, 1), 3600000)
run_tests("skewed_L2_2048x16-s2-LB-INV4-GPLRU", "list", 2, range(1, 300, 1), 3600000)

# run_tests("skewed_L2_2048x16-s2-random", "list", 2, range(288, 300, 3), 3600000)

# Sensitivity to Cache Size
# run_tests("skewed_L2_256x64-s2", "list", 2, range(65, 300, 1), 3600000)
# run_tests("skewed_L2_128x128-s2", "list", 2, range(65, 300, 1), 3600000)

# run_tests("skewed_L2_1024x64-s2", "list", 2, range(65, 300, 1), 3600000)
# run_tests("skewed_L2_512x128-s2", "list", 2, range(65, 300, 1), 3600000)