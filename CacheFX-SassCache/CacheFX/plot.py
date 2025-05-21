import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

plt.figure(figsize=(12.5, 7))

# X = ['FA','SetAssoc','CEASER','CEASER-S','Mirage','Skew-2-Ass128','Skew-2-LA-Inv2-GRan']
X = ['SetAssoc','CEASER-S', 'Skew-16', 'Mirage', 'Skew-2-Ass128', 'SassCache', 'Way-based Partitioning']
AES = [5372/6027.0, 6331/6027.0, 6112/6027.0, 5872/6027.0, 6135/6027.0, 99400/6027.0, 0]
SqMult = [46/74.0, 80/74.0, 76/74.0, 72/74.0, 74/74.0, 2647/74.0, 0]

X_axis = np.arange(len(X))

plt.bar(X_axis - 0.15, AES, 0.3, label = 'AES', color=(0.5, 0.5, 0.8), edgecolor='black', linewidth=2)
plt.bar(X_axis + 0.15, SqMult, 0.3, label = 'Mod. Exp.', color=(0.2, 0.2, 0.4), edgecolor='black', linewidth=2)

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor=(0.5, 0.5, 0.8), edgecolor='black', linewidth=2, alpha=0.2)

# place a text box in upper left in axes coords
plt.text(5.97, 0.51, 'Keys not\nDistinguished', fontsize=18,
        ha='center', va='center', bbox=props)

# plt.text(4.75, 1.435, '6.90', fontsize=14,
        # ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

# plt.text(5.25, 1.435, 'x.xx', fontsize=14,
        # ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

plt.text(4.7, 1.44, '10.71', fontsize=20,
        ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

plt.text(5.3, 1.44, '31.5', fontsize=20,
        ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

# plt.text(6.75, 1.435, '16.78', fontsize=14,
        # ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

# plt.text(7.25, 1.435, 'x.xx', fontsize=14,
        # ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

# Set labels, title, and save the figure
plt.xticks(X_axis, X, rotation=20, ha='right', rotation_mode='anchor')
# plt.xlabel('Cache Design', fontsize='22')
plt.xticks(fontsize='22')
plt.ylabel('Normalized encryptions', fontsize='28')
plt.yticks(fontsize='18')
plt.legend(loc='upper left', fontsize='20')
plt.grid(axis='y')
plt.gca().set_axisbelow(True)
plt.ylim(0.4,1.4)
plt.savefig('occupancy.pdf')

plt.figure(figsize=(12, 6.3))

# X = ['FA','SetAssoc','CEASER','CEASER-S','Mirage','Skew-2-Ass128','Skew-2-LA-Inv2-GRan'] 
X = ['FA','SetAssoc','CEASER-S', 'Skew-2-Ass128', 'SassCache']
Random = [6027, 5372, 6331, 6135, 94422]
LRU = [832, 862, 1174, 862, 94379]

X_axis = np.arange(len(X))

plt.bar(X_axis - 0.15, Random, 0.3, label = 'Ran', color=(0.5, 0.5, 0.8), edgecolor='black', linewidth=2)
plt.bar(X_axis + 0.15, LRU, 0.3, label = 'LRU', color=(0.2, 0.2, 0.4), edgecolor='black', linewidth=2)

plt.text(3.72, 9300, '64739', fontsize=19,
        ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

plt.text(4.28, 9300, '68479', fontsize=19,
        ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

# Set labels, title, and save the figure
plt.xticks(X_axis, X, rotation=20, ha='right', rotation_mode='anchor')

# plt.xlabel('Cache Design', fontsize='22')
plt.xticks(fontsize='22')
plt.ylabel('Number of encryptions', fontsize='27')
plt.yticks(fontsize='16')
plt.legend(loc='upper left', fontsize='20')
plt.grid(axis='y')
plt.gca().set_axisbelow(True)
plt.ylim(0,9000)
plt.savefig('occupancy-replacement.pdf')