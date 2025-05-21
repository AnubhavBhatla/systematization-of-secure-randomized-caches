import sys
import subprocess
import re
import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def extract_final_median(file_path):
    # Pattern to match 'Median: <floating point number>'
    pattern = r'Median:\s*(-?\d+\.\d+)'  # Matches optional negative floating point numbers

    final_median = None
    
    # Open the file and process each line
    with open(file_path, 'r') as file:
        for line in file:
            # Search for the pattern in the line
            match = re.search(pattern, line)
            if match:
                # If the pattern is found, update the final median
                final_median = float(match.group(1))
    
    return final_median

def run_command(a1, a2, a3, a4=10000000):
    netEncr = []
    successful_runs = 0
    timeout_seconds = 3600  # 5 minutes timeout, badha dena
    run_count = 0

    while successful_runs < int(a3):
        run_count += 1
        print(f"Attempting run {run_count}, cache config is {a1}...")

        # Construct the command to run
        command = f"./cachefx -c configs/{a1} -v {a2} -m attacker -a occupancy -t probability -g 10000000 -d 100" # 30,000 badha dena

        try:
            # Run the command with a timeout
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True, timeout=timeout_seconds)
            
            # Split the output into lines
            output_lines = result.stdout.splitlines()
            
            # Process the output to find "--encryptions: <Num>"
            found_encryption_line = False
            for line in output_lines:
                words = line.split()  # Split the line based on spaces
                if words and words[0].isdigit():  # Check if line starts with a number
                    for sub_line in output_lines:  # Look for the encryption line
                        if "--encryptions:" in sub_line:
                            encryption_num = int(sub_line.split(":")[1].strip())  # Extract <Num> from "--encryptions: <Num>"
                            print(encryption_num)
                            netEncr.append(encryption_num)
                            found_encryption_line = True
                            break
            
            if found_encryption_line:
                successful_runs += 1
                print(f"Run {run_count} succeeded with encryption.")
                # print("output = ")
                # print(output_lines)
                if (successful_runs % 100 == 0):
                    print(f"Median: {statistics.median(netEncr)}")
            else:
                # print("output was")
                # print(output_lines)
                print(f"Run {run_count} did not contain '--encryptions:' line. Retrying...")

        except subprocess.TimeoutExpired:
            print(f"Run {run_count} timed out after {timeout_seconds} seconds. Retrying...")
        except subprocess.CalledProcessError as e:
            print(f"Error on run {run_count}: {e.stderr}")

        
    # Return the result as netEncr/a3
    print(statistics.stdev(netEncr))
    print(statistics.mean(netEncr))
    return statistics.median(netEncr)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 get-figure.py <1/0: 1 - Use previous results, 0 - Obtain new results> <Figure number>")
        sys.exit(1)
    option = int(sys.argv[1])
    fig_num = int(sys.argv[2])
    if option not in [0, 1]:
        print("Invalid option. Use 1 to use previous results or 0 to obtain new results.")
        sys.exit(1)
    if option == 1:
        report_path = "results-original"
    else:
        report_path = "results"
    if fig_num == 15:
        encryptions_aes = {}
        encryptions_sqmult = {}
        if option == 0:
            # print("Obtaining new results for Figure 15...")
            # run setassoc_rand.xml, ceasers_2.xml, ceasers_16.xml, mirage.xml, skew-2-ass128.xml, sasscache_rand.xml, wpcache_random.xml
            encryptions_aes["SetAssoc"] = run_command("cl256/w16/setassoc_rand.xml", "AES", 10000)
            encryptions_aes["CEASER-S"] = run_command("cl256/w16/ceasers_2.xml", "AES", 10000)
            encryptions_aes["Skew-16"] = run_command("cl256/w16/ceasers_16.xml", "AES", 10000)
            encryptions_aes["Mirage"] = run_command("cl256/w16/mirage.xml", "AES", 10000)
            encryptions_aes["Skew-2-Ass128"] = run_command("cl256/w16/skew-2-ass128.xml", "AES", 10000)
            encryptions_aes["SassCache"] = run_command("cl256/w16/sasscache_rand.xml", "AES", 10000)
            encryptions_aes["Way-based Partitioning"] = 0
            encryptions_sqmult["FA-RR"] = run_command("cl256/assoc_rand.xml", "SquareMult", 10000)
            encryptions_sqmult["SetAssoc"] = run_command("cl256/w16/setassoc_rand.xml", "SquareMult", 10000)
            encryptions_sqmult["CEASER-S"] = run_command("cl256/w16/ceasers_2.xml", "SquareMult", 10000)
            encryptions_sqmult["Skew-16"] = run_command("cl256/w16/ceasers_16.xml", "SquareMult", 10000)
            encryptions_sqmult["Mirage"] = run_command("cl256/w16/mirage.xml", "SquareMult", 10000)
            encryptions_sqmult["Skew-2-Ass128"] = run_command("cl256/w16/skew-2-ass128.xml", "SquareMult", 10000)
            encryptions_sqmult["SassCache"] = run_command("cl256/w16/sasscache_rand.xml", "SquareMult", 10000)
            encryptions_sqmult["Way-based Partitioning"] = 0
            encryptions_sqmult["FA-RR"] = run_command("cl256/assoc_rand.xml", "SquareMult", 10000)
        else:
            # mirage -> mirage_aes_10k_noseed.txt, mirage_sqmult_10k_noseed.txt
            # ceasers_2 -> ceasers_2_aes_10k.txt, ceasers_2_sqmult_10k_noseed.txt
            # setassoc_rand -> setassoc_rand_aes_10k.txt, setassoc_rand_sqmult_10k_noseed.txt
            # ceasers_16 -> ceasers_16_aes_10k_noseed.txt, ceasers_16_sqmult_10k_noseed.txt
            # skew-2-ass128 -> ceasers_2_ass128_aes_10k.txt, ceasers_2_ass128_sqmult_10k_noseed.txt
            # sasscache_rand -> sasscache_rand_aes_10k.txt, sasscache_rand_squaremult_10k.txt
            # FA-RR -> fa_rand_aes_10k.txt, fa_rand_sqmult_10k_noseed.txt
            encryptions_aes["SetAssoc"] = extract_final_median(f"{report_path}/setassoc_rand_aes_10k.txt")
            encryptions_aes["CEASER-S"] = extract_final_median(f"{report_path}/ceasers_2_aes_10k.txt")
            encryptions_aes["Skew-16"] = extract_final_median(f"{report_path}/ceasers_16_aes_10k_noseed.txt")
            encryptions_aes["Mirage"] = extract_final_median(f"{report_path}/mirage_aes_10k_noseed.txt")
            encryptions_aes["Skew-2-Ass128"] = extract_final_median(f"{report_path}/custom_2_ass128_aes_10k_noseed.txt")
            encryptions_aes["SassCache"] = extract_final_median(f"{report_path}/sasscache_rand_aes_10k.txt")
            encryptions_aes["Way-based Partitioning"] = 0
            encryptions_aes["FA-RR"] = extract_final_median(f"{report_path}/fa_rand_aes_10k.txt")
            encryptions_sqmult["SetAssoc"] = extract_final_median(f"{report_path}/setassoc_rand_sqmult_10k_noseed.txt")
            encryptions_sqmult["CEASER-S"] = extract_final_median(f"{report_path}/ceasers_2_sqmult_10k_noseed.txt")
            encryptions_sqmult["Skew-16"] = extract_final_median(f"{report_path}/ceasers_16_sqmult_10k_noseed.txt")
            encryptions_sqmult["Mirage"] = extract_final_median(f"{report_path}/mirage_sqmult_10k_noseed.txt")
            encryptions_sqmult["Skew-2-Ass128"] = extract_final_median(f"{report_path}/ceasers_2_ass128_sqmult_10k_noseed.txt")
            encryptions_sqmult["SassCache"] = extract_final_median(f"{report_path}/sasscache_rand_squaremult_10k.txt")
            encryptions_sqmult["Way-based Partitioning"] = 0
            encryptions_sqmult["FA-RR"] = extract_final_median(f"{report_path}/fa_rand_sqmult_10k_noseed.txt")            
        plt.figure(figsize=(12.5, 7))
        X = ['SetAssoc','CEASER-S', 'Skew-16', 'Mirage', 'Skew-2-Ass128', 'SassCache', 'Way-based Partitioning']
        AES = []
        SqMult = []
        for key in X:
            # print(f"Key: {key}, AES: {encryptions_aes[key]}, SqMult: {encryptions_sqmult[key]}")
            AES.append(encryptions_aes[key]/encryptions_aes["FA-RR"])
            SqMult.append(encryptions_sqmult[key]/encryptions_sqmult["FA-RR"])

        X_axis = np.arange(len(X))

        plt.bar(X_axis - 0.15, AES, 0.3, label = 'AES', color=(0.5, 0.5, 0.8), edgecolor='black', linewidth=2)
        plt.bar(X_axis + 0.15, SqMult, 0.3, label = 'Mod. Exp.', color=(0.2, 0.2, 0.4), edgecolor='black', linewidth=2)

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round', facecolor=(0.5, 0.5, 0.8), edgecolor='black', linewidth=2, alpha=0.2)

        # place a text box in upper left in axes coords
        plt.text(5.97, 0.51, 'Keys not\nDistinguished', fontsize=18,
                ha='center', va='center', bbox=props)

        plt.text(4.7, 1.44, f" {AES[5]:.1f}", fontsize=20,
                ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

        plt.text(5.3, 1.44, f"{SqMult[5]:.1f} ", fontsize=20,
                ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

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
        plt.savefig('figure15.pdf')


        
    elif fig_num == 16:
        encryptions_rr = {}
        encryptions_lru = {}
        if option == 0:
            # print("Obtaining new results for Figure 15...")
            # run setassoc_rand.xml, ceasers_2.xml, ceasers_16.xml, mirage.xml, skew-2-ass128.xml, sasscache_rand.xml, wpcache_random.xml
            encryptions_rr["FA"] = run_command("cl256/assoc_rand.xml", "AES", 10000)
            encryptions_lru["FA"] = run_command("cl256/assoc_lru.xml", "AES", 10000)
            encryptions_rr["SetAssoc"] = run_command("cl256/w16/setassoc_rand.xml", "AES", 10000)
            encryptions_lru["SetAssoc"] = run_command("cl256/w16/setassoc_lru.xml", "AES", 10000)
            encryptions_rr["CEASER-S"] = run_command("cl256/w16/ceasers_2.xml", "AES", 10000)
            encryptions_lru["CEASER-S"] = run_command("cl256/w16/ceasers_2_lru.xml", "AES", 10000)
            encryptions_rr["Skew-2-Ass128"] = run_command("cl256/w16/skew-2-ass128.xml", "AES", 10000)
            encryptions_lru["Skew-2-Ass128"] = run_command("cl256/w16/skew-2-ass128-lru.xml", "AES", 10000)
            encryptions_rr["SassCache"] = run_command("cl256/w16/sasscache_rand.xml", "AES", 10000)
            encryptions_lru["SassCache"] = run_command("cl256/w16/sasscache_lru.xml", "AES", 10000)
        else:
            encryptions_rr["SetAssoc"] = extract_final_median(f"{report_path}/setassoc_rand_aes_10k.txt")
            encryptions_rr["CEASER-S"] = extract_final_median(f"{report_path}/ceasers_2_aes_10k.txt")
            encryptions_rr["Skew-2-Ass128"] = extract_final_median(f"{report_path}/custom_2_ass128_aes_10k_noseed.txt")
            encryptions_rr["SassCache"] = extract_final_median(f"{report_path}/sasscache_rand_aes_10k.txt")
            encryptions_rr["FA"] = extract_final_median(f"{report_path}/fa_rand_aes_10k.txt")
            encryptions_lru["FA"] = extract_final_median(f"{report_path}/fa_lru_aes_10k_noseed.txt")
            encryptions_lru["SetAssoc"] = extract_final_median(f"{report_path}/setassoc_lru_aes_10k_noseed.txt")
            # encryptions_lru["CEASER-S"] = 2257 # CHANGE THIS
            # encryptions_lru["Skew-2-Ass128"] = 1737 # CHANGE THIS
            encryptions_lru["CEASER-S"] = extract_final_median(f"{report_path}/ceasers_2_lru_aes_10k_noseed.txt")
            encryptions_lru["Skew-2-Ass128"] = extract_final_median(f"{report_path}/custom_2_ass128_lru_aes_10k.txt")
            encryptions_lru["SassCache"] = extract_final_median(f"{report_path}/sasscache_lru_aes_10k.txt")

        plt.figure(figsize=(12, 6.3))
        X = ['FA','SetAssoc','CEASER-S', 'Skew-2-Ass128', 'SassCache']
        Random = []
        LRU = []
        for key in X:
            # print(f"Key: {key}, AES: {encryptions_lru[key]}, SqMult: {encryptions_rr[key]}")
            Random.append(encryptions_rr[key])
            LRU.append(encryptions_lru[key])

        X_axis = np.arange(len(X))

        plt.bar(X_axis - 0.15, Random, 0.3, label = 'Ran', color=(0.5, 0.5, 0.8), edgecolor='black', linewidth=2)
        plt.bar(X_axis + 0.15, LRU, 0.3, label = 'LRU', color=(0.2, 0.2, 0.4), edgecolor='black', linewidth=2)

        plt.text(3.72, 9300, f"{Random[4]:.2f}", fontsize=19,
                ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

        plt.text(4.28, 9300, f"{LRU[4]:.2f}", fontsize=19,
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
        plt.savefig('figure16.pdf')
            
        
    else:
        print("Invalid figure number. Use 15 or 16.")
        sys.exit(1)
