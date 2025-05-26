import sys
import subprocess
import re
import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
import warnings
import concurrent.futures

warnings.filterwarnings("ignore", category=UserWarning)

NUM_ITERATIONS = 1000

def extract_final_median(file_path):
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
    timeout_seconds = 3600  # 60 minutes timeout, badha dena
    run_count = 0

    while successful_runs < int(a3):
        run_count += 1
        print(f"Attempting run {run_count}, cache config is {a1}...")

        # Construct the command to run
        command = f"./cachefx -c configs/{a1} -v {a2} -m attacker -a occupancy -t probability -g 10000000 -d 100"

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
                if (successful_runs % 100 == 0):
                    print(f"Median: {statistics.median(netEncr)}")
            else:
                print(f"Run {run_count} did not contain '--encryptions:' line. Retrying...")

        except subprocess.TimeoutExpired:
            print(f"Run {run_count} timed out after {timeout_seconds} seconds. Retrying...")
        except subprocess.CalledProcessError as e:
            print(f"Error on run {run_count}: {e.stderr}")

        
    # Return the result as netEncr/a3
    print(statistics.stdev(netEncr))
    print(statistics.mean(netEncr))
    return statistics.median(netEncr)

aes_tasks = [
    ("SetAssoc", "cl256/w16/setassoc_rand.xml"),
    ("CEASER-S", "cl256/w16/ceasers_2.xml"),
    ("Skew-16", "cl256/w16/ceasers_16.xml"),
    ("Mirage", "cl256/w16/mirage.xml"),
    ("Skew-2-Ass128", "cl256/w16/skew-2-ass128.xml"),
    ("SassCache", "cl256/w16/sasscache_rand.xml"),
    ("FA-RR", "cl256/assoc_rand.xml")
]

sqmult_tasks = [
    ("FA-RR", "cl256/assoc_rand.xml"),
    ("SetAssoc", "cl256/w16/setassoc_rand.xml"),
    ("CEASER-S", "cl256/w16/ceasers_2.xml"),
    ("Skew-16", "cl256/w16/ceasers_16.xml"),
    ("Mirage", "cl256/w16/mirage.xml"),
    ("Skew-2-Ass128", "cl256/w16/skew-2-ass128.xml")
]

tasks = [
    ("rr", "FA", "cl256/assoc_rand.xml"),
    ("lru", "FA", "cl256/assoc_lru.xml"),
    ("rr", "SetAssoc", "cl256/w16/setassoc_rand.xml"),
    ("lru", "SetAssoc", "cl256/w16/setassoc_lru.xml"),
    ("rr", "CEASER-S", "cl256/w16/ceasers_2.xml"),
    ("lru", "CEASER-S", "cl256/w16/ceasers_2_lru.xml"),
    ("rr", "Skew-2-Ass128", "cl256/w16/skew-2-ass128.xml"),
    ("lru", "Skew-2-Ass128", "cl256/w16/skew-2-ass128-lru.xml"),
    ("rr", "SassCache", "cl256/w16/sasscache_rand.xml"),
    ("lru", "SassCache", "cl256/w16/sasscache_lru.xml")
]

def task_runner(name, path, algo):
    return name, run_command(path, algo, NUM_ITERATIONS)

