import numpy as np
import matplotlib.pyplot as plt
import sys
from collections import defaultdict
import scipy.stats as stats
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

def process_ge_data(file_name):
    # Initialize a defaultdict to accumulate the GEs for each trace count
    trace_dict = defaultdict(list)

    # Open the file and process each line
    with open(file_name, 'r') as file:
        for line in file:
            # Extract trace count and GE value using string manipulation
            parts = line.strip().split(":")
            if len(parts) < 2:
                continue  # Skip malformed lines
            
            trace_part = parts[0].strip()
            ge_part = parts[1].strip().split(" ")[-1]  # Extract the GE value
            try:
                trace_count = int(trace_part.split()[1])  # Extract the trace count as an integer
                ge_value = float(ge_part)  # Convert GE to float
            except ValueError:
                continue  # Skip lines with invalid trace count or GE value
            
            # Append the GE value to the list corresponding to the trace count
            trace_dict[trace_count].append(ge_value)

    # Convert defaultdict to a regular dict (optional)
    return dict(trace_dict)

def calculate_mean_and_confidence_interval(data):
    # Calculate the mean
    mean = np.mean(data)

    # Calculate the standard deviation
    std_dev = np.std(data, ddof=1)  # Using ddof=1 to get the sample standard deviation

    # Calculate the standard error of the mean
    sem = std_dev / np.sqrt(len(data))

    # Z-value for 90% confidence interval (for a two-tailed test, the 5% on each side)
    z_value = stats.norm.ppf(0.95)

    # Calculate the margin of error
    margin_of_error = z_value * sem

    # Calculate the 90% confidence interval
    confidence_interval = (mean,mean - margin_of_error, mean + margin_of_error)
    return confidence_interval


def plot_guessing_entropy_vs_observations(data):
    # Create a figure for the plot
    plt.figure(figsize=(12, 6))

    # Iterate over each configuration type
    for config_type, config_data in data.items():
        # Extract the number of observations and the corresponding mean values
        num_observations = list(config_data.keys())
        mean_guessing_entropy = [config_data[obs][0] for obs in num_observations]

        # Plotting the mean guessing entropy without error bars
        plt.plot(num_observations, mean_guessing_entropy, label=config_type, marker='o')

    # Label the axes
    plt.xlabel('Number of Observations', fontsize=24)
    plt.ylabel('Guessing Entropy', fontsize=24)
    # plt.title('Guessing Entropy vs Number of Observations for Different Cache Configurations')

    # Add a legend to distinguish between different config types
    plt.legend(fontsize=14, loc='lower right')

    # Show the plot
    plt.grid(True)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    
    # Save the plot as a PDF
    plt.savefig("figure17.pdf")


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print("Usage: python get-figure.py")
        print("We do not support generating new results. The figure is generated using the original results.")
        exit(1)

    plotter = {}
    keys = ['CEASER-S','Mirage','SassCache','Skew-16', 'Skew-2-Ass64', 'Skew-2-Ass128']
    files = ['results-original/GE_ceasers.txt','results-original/GE_mirage.txt','results-original/GE_sass.txt','results-original/GE_scatter.txt','results-original/GE_skew-2-ass64.txt', 'results-original/GE_skew-2-ass128.txt']
    for i in range(len(keys)):
        tmp = process_ge_data(files[i])
        plotter[keys[i]] = {}
        for key in tmp.keys():
            plotter[keys[i]][key] = calculate_mean_and_confidence_interval(tmp[key])
    plot_guessing_entropy_vs_observations(plotter)


