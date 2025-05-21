import sys
import subprocess
import statistics

def run_command(a1, a2, a3, a4):
    netEncr = []
    successful_runs = 0
    timeout_seconds = 1000  # 5 minutes timeout, badha dena
    run_count = 0

    while successful_runs < int(a3):
        run_count += 1
        print(f"Attempting run {run_count}, cache config is {a1}...",flush=True)

        # Construct the command to run
        command = f"./cachefx -c configs/{a1} -v {a2} -m attacker -a occupancy -t probability -g 1000000 -d {a4}" # 30,000 badha dena

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
                    print(f"Median: {statistics.median(netEncr)}",flush=True)
            else:
                # print("output was")
                # print(output_lines)
                print(f"Run {run_count} did not contain '--encryptions:' line. Retrying...",flush=True)

        except subprocess.TimeoutExpired:
            print(f"Run {run_count} timed out after {timeout_seconds} seconds. Retrying...",flush=True)
        except subprocess.CalledProcessError as e:
            print(f"Error on run {run_count}: {e.stderr}",flush=True)

        
    # Return the result as netEncr/a3
    print(statistics.stdev(netEncr))
    print(statistics.mean(netEncr))
    return statistics.median(netEncr)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <Cache config, path needed, relative path from folder config (eg cl2048/w16/ceasers_2.xml)> <victim type, eg: AES> <number of iterations>")
        sys.exit(1)

    # Get command-line arguments
    a1 = sys.argv[1]
    a2 = sys.argv[2]
    a3 = sys.argv[3]
    a4 = sys.argv[4]

    # Run the command a3 times and calculate the netEncr/a3
    result = run_command(a1, a2, a3, a4)
    print(f"Final result: {result}")
