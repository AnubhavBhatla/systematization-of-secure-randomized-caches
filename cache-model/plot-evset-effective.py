import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

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
 
# # Plotting code
# plt.figure(figsize=(12, 6))
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
# plt.plot(x_values, y_values, marker='|', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='CEASER')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2.dat')
# plt.plot(x_values, y_values, marker='x', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s4.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-4')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s8.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-8')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s16.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16')

# # Set labels, title, and save the figure
# plt.xlabel('Size of Eviction Sets', fontsize='22')
# plt.xticks(fontsize='14')
# plt.ylabel('Eviction Rate', fontsize='22')
# plt.yticks(fontsize='14')
# plt.legend(loc='lower right', fontsize='16')
# plt.grid(True)
# plt.xlim(0,300)
# plt.savefig('evrate-skews.pdf')

# Plotting code
plt.figure(figsize=(12, 6))
 
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s4.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-4')
 
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s4-LB.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-4-LA')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s8.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-8')
 
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s8-LB.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-8-LA')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s16.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s16-LB.dat')
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

# Main figure
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB.dat')
plt.plot(x_values, y_values, marker='x', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV1.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV2.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV6.dat')
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
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB.dat')
inset_ax.plot(x_values, y_values, marker='x', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV1.dat')
inset_ax.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV2.dat')
inset_ax.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV6.dat')
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

# # Plotting code
# plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2.dat')
# plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass16')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_1024x32-s2.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass32')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s16.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16-Ass16')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2-random.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-Ran')

# # Set labels, title, and save the figure
# plt.xlabel('Size of Eviction Sets', fontsize='22')
# plt.xticks(fontsize='14')
# plt.ylabel('Eviction Rate', fontsize='22')
# plt.yticks(fontsize='14')
# plt.legend(loc='lower right', fontsize='16')
# plt.grid(True)
# plt.xlim(-10,300)
# plt.savefig('evrate-assoc.pdf')

# # Plotting code
# plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB.dat')
# plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass16-LA')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_1024x32-s2-LB.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass32-LA')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2-LB.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-LA')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2-LB.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-LA')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s16-LB.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16-Ass16-LA')

# # Set labels, title, and save the figure
# plt.xlabel('Size of Eviction Sets', fontsize='22')
# plt.xticks(fontsize='14')
# plt.ylabel('Eviction Rate', fontsize='22')
# plt.yticks(fontsize='14')
# plt.legend(loc='upper left', fontsize='16')
# plt.grid(True)
# plt.ylim(-0.05,1.05)
# plt.savefig('evrate-assoc-LB.pdf')

# # Plotting code
# plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
# plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass16-LA-Inv2-GRan')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_1024x32-s2-LB-INV2-GRAN.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass32-LA-Inv2-GRan')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2-LB-INV2-GRAN.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-LA-Inv2-GRan')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2-LB-INV2-GRAN.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-LA-Inv2-GRan')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s16-LB.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16-Ass16-LA')

# # Set labels, title, and save the figure
# plt.xlabel('Size of Eviction Sets', fontsize='22')
# plt.xticks(fontsize='14')
# plt.ylabel('Eviction Rate', fontsize='22')
# plt.yticks(fontsize='14')
# plt.legend(loc='upper left', fontsize='14')
# plt.grid(True)
# plt.ylim(-0.05,1.05)
# plt.savefig('evrate-assoc-LB-Inv2-GRan.pdf')

# # Plotting code
# plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
# plt.plot(x_values, y_values, marker='+', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='CEASER')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Inv6-GRan')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_1024x32-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Ass32-Inv6-GRan')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_512x64-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Ass64-Inv6-GRan')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_256x128-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Ass128-Inv6-GRan')

# # Set labels, title, and save the figure
# plt.xlabel('Size of Eviction Sets', fontsize='22')
# plt.xticks(fontsize='14')
# plt.ylabel('Eviction Rate', fontsize='22')
# plt.yticks(fontsize='14')
# plt.legend(loc='lower right', fontsize='16')
# plt.grid(True)
# plt.xlim(0,150)
# plt.savefig('evrate-noskews.pdf')

plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='|', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='CEASER')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-1-Inv1-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-1-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-1-Inv4-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV1-GRAN.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv1-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV6-GRAN.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv4-GLRU')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv6-GRan')

# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='lower right', fontsize='16')
plt.grid(True)
plt.xlim(0,100)
plt.savefig('evrate-globev.pdf')

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Main figure
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='|', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='CEASER')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='CEASER-Inv1-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='CEASER-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='CEASER-Inv4-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV1-GRAN.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv1-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV6-GRAN.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv4-GLRU')

# Set labels, grid, and axis limits
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='lower right', fontsize='16')
plt.grid(True)
plt.xlim(0, 100)

# Adding the zoomed-in inset
ax = plt.gca()  # Main axis
inset_ax = inset_axes(ax, width="30%", height="20%", loc="lower center")  # Position inset

# Plot the same data on the inset axes
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
inset_ax.plot(x_values, y_values, marker='|', linestyle='-', color='blue', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
inset_ax.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
inset_ax.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-L2_2048x16.dat')
inset_ax.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2.dat')
inset_ax.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV1-GRAN.dat')
inset_ax.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV2-GRAN.dat')
inset_ax.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-INV6-GRAN.dat')
inset_ax.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='blue', markersize='10', mew='0.2', linewidth='0.5')

# Set limits for the inset
inset_ax.set_xlim(20, 30)
inset_ax.set_ylim(0.95, 1.05)
inset_ax.grid(True)

mark_inset(ax, inset_ax, loc1=1, loc2=3, fc="none", ec="0.5")


# Remove axis labels from the inset
inset_ax.set_xticks([])
inset_ax.set_yticks([])

# Save the figure
plt.savefig('evrate-globev-zoomed-no-labels.pdf')


# Plotting code
plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB.dat')
# plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRAN.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GLRU.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRan')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRRIP.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRRIP')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GPLRU.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRPLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GLRU.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRan')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRRIP.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRRIP')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GPLRU.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRPLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRAN.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GLRU')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GLRU.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRan')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRRIP.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRRIP')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GPLRU.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRPLRU')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv6-GRan')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x28-s2-LB-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='MIRAGE-GRan')

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

# # Plotting code
# plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB.dat')
# plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

# # x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRAN.dat')
# # plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRan')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GLRU.dat')
# plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GE')

# # x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
# # plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRan')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GLRU.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GE')

# # x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRAN.dat')
# # plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRan')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GLRU.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GE')

# # x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV6-GRAN.dat')
# # plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv6-GRan')

# # x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV6-GLRU.dat')
# # plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv6-GLRU')

# # x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x28-s2-LB-INV6-GRAN.dat')
# # plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='MIRAGE-GRan')

# # x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x28-s2-LB-INV6-GLRU.dat')
# # plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='MIRAGE-GLRU')

# # Set labels, title, and save the figure
# plt.xlabel('Size of Eviction Sets', fontsize='22')
# plt.xticks(fontsize='14')
# plt.ylabel('Eviction Rate', fontsize='22')
# plt.yticks(fontsize='14')
# plt.legend(loc='upper left', fontsize='14')
# plt.grid(True)
# plt.ylim(-0.05,1.05)
# plt.xlim(-30,300)
# plt.savefig('evrate-LB-globlru.pdf')

# # Plotting code
# plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-0.dat')
# plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-0')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-25.dat')
# plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-25')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-50.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-50')

# # x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-75.dat')
# # plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-75')

# # x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-95.dat')
# # plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-95')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-100.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-100')


# # Set labels, title, and save the figure
# plt.xlabel('Size of Eviction Sets', fontsize='22')
# plt.xticks(fontsize='14')
# plt.ylabel('Eviction Rate', fontsize='22')
# plt.yticks(fontsize='14')
# plt.legend(loc='lower right', fontsize='16')
# plt.grid(True)
# plt.savefig('evrate-warmup.pdf')

# # Plotting code
# plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRAN.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRan')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-INV1-GRAN-100.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRan-100')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRan')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-INV2-GRAN-100.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRan-100')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRAN.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRan')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-INV4-GRAN-100.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRan-100')

