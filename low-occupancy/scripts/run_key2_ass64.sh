#!/bin/bash

export BASE_DIR=/home/randomized_caches

# Define the command to run
COMMAND="../../../ceaser/perf_analysis/gem5/build/X86/gem5.opt --outdir ./stats/ ../../../ceaser-s/perf_analysis/gem5/configs/example/spec06_config_multiprogram_key2.py --num-cpus=1 --mem-size=8GB --mem-type=DDR4_2400_8x8 --cpu-type TimingSimpleCPU --caches --l2cache --l1d_size=512B --l1i_size=32kB --l2_size=16MB --l1d_assoc=8 --l1i_assoc=8 --l2_assoc=64 --mirage_mode=ceaser --l2_numSkews=2 --l2_TDR=1.75 --l2_EncrLat=3 --prog-interval=300Hz"

# Number of times to run the command
RUNS=400

# Create run directories
mkdir -p key1
mkdir -p key2

# Output file to store lines containing "Attacker"
OUTPUT_FILE="key2/timing_values_run_$1"

# Clear the output file before starting
> "$OUTPUT_FILE"

# Run the command multiple times
for ((i = 1; i <= RUNS; i++)); do
    echo "Running Skew-2-Ass64... key2... file$1... iteration $i..."

    # Execute the command and capture both stdout and stderr
    OUTPUT=$($COMMAND 2>&1)

    # Check if command ran successfully
    if [ $? -ne 0 ]; then
        echo "Error running command on iteration $i"
        echo "Output was: $OUTPUT"
        continue
    fi

    # Extract lines containing "Attacker" (case-sensitive)
    echo "$OUTPUT" | grep "Attacker" >> "$OUTPUT_FILE"
done

echo "Done. Extracted lines are saved to skew-2-ass64/$OUTPUT_FILE."