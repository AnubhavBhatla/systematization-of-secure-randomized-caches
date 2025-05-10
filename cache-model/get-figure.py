#!/usr/bin/python3

import os.path
import subprocess
import threading
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from matplotlib import rcParams
import numpy as np

def read_and_sort_data(file_path):
    x_values = []
    y_values = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split()
            if parts[0] != 'Generate':  # Skip 'Generate' lines and take the values
                x_values.append(float(parts[0]))
                y_values.append(float(parts[1]))
    
    # Pair x and y values and sort by x
    sorted_points = sorted(zip(x_values, y_values), key=lambda point: point[0])
    
    # Unzip sorted points back into separate x and y lists
    x_values_sorted, y_values_sorted = zip(*sorted_points)
    
    return x_values_sorted, y_values_sorted
 
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

# configuration type
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

if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print("Usage: python get-figure.py <1/0: 1 - Use generated results 0 - Generate new results and use them> <figure_number>")
        exit(1)

    option = int(sys.argv[1])
    figureNumber = int(sys.argv[2])
    if option == 0:
        report_path = "report"
    elif option == 1:   
        report_path = "report-original"
    else:
        print("Invalid option. Use 0 for generating new results and 1 for original results.")
        exit(1)
    
    if figureNumber == 3:
        if option == 0:
            run_tests("L2_2048x16",        "list", 2, range(1, 33, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2", "list", 2, range(1, 100, 1), 3600000)
            run_tests("skewed_L2_2048x16-s4", "list", 2, range(1, 200, 1), 3600000)
            run_tests("skewed_L2_2048x16-s8", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s16", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-L2_2048x16.dat')
        plt.plot(x_values, y_values, marker='|', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='CEASER')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2.dat')
        plt.plot(x_values, y_values, marker='x', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s4.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-4')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s8.dat')
        plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-8')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s16.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16')

        # Set labels, title, and save the figure
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='lower right', fontsize='16')
        plt.grid(True)
        plt.xlim(0,300)
        plt.savefig('evrate-skews.pdf')

    
    elif figureNumber == 4:
        if option == 0:
            run_tests("skewed_L2_2048x16-s2", "list", 2, range(1, 100, 1), 3600000)
            run_tests("skewed_L2_2048x16-s4", "list", 2, range(1, 200, 1), 3600000)
            run_tests("skewed_L2_2048x16-s8", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s16", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s4-LB", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s8-LB", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s16-LB", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s4.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-4')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s4-LB.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-4-LA')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s8.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-8')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s8-LB.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-8-LA')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s16.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s16-LB.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16-LA')

        # Set labels, title, and save the figure
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='lower right', fontsize='16')
        plt.grid(True)
        plt.xlim(0,300)
        plt.savefig('evrate-skews-LB.pdf')

    
    elif figureNumber == 5:
        if option == 0:
            run_tests("L2_2048x16",        "list", 2, range(1, 33, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2", "list", 2, range(1, 100, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-INV1-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-INV2-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-INV4-GLRU", "list", 2, range(1, 100, 1), 3600000)
            run_tests("L2_2048x16-INV1-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("L2_2048x16-INV2-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("L2_2048x16-INV4-GLRU", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-L2_2048x16.dat')
        plt.plot(x_values, y_values, marker='|', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='CEASER')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-L2_2048x16-INV1-GLRU.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-1-Inv1-GLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-L2_2048x16-INV2-GLRU.dat')
        plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-1-Inv2-GLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-L2_2048x16-INV4-GLRU.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-1-Inv4-GLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-INV1-GRAN.dat')
        plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv1-GLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-INV2-GRAN.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv2-GLRU')

        # Set labels, title, and save the figure
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='lower right', fontsize='16')
        plt.grid(True)
        plt.xlim(0,100)
        plt.savefig('evrate-globev.pdf')



    elif figureNumber == 6:
        if option == 0:
            run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV1-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV2-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV4-GLRU", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB.dat')
        plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GLRU.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GE')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GLRU.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GE')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GLRU.dat')
        plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GE')

        # Set labels, title, and save the figure
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='upper left', fontsize='14')
        plt.grid(True)
        plt.ylim(-0.05,1.05)
        plt.xlim(-30,300)
        plt.savefig('evrate-LB-globlru.pdf')

    elif figureNumber == 7:
        if option == 0:
            run_tests("skewed_L2_2048x16-s2-LB", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV1", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV4", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB.dat')
        plt.plot(x_values, y_values, marker='x', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV1.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV2.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV4.dat')
        plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='pink', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4')

        # Set labels, title, and grid
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='lower right', fontsize='16')
        plt.grid(True)
        plt.ylim(-0.05, 1.05)

        # Adding the zoomed-in inset
        ax = plt.gca()  # Get the current axis
        inset_ax = inset_axes(ax, width="30%", height="20%", loc="upper left")  # Define inset position and size

        # Define the zoomed-in region
        zoom_x_min, zoom_x_max = 100, 140  # Adjust these values as per your data
        zoom_y_min, zoom_y_max = 0.75, 0.85  # Adjust these values as per your data

        # Plot the same data on the inset axes
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB.dat')
        inset_ax.plot(x_values, y_values, marker='x', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV1.dat')
        inset_ax.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV2.dat')
        inset_ax.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV4.dat')
        inset_ax.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='pink', markersize='6', mew='0.2', linewidth='0.5')

        # Set limits for the inset
        inset_ax.set_xlim(zoom_x_min, zoom_x_max)
        inset_ax.set_ylim(zoom_y_min, zoom_y_max)
        inset_ax.grid(True)

        # Mark the zoomed region on the main plot
        mark_inset(ax, inset_ax, loc1=1, loc2=3, fc="none", ec="0.5")

        inset_ax.set_xticks([])
        inset_ax.set_yticks([])

        # Save the figure
        plt.savefig('evrate-invalid-with-inset.pdf')

    elif figureNumber == 8:
        if option == 0:
            run_tests("skewed_L2_2048x16-s2", "list", 2, range(1, 100, 1), 3600000)
            run_tests("skewed_L2_1024x32-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_512x64-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_256x128-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s16", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass16')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_1024x32-s2.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass32')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x64-s2.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x128-s2.dat')
        plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s16.dat')
        plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16-Ass16')

        # Set labels, title, and save the figure
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='lower right', fontsize='16')
        plt.grid(True)
        plt.xlim(-10,300)
        plt.savefig('evrate-assoc.pdf')



    elif figureNumber == 9:
        if option == 0:
            run_tests("skewed_L2_2048x16-s2-INV2-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_1024x32-s2-LB-INV2-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_512x64-s2-LB-INV2-GLRU", "list", 2, range(1, 350, 1), 3600000)
            run_tests("skewed_L2_256x128-s2-LB-INV2-GLRU", "list", 2, range(1, 350, 1), 3600000)
            run_tests("skewed_L2_2048x16-s16-LB", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass16-LA-Inv2-GRan')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_1024x32-s2-LB-INV2-GRAN.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass32-LA-Inv2-GRan')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x64-s2-LB-INV2-GRAN.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-LA-Inv2-GRan')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x128-s2-LB-INV2-GRAN.dat')
        plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-LA-Inv2-GRan')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s16-LB.dat')
        plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16-Ass16-LA')

        # Set labels, title, and save the figure
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='upper left', fontsize='14')
        plt.grid(True)
        plt.ylim(-0.05,1.05)
        plt.savefig('evrate-assoc-LB-Inv2-GRan.pdf')


    elif figureNumber == 10:
        if option == 0:
            run_tests("skewed_L2_256x128-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_512x64-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_256x128-s2-random", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_512x64-s2-random", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_256x128-s2-srrip", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_512x64-s2-srrip", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_256x128-s2-plru", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_512x64-s2-plru", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x64-s2-random.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-Ran')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x64-s2.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-LRU')
        
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x64-s2-srrip.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-RRIP')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x64-s2-plru.dat')
        plt.plot(x_values, y_values, marker='*', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-RPLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x128-s2-random.dat')
        plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-Ran')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x128-s2.dat')
        plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-LRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x128-s2-srrip.dat')
        plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-RRIP')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x128-s2-plru.dat')
        plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='#008080', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-RPLRU')

        # Set labels, title, and save the figure
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='upper left', fontsize='16')
        plt.grid(True)
        plt.xlim(-10,300)
        plt.savefig('evrate-replacement.pdf')

    elif figureNumber == 11:
        if option == 0:
            run_tests("skewed_L2_2048x16-s2-LB-INV1-GRRIP", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV2-GRRIP", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV4-GRRIP", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV1-GRAN", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV2-GRAN", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV4-GRAN", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV1-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV2-GLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV4-GLRU", "list", 2, range(1, 100, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV1-GPLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV2-GPLRU", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_2048x16-s2-LB-INV4-GPLRU", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRAN.dat')
        plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRan')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GLRU.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRRIP.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRRIP')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GPLRU.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRPLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
        plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRan')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GLRU.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRRIP.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRRIP')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GPLRU.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRPLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRAN.dat')
        plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRan')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GLRU.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GLRU')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRRIP.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRRIP')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GPLRU.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRPLRU')

        # Set labels, title, and save the figure
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='upper left', fontsize='12')
        plt.grid(True)
        plt.ylim(-0.05,1.05)
        plt.xlim(-30,300)
        plt.savefig('evrate-LB-globev.pdf')

    elif figureNumber == 12:
        if option == 0:
            run_tests_attack("skewed_L2_2048x16-s16", "list", 2, range( 3*512*1024, 15*256*1024,  32*1024), "87")
            run_tests_attack("skewed_L2_2048x16-s2", "list", 2, range( 0*512*1024, 5*512*1024,  32*1024), "26")
            run_tests_attack("skewed_L2_2048x16-s2-LB-INV2-GRAN", "list", 2, range( 1536*1024, 3*1024*1024,  32*1024), "70")
            run_tests_attack("skewed_L2_512x64-s2",     "list", 2, range( 3*1024*1024, 4*1024*1024, 32*1024), "116")
            run_tests_attack("skewed_L2_256x128-s2",     "list", 2, range( 7*1024*1024, 8*1024*1024,  32*1024), "241")       
            run_tests_attack("skewed_L2_512x64-s2-LB",     "list", 2, range( 7*512*1024, 13*512*1024, 32*1024), "122")
            run_tests_attack("skewed_L2_256x128-s2-LB",     "list", 2, range( 15*512*1024, 17*512*1024, 32*1024), "244")
        #### Need Plotting Code @Anubhav ####
        print("All results are obtained, manually find the number of evictions corresponding to a probability of 0.5 for forming eviction set of requisite size")
        rcParams.update({'figure.autolayout': True})

        plt.figure(figsize=(10, 6))

        X = ['Skew-16','Skew-2','Skew-2-LA-Inv2-GLRU','Skew-2-Ass64','Skew-2-Ass64-LA-Inv2-GLRU','Skew-2-Ass128','Skew-2-Ass128-LA-Inv2-GLRU']
        Random = [] 

        if (len(Random) != len(X)):
            print("Please add the number of evictions for each configuration to the list named Random")
            exit(1)

        X_axis = np.arange(len(X))

        plt.bar(X_axis, Random, 0.4, label = 'Ran', color=(0.5, 0.5, 0.8), edgecolor='black', linewidth=2)

        # Set labels, title, and save the figure
        plt.xticks(X_axis, X, rotation=20, ha='right', rotation_mode='anchor')

        # plt.xlabel('Cache Design', fontsize='22')
        plt.xticks(fontsize='18')
        plt.ylabel('Number of LLC Evictions\n(in millions)', fontsize='22')
        plt.yticks(np.arange(0, 12, 2), fontsize='16')
        # plt.legend(loc='upper left', fontsize='20')
        plt.grid(axis='y')
        plt.gca().set_axisbelow(True)
        # plt.ylim(0,12)
        plt.savefig('evset-attack-bar.pdf')

    elif figureNumber == 13:
        if option == 0:
            run_tests("skewed_L2_256x64-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_1024x64-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_24576x64-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_128x128-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_512x128-s2", "list", 2, range(1, 300, 1), 3600000)
            run_tests("skewed_L2_12288x128-s2", "list", 2, range(1, 300, 1), 3600000)
        plt.figure(figsize=(12, 6))

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x64-s2.dat')
        plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-1MB')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x64-s2.dat')
        plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-2MB')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_1024x64-s2.dat')
        plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-4MB')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_24576x64-s2.dat')
        plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='pink', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-96MB')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_128x128-s2.dat')
        plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-1MB')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x128-s2.dat')
        plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-2MB')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x128-s2.dat')
        plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-4MB')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_12288x128-s2.dat')
        plt.plot(x_values, y_values, marker='*', markerfacecolor='none', linestyle='-', color='grey', markersize='9', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-96MB')


        # Set labels, grid, and axis limits
        plt.xlabel('Size of Eviction Sets', fontsize='22')
        plt.xticks(fontsize='14')
        plt.ylabel('Eviction Rate', fontsize='22')
        plt.yticks(fontsize='14')
        plt.legend(loc='upper left', fontsize='16')
        plt.grid(True)
        plt.xlim(-10, 300)

        # Adding the zoomed-in inset
        ax = plt.gca()  # Main axis
        inset_ax = inset_axes(ax, width="12.5%", height="32.5%", loc="lower right", borderpad=2)  # Position inset at bottom

        # Plot the same data on the inset axes
        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x64-s2.dat')
        inset_ax.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x64-s2.dat')
        inset_ax.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_1024x64-s2.dat')
        inset_ax.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_24576x64-s2.dat')
        inset_ax.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='pink', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_128x128-s2.dat')
        inset_ax.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_256x128-s2.dat')
        inset_ax.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_512x128-s2.dat')
        inset_ax.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5')

        x_values, y_values = read_and_sort_data(report_path+'/evset-effective-skewed_L2_12288x128-s2.dat')
        inset_ax.plot(x_values, y_values, marker='*', markerfacecolor='none', linestyle='-', color='grey', markersize='9', mew='0.2', linewidth='0.5')

        # Set limits for the inset
        inset_ax.set_xlim(215, 245)
        inset_ax.set_ylim(0.1, 0.4)
        inset_ax.grid(True)

        mark_inset(ax, inset_ax, loc2=1, loc1=3, fc="none", ec="0.5")

        # Remove axis labels from the inset
        inset_ax.set_xticks([])
        inset_ax.set_yticks([])
        plt.savefig('evrate-size-inset.pdf')

    elif figureNumber == 14:
        if option == 0:
            run_tests_attack("skewed_L2_512x64-s2",     "list", 2, range( 3*1024*1024, 4*1024*1024, 32*1024), "116")
            run_tests_attack("skewed_L2_256x64-s2",     "list", 2, range( 3*512*1024, 4*512*1024, 32*1024), "116")
            run_tests_attack("skewed_L2_1024x64-s2",     "list", 2, range( 7*1024*1024, 4*2048*1024, 32*1024), "116")
            run_tests_attack("skewed_L2_256x128-s2",     "list", 2, range( 7*1024*1024, 8*1024*1024,  32*1024), "241")
            run_tests_attack("skewed_L2_128x128-s2",     "list", 2, range( 7*512*1024, 8*512*1024,  32*1024), "241")
            run_tests_attack("skewed_L2_512x128-s2",     "list", 2, range( 15*1024*1024, 8*2048*1024,  32*1024), "241")
        #### Need Plotting Code @Anubhav ####
        print("All results are obtained, manually find the number of evictions corresponding to a probability of 0.5 for forming eviction set of requisite size")
        plt.figure(figsize=(12, 6.4))

        X = ['Skew-2-Ass64-1MB','Skew-2-Ass64-2MB','Skew-2-Ass64-4MB','Skew-2-Ass128-1MB','Skew-2-Ass128-2MB','Skew-2-Ass128-4MB']
        Random = []
        if (len(Random) != len(X)):
            print("Please add the number of evictions for each configuration to the list named Random")
            exit(1)

        X_axis = np.arange(len(X))

        plt.bar(X_axis, Random, 0.4, label = 'Ran', color=(0.5, 0.5, 0.8), edgecolor='black', linewidth=2)

        # Set labels, title, and save the figure
        plt.xticks(X_axis, X, rotation=20, ha='right', rotation_mode='anchor')

        # plt.xlabel('Cache Design', fontsize='22')
        plt.xticks(fontsize='21')
        plt.ylabel('Number of LLC Evictions\n(in millions)', fontsize='26')
        plt.yticks(np.arange(0, 18, 3), fontsize='16')
        # plt.legend(loc='upper left', fontsize='20')
        plt.grid(axis='y')
        plt.gca().set_axisbelow(True)
        # plt.ylim(0,18)
        plt.savefig('evset-attack-size-bar.pdf')

    else:
        print("Invalid figure number for evrate experiment, none of the others done so far")
        exit(1)