# # Set labels, title, and save the figure
plt.figure(figsize=(12, 6))
# fig, ax = plt.subplots(figsize=[12,6])

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-0.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-0')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-25.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-25')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-50.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-50')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-75.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-75')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-95.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='grey', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-95')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-100.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-100')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Average Warmup')

# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='lower right', fontsize='16')
plt.grid(True)
plt.xlim(0,100)
plt.savefig('evrate-warmup-LB.pdf')

# Main figure
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-0.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-0')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-25.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-25')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-50.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-50')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-75.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-75')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-95.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='grey', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-95')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-100.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-100')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-Avg')

# Set labels, title, and grid
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='lower right', fontsize='16')
plt.grid(True)
plt.xlim(0, 100)

# Adding the zoomed-in inset
ax = plt.gca()  # Get the current axis
inset_ax = inset_axes(ax, width="30%", height="20%", loc="upper left")  # Define inset position

# Plot the same data on the inset axes
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-0.dat')
inset_ax.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='blue', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-25.dat')
inset_ax.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-50.dat')
inset_ax.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-75.dat')
inset_ax.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-95.dat')
inset_ax.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='grey', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-warmup-skewed_L2_2048x16-s2-LB-100.dat')
inset_ax.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='black', markersize='10', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_2048x16-s2-LB.dat')
inset_ax.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='purple', markersize='10', mew='0.2', linewidth='0.5')

# Set limits for the inset
inset_ax.set_xlim(55, 65)
inset_ax.set_ylim(-0.05, 0.05)
inset_ax.grid(True)

inset_ax.set_xticks([])
inset_ax.set_yticks([])

mark_inset(ax, inset_ax, loc2=1, loc1=3, fc="none", ec="0.5")

# Save the figure
plt.savefig('evrate-warmup-LB-zoomed.pdf')

plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x64-s2.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-1MB')
 
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-2MB')
 
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_1024x64-s2.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-4MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_128x128-s2.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-1MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-2MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x128-s2.dat')
plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-4MB')

# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='upper left', fontsize='16')
plt.grid(True)
plt.xlim(-10,300)
plt.savefig('evrate-size.pdf')

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Main figure
plt.figure(figsize=(12, 6))

# Plot the main data
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x64-s2.dat')
# plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-1MB')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-2MB')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_1024x64-s2.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-4MB')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_128x128-s2.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-1MB')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-2MB')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x128-s2.dat')
# plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-4MB')
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x64-s2.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-1MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-2MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_1024x64-s2.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-4MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_24576x64-s2.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='pink', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-96MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_128x128-s2.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-1MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-2MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x128-s2.dat')
plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-4MB')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_12288x128-s2.dat')
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
x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x64-s2.dat')
inset_ax.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2.dat')
inset_ax.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_1024x64-s2.dat')
inset_ax.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_24576x64-s2.dat')
inset_ax.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='pink', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_128x128-s2.dat')
inset_ax.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2.dat')
inset_ax.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x128-s2.dat')
inset_ax.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5')

x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_12288x128-s2.dat')
inset_ax.plot(x_values, y_values, marker='*', markerfacecolor='none', linestyle='-', color='grey', markersize='9', mew='0.2', linewidth='0.5')

# Set limits for the inset
inset_ax.set_xlim(215, 245)
inset_ax.set_ylim(0.1, 0.4)
inset_ax.grid(True)

mark_inset(ax, inset_ax, loc2=1, loc1=3, fc="none", ec="0.5")

# Remove axis labels from the inset
inset_ax.set_xticks([])
inset_ax.set_yticks([])



# # Plotting code
# plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2-random.dat')
# plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-Random')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-LRU')
 
# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_512x64-s2-srrip.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-SRRIP')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2-random.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-Random')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-LRU')

# x_values, y_values = read_and_sort_data('report-anubhav/evset-effective-skewed_L2_256x128-s2-srrip.dat')
# plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-SRRIP')

# # Set labels, title, and save the figure
# plt.xlabel('Size of Eviction Sets', fontsize='22')
# plt.xticks(fontsize='14')
# plt.ylabel('Eviction Rate', fontsize='22')
# plt.yticks(fontsize='14')
# plt.legend(loc='upper left', fontsize='16')
# plt.grid(True)
# plt.xlim(-10,300)
# plt.savefig('evrate-replacement.pdf')