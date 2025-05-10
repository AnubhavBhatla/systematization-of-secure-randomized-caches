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


def read_and_sort_data_attack(file_path):
    x_values = []
    y_values = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            # Split the line into parts
            parts = lines[i].split()
            if (parts[0] == 'Generate') or (parts[0] == 'Test'):  # Even index: take x value
                pass
            else:           # Odd index: take y value
                parts = lines[i].split(',')
                if len(parts) < 2:
                    continue
                if (parts[1] == ' Inter'):
                    pass
                else:
                    x_values.append(float(parts[0]))
                    y_values.append(float(parts[1]))

    # Pair x and y values and sort by x
    sorted_points = sorted(zip(x_values, y_values), key=lambda point: point[0])
    
    # Unzip sorted points back into separate x and y lists
    x_values_sorted, y_values_sorted = zip(*sorted_points)
    
    return x_values_sorted, y_values_sorted


def find_x_for_y_half(x_values, y_values):
    for i in range(1, len(y_values)):
        if y_values[i-1] < 0.5 <= y_values[i]:
            # Linear interpolation
            x0, x1 = x_values[i-1], x_values[i]
            y0, y1 = y_values[i-1], y_values[i]
            return x0 + (0.5 - y0) * (x1 - x0) / (y1 - y0)
        elif y_values[i] == 0.5:
            # If y is exactly 0.5, return the corresponding x value
            return x_values[i]
        elif y_values[i-1] == 0.5:
            # If y is exactly 0.5, return the corresponding x value
            return x_values[i-1]
    raise ValueError("No crossing at y=0.5 found in the data.")


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
    if len(sys.argv) != 3:
        print("Usage: python3 get-table.py <1/0 1: Use generated results, 0: Generate new results> <table number>")
        sys.exit(1)

    option = int(sys.argv[1])
    if option == 0:
        report_path = "report"
    elif option == 1:
        report_path = "report-original"
    else:
        print("Invalid option. Please enter 0 or 1.")
        sys.exit(1)


    tableNum = int(sys.argv[2])
 
    if tableNum == 1:
        print("No experiment was performed for table 1")
    elif tableNum == 2:
        # stuff
        if option == 0:
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

        x_values_ppp = {}
        y_values_ppp = {}
        x_values_ct = {}
        y_values_ct = {}

        ppp_vals = {}
        ct_vals = {}

        for config in ["skewed_L2_2048x16-s16", "skewed_L2_512x64-s2"]:
            ppp_vals[config] = []
            ct_vals[config] = []
            x_values_ppp[config] = {}
            y_values_ppp[config] = {}
            x_values_ct[config] = {}
            y_values_ct[config] = {}
            for other in ["10", "20", "30", "40"]:
                file_path = report_path + "/evset-attack-ppp-%s-%s.dat" % (config, other)
                x_values_ppp[config][other], y_values_ppp[config][other] = read_and_sort_data_attack(file_path)
                try:
                    x_half = find_x_for_y_half(x_values_ppp[config][other], y_values_ppp[config][other])
                    ppp_vals[config].append(float(float(x_half)/float(1000000)))
                except ValueError as e:
                    print(e,config,other,"PPP")
                file_path = report_path + "/evset-attack-%s-%s.dat" % (config, other)
                x_values_ct[config][other], y_values_ct[config][other] = read_and_sort_data_attack(file_path)
                try:
                    x_half = find_x_for_y_half(x_values_ct[config][other], y_values_ct[config][other])
                    ct_vals[config].append(float(float(x_half)/float(1000000)))
                except ValueError as e:
                    print(y_values_ct[config][other])
                    print(e,config,other,"CT")
        print("===================================================")
        print("| PPP-Skew-16 | PPP-Ass64 | CT-Skew-16 | CT-Ass64 |")
        print("===================================================")  
        for i in range(4):
            print("| %10.1f | %10.1f | %10.1f | %9.1f|" % (ppp_vals["skewed_L2_2048x16-s16"][i], ppp_vals["skewed_L2_512x64-s2"][i], ct_vals["skewed_L2_2048x16-s16"][i], ct_vals["skewed_L2_512x64-s2"][i]))   
        print("===================================================") 





    elif tableNum == 3:
        # champsim
        print("Performance results were obtained using Champsim simulator")
        exit(0)
    else:
        print("Invalid table number. Please enter 1, 2, or 3.")
        sys.exit(1) 