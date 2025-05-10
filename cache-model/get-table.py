#!/usr/bin/python3

import os.path
import subprocess
import threading
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from matplotlib import rcParams
import numpy as np

test_attack = "test/evset-attack"

def run_test_attack(ccfg, tcfg, level, period, other,report):
    s_arg    = "%s %s %d %d %d %s" % (ccfg, tcfg, level, period, 10, other)
    print(test_attack + " " + s_arg)
    subprocess.call(test_attack + " " + s_arg + " >> " + report, shell=True)

def run_tests_attack(ccfg, tcfg, level, prange, other):
    threads = []
    report = "report/evset-attack-%s-%s.dat" %(ccfg, other)

    for period in prange:
        thread = threading.Thread(target=run_test_attack, args=(ccfg, tcfg, level, period, other, report))
        threads.append(thread)
        thread.start()
        if len(threads) >= 15:
            for t in threads:
                t.join()
            threads = []
    for t in threads:
        t.join()


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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 get-table.py <table number>")
        sys.exit(1)

    tableNum = int(sys.argv[1])
 
    if tableNum == 1:
        print("No experiment was performed for table 1")
    elif tableNum == 2:
        # stuff
        run_tests_attack("skewed_L2_2048x16-s16", "list", 2, range( 100*1000, 10*100*1000,  100*1000), "10")
        run_tests_attack("skewed_L2_2048x16-s16", "list", 2, range( 5*100*1000, 20*100*1000,  100*1000), "20")
        run_tests_attack("skewed_L2_2048x16-s16", "list", 2, range( 10*100*1000, 15*100*1000,  100*1000), "30")
        run_tests_attack("skewed_L2_2048x16-s16", "list", 2, range( 10*100*1000, 30*100*1000,  100*1000), "40")
        run_tests_attack("skewed_L2_512x64-s2", "list", 2, range( 100*1000, 10*100*1000,  100*1000), "10")
        run_tests_attack("skewed_L2_512x64-s2", "list", 2, range( 5*100*1000, 20*100*1000,  100*1000), "20")
        run_tests_attack("skewed_L2_512x64-s2", "list", 2, range( 10*100*1000, 15*100*1000,  100*1000), "30")
        run_tests_attack("skewed_L2_512x64-s2", "list", 2, range( 10*100*1000, 30*100*1000,  100*1000), "40")
        run_tests("skewed_L2_2048x16-s16", "list", 2, range( 100*1000, 20*100*1000,  100*1000), "10")
        run_tests("skewed_L2_2048x16-s16", "list", 2, range( 5*100*1000, 40*100*1000,  100*1000), "20")
        run_tests("skewed_L2_2048x16-s16", "list", 2, range( 10*100*1000, 30*100*1000,  100*1000), "30")
        run_tests("skewed_L2_2048x16-s16", "list", 2, range( 10*100*1000, 60*100*1000,  100*1000), "40")
        run_tests("skewed_L2_512x64-s2", "list", 2, range( 100*1000, 20*100*1000,  100*1000), "10")
        run_tests("skewed_L2_512x64-s2", "list", 2, range( 5*100*1000, 40*100*1000,  100*1000), "20")
        run_tests("skewed_L2_512x64-s2", "list", 2, range( 10*100*1000, 30*100*1000,  100*1000), "30")
        run_tests("skewed_L2_512x64-s2", "list", 2, range( 10*100*1000, 60*100*1000,  100*1000), "40")
        print("Results obtained, now extract number of evictions corresponding to 0.5% probability of obtaining eviction set")

    elif tableNum == 3:
        # champsim
        print("Performance results were obtained using Champsim simulator")
        exit(0)
    else:
        print("Invalid table number. Please enter 1, 2, or 3.")
        sys.exit(1) 