#!/usr/bin/python3

import os.path
import subprocess
import threading
import sys

# configuration type
test = "test/evset-attack-ppp"

def run_test(ccfg, tcfg, level, period, other, report):
    s_arg    = "%s %s %d %d %d %s" % (ccfg, tcfg, level, period, 5, other)
    print(test + " " + s_arg)
    subprocess.call(test + " " + s_arg + " >> " + report, shell=True)

def run_tests(ccfg, tcfg, level, prange, other):
    threads = []
    report = "report/evset-attack-ppp-%s-%s.dat" %(ccfg, other)

    for period in prange:
        thread = threading.Thread(target=run_test, args=(ccfg, tcfg, level, period, other, report))
        threads.append(thread)
        thread.start()
        if len(threads) >= 32:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()

# run_tests("L2_1024x16_RCL",     "list", 2, range( 1*16*1024, 32*16*1024,  12*1024), "16")
# run_tests("skewed_L2_1024x32-s2",     "list", 2, range( 16*16*1024, 48*16*1024,  12*1024), "25")

# run_tests("skewed_L2_512x64-s2",     "list", 2, range(2*512*1024, 5*256*1024, 32*1024), "10")
# run_tests("skewed_L2_512x64-s2",     "list", 2, range(2*512*1024, 5*256*1024, 32*1024), "20")

# run_tests("skewed_L2_256x64-s2",     "list", 2, range( 3*512*1024, 4*512*1024, 32*1024), "116")
# run_tests("skewed_L2_1024x64-s2",     "list", 2, range( 7*1024*1024, 4*2048*1024, 32*1024), "116")

# run_tests("skewed_L2_256x128-s2",     "list", 2, range( 9*1024*1024, 10*1024*1024,  32*1024), "241")
# run_tests("skewed_L2_128x128-s2",     "list", 2, range( 7*512*1024, 8*512*1024,  32*1024), "241")
# run_tests("skewed_L2_512x128-s2",     "list", 2, range( 15*1024*1024, 8*2048*1024,  32*1024), "241")

# run_tests("skewed_L2_512x64-s2-LB",     "list", 2, range( 7*512*1024, 9*512*1024, 32*1024), "122")
# run_tests("skewed_L2_256x128-s2-LB",     "list", 2, range( 15*512*1024, 17*512*1024, 32*1024), "244")
# run_tests("skewed_L2_1024x16-s4",     "list", 2, range( 24*16*1024, 80*16*1024,  12*1024), "45")
# run_tests("skewed_L2_1024x16-s8",     "list", 2, range( 48*16*1024, 120*16*1024,  12*1024), "68")

# run_tests("skewed_L2_2048x16-s16", "list", 2, range(3*256*1024, 2*512*1024,  32*1024), "10")
# run_tests("skewed_L2_2048x16-s16", "list", 2, range(2*512*1024, 3*512*1024,  32*1024), "20")

# run_tests("skewed_L2_2048x16-s16-LB", "list", 2, range( 1.5*1024*1024, 3*1024*1024,  32*1024), "125")
