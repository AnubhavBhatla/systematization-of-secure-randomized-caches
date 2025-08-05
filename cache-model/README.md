# cache-model

This tool is used for our eviction-rate experiments as well as our eviction-set-generation experiments. These correspond to **_Figures 3-14, 18-19, and Table 2_** in our paper. The `cache-model` directory contains the files and scripts required for these experiments.

> The original source code of this tool can found at: [cache-model](https://github.com/comparch-security/cache-model)

Given below is a brief description of the directories in `cache-model`

* `attack` contains code required for eviction set creation and search.
* `cache` contains code for various cache designs and associated files for indexing, replacement policy etc. These files can be updated to append a new cache design (both skewed and unskewed designs are supported).
* `config` contains .json files to create various cache configurations as needed. These json files can be edited to create any new combinations using existing designs defined in `cache`.
* `datagen` is a sub-repository which contains code required for random number generation, needed for attack algorithms.
* `report-original` contains our in-house results for various cache designs and configurations and can be used to easily reproduce plots and tables from the paper.
* `test` contains code for both eviction set creation algorithms and using eviction sets to measure eviction rate. These files can be updated to add any additional attack experiments.
* `util` contains code which complements various functions such as measuring statistics, cache queries etc.