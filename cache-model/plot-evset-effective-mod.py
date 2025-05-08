import matplotlib.pyplot as plt

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
 
# Plotting code
plt.figure(figsize=(12, 6))
 
x_values, y_values = read_and_sort_data('report/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='|', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='CEASER')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2.dat')
plt.plot(x_values, y_values, marker='x', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s4.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-4')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s8.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-8')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s16.dat')
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

# Plotting code
plt.figure(figsize=(12, 6))
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s4.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-4')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s4-LB.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-4-LA')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s8.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-8')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s8-LB.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-8-LA')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s16.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s16-LB.dat')
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

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB.dat')
plt.plot(x_values, y_values, marker='x', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV1.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV2.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV6.dat')
plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='pink', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV6.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='pink', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv6')
 
# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_1024x32-s2-LB-INV6.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv6-Ass32')
 
# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_512x64-s2-LB-INV6.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv6-Ass64')
 
# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='lower right', fontsize='16')
plt.grid(True)
plt.ylim(-0.05,1.05)
plt.savefig('evrate-invalid.pdf')

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass16')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_1024x32-s2.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass32')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_512x64-s2.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_256x128-s2.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s16.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16-Ass16')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_256x128-s2-random.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-Ran')

# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='lower right', fontsize='16')
plt.grid(True)
plt.xlim(-10,300)
plt.savefig('evrate-assoc.pdf')

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass16-LA')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_1024x32-s2-LB.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass32-LA')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_512x64-s2-LB.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-LA')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_256x128-s2-LB.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-LA')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s16-LB.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16-Ass16-LA')

# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='upper left', fontsize='16')
plt.grid(True)
plt.ylim(-0.05,1.05)
plt.savefig('evrate-assoc-LB.pdf')

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass16-LA-Inv2-GLRU')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_1024x32-s2-LB-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass32-LA-Inv2-GLRU')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_512x64-s2-LB-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-LA-Inv2-GLRU')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_256x128-s2-LB-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-LA-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s16.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-16-Ass16')

# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='upper left', fontsize='16')
plt.grid(True)
plt.xlim(-30,300)
plt.ylim(-0.05,1.05)
plt.savefig('evrate-assoc-LB-Inv2-GE.pdf')

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='+', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='CEASER')

x_values, y_values = read_and_sort_data('report/evset-effective-L2_2048x16-INV6-GRAN.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Inv6-GRan')
 
x_values, y_values = read_and_sort_data('report/evset-effective-L2_1024x32-INV6-GRAN.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Ass32-Inv6-GRan')
 
x_values, y_values = read_and_sort_data('report/evset-effective-L2_512x64-INV6-GRAN.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Ass64-Inv6-GRan')
 
x_values, y_values = read_and_sort_data('report/evset-effective-L2_256x128-INV6-GRAN.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Ass128-Inv6-GRan')

# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='lower right', fontsize='16')
plt.grid(True)
plt.xlim(0,150)
plt.savefig('evrate-noskews.pdf')

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='|', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='CEASER')

x_values, y_values = read_and_sort_data('report/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-1-Inv1-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-1-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-L2_2048x16.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-1-Inv4-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-INV1-GRAN.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv1-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-INV6-GRAN.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Inv4-GLRU')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-INV6-GRAN.dat')
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


# Plotting code
plt.figure(figsize=(12, 6))

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB.dat')
# plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GLRU.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRan')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRAN.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRRIP.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRRIP')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GLRU.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRan')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRRIP.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRRIP')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GLRU.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRan')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRAN.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRRIP.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRRIP')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv6-GRan')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x28-s2-LB-INV6-GRAN.dat')
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

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB.dat')
plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRAN.dat')
# plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GRan')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRAN.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GLRU')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GRan')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GLRU')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRAN.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GRan')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRAN.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GLRU')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv6-GRan')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV6-GLRU.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv6-GLRU')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x28-s2-LB-INV6-GRAN.dat')
# plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='MIRAGE-GRan')

# x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x28-s2-LB-INV6-GLRU.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='MIRAGE-GLRU')

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

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-0.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-0')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-25.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-25')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-50.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-50')

# x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-75.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-75')

# x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-95.dat')
# plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-95')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-100.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-100')


# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='lower right', fontsize='16')
plt.grid(True)
plt.savefig('evrate-warmup.pdf')

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV1-GRAN.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-LB-INV1-GRAN-100.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv1-GLRU-100')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV2-GRAN.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-LB-INV2-GRAN-100.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv2-GLRU-100')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB-INV4-GRAN.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GLRU')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-LB-INV4-GRAN-100.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-LA-Inv4-GLRU-100')

# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='lower right', fontsize='14')
plt.grid(True)
# plt.xlim(-10,350)
plt.savefig('evrate-warmup-LB-INV-GE.pdf')
# Plotting code
plt.figure(figsize=(12, 6))
# fig, ax = plt.subplots(figsize=[12,6])

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-LB-0.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='blue', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-0')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-LB-25.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-25')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-LB-50.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-50')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-LB-75.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-75')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-LB-95.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='grey', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-95')

x_values, y_values = read_and_sort_data('report/evset-effective-warmup-skewed_L2_2048x16-s2-LB-100.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Warmup-100')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_2048x16-s2-LB.dat')
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

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_256x64-s2.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-1MB')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_512x64-s2.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-2MB')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_1024x64-s2.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-4MB')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_128x128-s2.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-1MB')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_256x128-s2.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-2MB')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_512x128-s2.dat')
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

# Plotting code
plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_512x64-s2-random.dat')
plt.plot(x_values, y_values, marker='x', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-Ran')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_512x64-s2.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='black', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-LRU')
 
x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_512x64-s2-srrip.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass64-RRIP')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_256x128-s2-random.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='red', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-Ran')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_256x128-s2.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='brown', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-LRU')

x_values, y_values = read_and_sort_data('report/evset-effective-skewed_L2_256x128-s2-srrip.dat')
plt.plot(x_values, y_values, marker='|', markerfacecolor='none', linestyle='-', color='orange', markersize='6', mew='0.2', linewidth='0.5', label='Skew-2-Ass128-RRIP')

# Set labels, title, and save the figure
plt.xlabel('Size of Eviction Sets', fontsize='22')
plt.xticks(fontsize='14')
plt.ylabel('Eviction Rate', fontsize='22')
plt.yticks(fontsize='14')
plt.legend(loc='upper left', fontsize='16')
plt.grid(True)
plt.xlim(-10,300)
plt.savefig('evrate-replacement.pdf')