def task_runner_rr_lru(target, name, path):
    return target, name, run_command(path, "AES", NUM_ITERATIONS)

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
            with concurrent.futures.ProcessPoolExecutor() as executor:
                # Submit AES tasks
                aes_futures = {executor.submit(task_runner, name, path, "AES"): name for name, path in aes_tasks}
                # Submit SquareMult tasks
                sqmult_futures = {executor.submit(task_runner, name, path, "SquareMult"): name for name, path in sqmult_tasks}

                # Collect AES results
                for future in concurrent.futures.as_completed(aes_futures):
                    name, result = future.result()
                    encryptions_aes[name] = result
                encryptions_aes["Way-based Partitioning"] = 0

                # Collect SquareMult results
                for future in concurrent.futures.as_completed(sqmult_futures):
                    name, result = future.result()
                    encryptions_sqmult[name] = result
                encryptions_sqmult["Way-based Partitioning"] = 0
                encryptions_sqmult["SassCache"] = 2332
        else:
            encryptions_aes["SetAssoc"] = extract_final_median(f"{report_path}/setassoc_rand_aes_10k.txt")
            encryptions_aes["CEASER-S"] = extract_final_median(f"{report_path}/ceasers_2_aes_10k.txt")
            encryptions_aes["Skew-16"] = extract_final_median(f"{report_path}/ceasers_16_aes_10k.txt")
            encryptions_aes["Mirage"] = extract_final_median(f"{report_path}/mirage_aes_10k.txt")
            encryptions_aes["Skew-2-Ass128"] = extract_final_median(f"{report_path}/custom_2_ass128_aes_10k.txt")
            encryptions_aes["SassCache"] = extract_final_median(f"{report_path}/sasscache_rand_aes_10k.txt")
            encryptions_aes["Way-based Partitioning"] = 0
            encryptions_aes["FA-RR"] = extract_final_median(f"{report_path}/fa_rand_aes_10k.txt")
            encryptions_sqmult["SetAssoc"] = extract_final_median(f"{report_path}/setassoc_rand_sqmult_10k.txt")
            encryptions_sqmult["CEASER-S"] = extract_final_median(f"{report_path}/ceasers_2_sqmult_10k.txt")
            encryptions_sqmult["Skew-16"] = extract_final_median(f"{report_path}/ceasers_16_sqmult_10k.txt")
            encryptions_sqmult["Mirage"] = extract_final_median(f"{report_path}/mirage_sqmult_10k.txt")
            encryptions_sqmult["Skew-2-Ass128"] = extract_final_median(f"{report_path}/custom_2_ass128_sqmult_10k.txt")
            encryptions_sqmult["SassCache"] = extract_final_median(f"{report_path}/sasscache_rand_sqmult_10k.txt")
            encryptions_sqmult["Way-based Partitioning"] = 0
            encryptions_sqmult["FA-RR"] = extract_final_median(f"{report_path}/fa_rand_sqmult_10k.txt")            
        plt.figure(figsize=(12.5, 7))
        X = ['SetAssoc','CEASER-S', 'Skew-16', 'Mirage', 'Skew-2-Ass128', 'SassCache', 'Way-based Partitioning']
        AES = []
        SqMult = []
        for key in X:
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
            with concurrent.futures.ProcessPoolExecutor() as executor:
                futures = {executor.submit(task_runner_rr_lru, target, name, path): (target, name)
                        for target, name, path in tasks}

                for future in concurrent.futures.as_completed(futures):
                    target, name, result = future.result()
                    if target == "rr":
                        encryptions_rr[name] = result
                    else:
                        encryptions_lru[name] = result
        else:
            encryptions_rr["SetAssoc"] = extract_final_median(f"{report_path}/setassoc_rand_aes_10k.txt")
            encryptions_rr["CEASER-S"] = extract_final_median(f"{report_path}/ceasers_2_aes_10k.txt")
            encryptions_rr["Skew-2-Ass128"] = extract_final_median(f"{report_path}/custom_2_ass128_aes_10k.txt")
            encryptions_rr["SassCache"] = extract_final_median(f"{report_path}/sasscache_rand_aes_10k.txt")
            encryptions_rr["FA"] = extract_final_median(f"{report_path}/fa_rand_aes_10k.txt")
            encryptions_lru["FA"] = extract_final_median(f"{report_path}/fa_lru_aes_10k.txt")
            encryptions_lru["SetAssoc"] = extract_final_median(f"{report_path}/setassoc_lru_aes_10k.txt")
            encryptions_lru["CEASER-S"] = extract_final_median(f"{report_path}/ceasers_2_lru_aes_10k.txt")
            encryptions_lru["Skew-2-Ass128"] = extract_final_median(f"{report_path}/custom_2_ass128_lru_aes_10k.txt")
            encryptions_lru["SassCache"] = extract_final_median(f"{report_path}/sasscache_lru_aes_10k.txt")

        plt.figure(figsize=(12, 6.3))
        X = ['FA','SetAssoc','CEASER-S', 'Skew-2-Ass128', 'SassCache']
        Random = []
        LRU = []
        for key in X:
            Random.append(encryptions_rr[key])
            LRU.append(encryptions_lru[key])

        X_axis = np.arange(len(X))

        plt.bar(X_axis - 0.15, Random, 0.3, label = 'Ran', color=(0.5, 0.5, 0.8), edgecolor='black', linewidth=2)
        plt.bar(X_axis + 0.15, LRU, 0.3, label = 'LRU', color=(0.2, 0.2, 0.4), edgecolor='black', linewidth=2)

        plt.text(3.72, 9300, f"{Random[4]:.0f}", fontsize=19,
                ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

        plt.text(4.28, 9300, f"{LRU[4]:.0f}", fontsize=19,
                ha='center', va='center', bbox={'facecolor':'white','alpha':1,'edgecolor':'none','pad':1})

        # Set labels, title, and save the figure
        plt.xticks(X_axis, X, rotation=20, ha='right', rotation_mode='anchor')

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
