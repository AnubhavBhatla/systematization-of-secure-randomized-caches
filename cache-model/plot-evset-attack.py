import matplotlib.pyplot as plt

def read_and_sort_data(file_path):
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

plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_512x64-s2-116.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='blue', markersize='8', mew='0.5', linewidth='1', label='Skew-2-Ass64-116')

# x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_512x64-s2-LB-122.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='green', markersize='6', mew='0.5', linewidth='1', label='Skew-2-LA-Ass64-122')

x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_256x128-s2-241.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='8', mew='0.5', linewidth='1', label='Skew-2-Ass128-241')

# x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_256x128-s2-LB-244.dat')
# plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='grey', markersize='6', mew='0.5', linewidth='1', label='Skew-2-LA-Ass128-244')

x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_2048x16-s16-87.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='purple', markersize='8', mew='0.5', linewidth='1', label='Skew-16-87')

# plt.title('Plot of different optimizations on top of a 2-skew associative cache')
plt.xlabel('Number of evictions', fontsize='18')
plt.xlim(2*1024*1024,8*1024*1024)
plt.xticks(fontsize='14')
plt.ylabel('Probability of creating the eviction set', fontsize='18')
plt.yticks(fontsize='14')
plt.legend(loc='lower center', fontsize='14')
plt.grid(True)
plt.savefig('evset-attack.pdf')
plt.show()


plt.figure(figsize=(12, 6))

x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_256x64-s2-116.dat')
plt.plot(x_values, y_values, marker='s', markerfacecolor='none', linestyle='-', color='blue', markersize='8', mew='0.5', linewidth='1', label='Skew-2-Ass64-116-1MB')

x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_512x64-s2-116.dat')
plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='green', markersize='8', mew='0.5', linewidth='1', label='Skew-2-Ass64-116-2MB')

x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_1024x64-s2-116.dat')
plt.plot(x_values, y_values, marker='+', markerfacecolor='none', linestyle='-', color='purple', markersize='8', mew='0.5', linewidth='1', label='Skew-2-Ass64-116-4MB')

x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_128x128-s2-241.dat')
plt.plot(x_values, y_values, marker='o', markerfacecolor='none', linestyle='-', color='brown', markersize='8', mew='0.5', linewidth='1', label='Skew-2-Ass128-241-1MB')

x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_256x128-s2-241.dat')
plt.plot(x_values, y_values, marker='v', markerfacecolor='none', linestyle='-', color='grey', markersize='8', mew='0.5', linewidth='1', label='Skew-2-Ass128-241-2MB')

# x_values, y_values = read_and_sort_data('report/evset-attack-skewed_L2_512x128-s2-241.dat')
# plt.plot(x_values, y_values, marker='^', markerfacecolor='none', linestyle='-', color='orange', markersize='8', mew='0.5', linewidth='1', label='Skew-2-Ass128-241-4MB')

# plt.title('Plot of different optimizations on top of a 2-skew associative cache')
plt.xlabel('Number of evictions', fontsize='18')
# plt.xlim(2*1024*1024,8*1024*1024)
plt.xticks(fontsize='14')
plt.ylabel('Probability of creating the eviction set', fontsize='18')
plt.yticks(fontsize='14')
plt.legend(loc='lower center', fontsize='14')
plt.grid(True)
plt.savefig('evset-attack-size.pdf')
plt.show()