import sys
import subprocess
import re
import statistics
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

def run_command(a1, a2, a3, a4=10000000):
    netEncr = []
    successful_runs = 0
    timeout_seconds = 1000  # 5 minutes timeout, badha dena
    run_count = 0

    while successful_runs < int(a3):
        run_count += 1
        print(f"Attempting run {run_count}, cache config is {a1}...",flush=True)

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
                print(f"Run {run_count} succeeded with encryption.",flush=True)
                # print("output = ")
                # print(output_lines)
                if (successful_runs % 100 == 0):
                    print(f"Median: {statistics.median(netEncr)}")
            else:
                # print("output was")
                # print(output_lines)
                print(f"Run {run_count} did not contain '--encryptions:' line. Retrying...",flush=True)

        except subprocess.TimeoutExpired:
            print(f"Run {run_count} timed out after {timeout_seconds} seconds. Retrying...",flush=True)
        except subprocess.CalledProcessError as e:
            print(f"Error on run {run_count}: {e.stderr}",flush=True)

        
    # Return the result as netEncr/a3
    print(statistics.stdev(netEncr),flush=True)
    print(statistics.mean(netEncr),flush=True)
    return statistics.median(netEncr)

encryptions_rr = {}
encryptions_lru = {}
encryptions_aes = {}
encryptions_sqmult = {}

# encryptions_aes["SetAssoc"] = run_command("cl256/w16/setassoc_rand.xml", "AES", 10000)
# encryptions_aes["CEASER-S"] = run_command("cl256/w16/ceasers_2.xml", "AES", 10000)
# encryptions_aes["Skew-16"] = run_command("cl256/w16/ceasers_16.xml", "AES", 10000)
# encryptions_aes["Mirage"] = run_command("cl256/w16/mirage.xml", "AES", 10000)
# encryptions_aes["Skew-2-Ass128"] = run_command("cl256/w16/skew-2-ass128.xml", "AES", 10000)
# encryptions_aes["SassCache"] = run_command("cl256/w16/sasscache_rand.xml", "AES", 10000)
# encryptions_aes["Way-based Partitioning"] = 0
# encryptions_sqmult["FA-RR"] = run_command("cl256/assoc_rand.xml", "SquareMult", 10000)
# encryptions_sqmult["SetAssoc"] = run_command("cl256/w16/setassoc_rand.xml", "SquareMult", 10000)
# encryptions_sqmult["CEASER-S"] = run_command("cl256/w16/ceasers_2.xml", "SquareMult", 10000)
# encryptions_sqmult["Skew-16"] = run_command("cl256/w16/ceasers_16.xml", "SquareMult", 10000)
# encryptions_sqmult["Mirage"] = run_command("cl256/w16/mirage.xml", "SquareMult", 10000)
# encryptions_sqmult["Skew-2-Ass128"] = run_command("cl256/w16/skew-2-ass128.xml", "SquareMult", 10000)
# encryptions_sqmult["SassCache"] = run_command("cl256/w16/sasscache_rand.xml", "SquareMult", 10000)
# encryptions_sqmult["Way-based Partitioning"] = 0
# encryptions_sqmult["FA-RR"] = run_command("cl256/assoc_rand.xml", "SquareMult", 10000)

# encryptions_rr["FA"] = run_command("cl256/assoc_rand.xml", "AES", 10000)
# encryptions_lru["FA-LRU"] = run_command("cl256/assoc_lru.xml", "AES", 10000)
# encryptions_rr["SetAssoc"] = run_command("cl256/w16/setassoc_rand.xml", "AES", 10000)
# encryptions_lru["SetAssoc"] = run_command("cl256/w16/setassoc_lru.xml", "AES", 10000)
# encryptions_rr["CEASER-S"] = run_command("cl256/w16/ceasers_2.xml", "AES", 10000)
# encryptions_lru["CEASER-S"] = run_command("cl256/w16/ceasers_2_lru.xml", "AES", 10000)
# encryptions_rr["Skew-2-Ass128"] = run_command("cl256/w16/skew-2-ass128.xml", "AES", 10000)
# encryptions_lru["Skew-2-Ass128"] = run_command("cl256/w16/skew-2-ass128-lru.xml", "AES", 10000)
# encryptions_rr["SassCache"] = run_command("cl256/w16/sasscache_rand.xml", "AES", 10000)
encryptions_lru["SassCache"] = run_command("cl256/w16/sasscache_lru.xml", "AES", 10000)

print("random repl: ", encryptions_rr,flush=True)
print("lru repl: ", encryptions_lru,flush=True)
print("aes: ",encryptions_aes,flush=True)
print("sqmult: ",encryptions_sqmult,flush=True)
# print(encryptions_rr, encryptions_lru)

