### low-occupancy

This tool is used for our experiments involving low-occupancy-based attacks. This correponds to **_Figure 17_** in our paper. The `low-occupancy` directory contains the files and scripts for the experiment for these experiments using our original results only.

> The original source code of this tool can found at: [randomized_caches](https://github.com/SEAL-IIT-KGP/randomized_caches).

Given below is a brief description of the directories in `low-occupancy`
* `configs` contains gem5 config files needed for running programs with either keys.
* `results-original` contains our in-house results for various cache designs and configurations and can be used to easily reproduce plots and tables from the paper.
* `scripts` contains in-house scripts to clone the source code, build it, run various experiments and generate entropy results based on the experiments.