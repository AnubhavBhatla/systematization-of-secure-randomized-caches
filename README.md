# systematization-of-secure-randomized-caches

This repository contains the artifact for "SoK: So, You Think You Know All About Secure Randomized Caches?", to appear at USENIX Security 2025.

We provide various tools in this artifact which can be used to reproduce the results from our paper. We only focus on the figures and tables that include a security analysis of various cache designs. While the paper also studies other characteristics like power and performance, we don't provide tools for those here to keep this artifact focused solely on security. A description of all the tools used and their corresponding experiments can be found below:

### cache-model

This tool is used for our eviction-rate experiments as well as our eviction-set-generation experiments. These correspond to **_Figures 3-14, 18-19, and Table 2_** in our paper. The `cache-model` directory contains the files and scripts required for these experiments.

> The original source code of this tool can found at: [cache-model](https://github.com/comparch-security/cache-model)

### cachefx

This tool is used for our cryptographic attack implementation for occupancy-based attacks. These correspond to **_Figures 15-16_** in our paper. The `cachefx` directory contains the files and scripts required for these experiments.

> The original source code of this tool can found at: [CacheFX](https://github.com/0xADE1A1DE/CacheFX).

### low-occupancy

This tool is used for our experiments involving low-occupancy-based attacks. This correponds to **_Figure 17_** in our paper. The `low-occupancy` directory contains the files and scripts for the experiment for these experiments using our original results only.

> The original source code of this tool can found at: [randomized_caches](https://github.com/SEAL-IIT-KGP/randomized_caches).

---
---

## Table of contents
* [Directory Structure](#directory-structure)
* [Installing dependencies](#installing-dependencies)
* [Building projects](#building-projects)
    * [Build](#build)
    * [Clean](#clean)
* [Generating figures and table](#generating-figures-and-table)
    * [Figures](#figures)
    * [Table](#table)

---
---

## Directory Structure

```
├── cache-model/
│   ├── src files/
│   ├── report/
│   ├── report-original/
│   ├── genFigs.sh
│   ├── get-figure.py
│   ├── get-table.py
│   └── Makefile
├── cachefx/
│   ├── src files
│   ├── results/
│   ├── results-original/
│   ├── genFigs.sh
│   ├── get-figure.py
│   └── Makefile
├── low-occupancy/
│   ├── configs/
│   ├── results-original/
│   ├── scripts/
│   ├── get-figure.py
├── buildAll.sh
├── genAllFigs.sh
├── genTable.sh
├── requirements.txt
├── LICENSE.md
├── README.md
├── .gitignore
└── .gitmodules
```

---
---

## Installing dependencies

Use the following command to install all the python packages required:

```
pip3 install -r requirements.txt
```

We also require the C++ boost library, which can be installed using:

```
sudo apt install libboost-all-dev
```

---
---

## Building projects
### Build

In order to build all required files, use the following script:

```
bash buildAll.sh build
```

---

### Clean
The output files can be cleaned using

```
bash buildAll.sh clean
```

---
---

## Generating figures and table
### Figures

Use the following command to generate all figures using a fresh set of simulations (this may take days to finish):

```
bash genAllFigures.sh 0
```

Instead, we also provide the option to generate figures using our original results:

```
bash genAllFigures.sh 1
```

---

#### Tweak-able options to speed up simulations

We provide user options to change simulation parameters. We relax these parameters by default in this artifact in order to speed up simulations. You may choose to instead change these to get results identical to the paper.

* **Number of threads:** By default, eviction-rate experiments use 100 CPU threads in order to speed up simulations. You may change the `NUM_THREADS` parameter in `cache-model/get-figure.py` based on your system.

* **Samples for eviction set size:** In the paper, we take (for most experiments) 300 samples from 1 to 300 for the eviction set size in eviction-rate experiments. In order to replicate this, you may set the `SKIP` parameter to 1 in `cache-model/get-figure.py`. This value is set to 3 by default.

* **Iterations for cryptographic attacks:** In the paper, we run cryptographic attacks for 100,000 iterations (except for SassCache, which is much slower than other cache designs). However, due to practicality issues, we set this to 1000 iterations using `NUM_ITERATIONS` in `cachefx/get-figure.py`.

---

#### Generating individual figures

We also recommend generating individual figures, multiple at a time, on different systems to parallelize simulations.
In order to plot a single figure, use the following steps:

```
cd <directory: cache-model - For figures 3-14, 18-19; cachefx - For figures 15-16>

python3 get-figure.py <1/0: 1 - Use generated results; 0 - Generate new results and use them> <figure_number>
```

> [!IMPORTANT] 
> **Figure 15:** We do not run the square multiplication victim on SassCache as it is very time consuming to run. We also do not run way-based partitioning configurations here as, according to our simulations of over 10,000,000 encryptions, the keys were not being differentiated.

**Figure 17:** We provide our simulation results to reproduce this figure, which can be done using the following steps:

```
cd low-occupancy/

sudo docker run -it -v $(pwd)/randomized_caches:/home/randomized_caches randomized-caches

cd randomized_cache_hello_world/

bash setup.sh

cd ../

bash buildAES.sh

bash genNumbers.sh

bash getGE.sh

exit

sudo mv randomized_caches/results results

python3 get-figure.py 0
```

> [!IMPORTANT] 
> We do not provide the gem5 code required to reproduce these results. The code has been taken from [here](https://github.com/SEAL-IIT-KGP/randomized_caches/tree/main?tab=readme-ov-file) and we do not make any modifications to it. In order to run the high-associativity configurations used in our paper, use the following command (for 64-way configuration):

```
./build/X86/gem5.opt --outdir ./stats configs/example/spec06_config_multiprogram.py --benchmark=xz --num-cpus=2 --mem-size=8GB --mem-type=DDR4_2400_8x8 --cpu-type TimingSimpleCPU --caches --l2cache --l1d_size=512B --l1i_size=32kB --l2_size=16MB --l1d_assoc=8 --l1i_assoc=8 --l2_assoc=64 --mirage_mode=ceaser --l2_numSkews=2 --l2_TDR=1.75 --l2_EncrLat=3 --prog-interval=300Hz --maxinsts=1000000000 
```

The `--l2_assoc` option can be tweaked to use the 128-way configuration. The remaining steps have been described in the above-mentioned link.

---

### Table

Use the following command to generate Table 2 using a fresh set of simulations (this may take days to finish):

```
bash genTable.sh 0
```

Instead, we also provide the option to generate Table 2 using our original results:

```
bash genTable.sh 1
```

<!-- > [!IMPORTANT]  -->
<!-- > **Table 1:** We do not reproduce it here as it doesn't require any simulations. -->
<!-- > **Table 3:** We do not reproduce it here and we do not provide ChampSim and PCACTI code and configurations. -->

---
---