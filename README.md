# systematization-of-secure-randomized-caches

> [!NOTE]
> This repository contains the artifact for "SoK: So, You Think You Know All About Secure Randomized Caches?", to appear at USENIX Security 2025.

---
---

## Table of contents
* [Directory Structure](#directory-structure)
    * [cache-model](#cache-model)
    * [cachefx](#cachefx)
    * [low-occupancy](#low-occupancy)
* [Installing dependencies](#installing-dependencies)
* [Building projects](#building-projects)
    * [Build](#build)
    * [Clean](#clean)
* [Generating figures and tables](#generating-figures-and-tables)
    * [Figures](#figures)
    * [Tables](#tables)

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
│   ├── results-original/
│   ├── get-figure.py
├── buildAll.sh
├── genAllFigs.sh
├── genAllTables.sh
├── requirements.txt
├── LICENSE.md
├── README.md
├── .gitignore
└── .gitmodules
```

### cache-model

This directory contains the files and scripts for the eviction rate experiment and the eviction set generation experiment.

> This code is a modified version of [cache-model](https://github.com/comparch-security/cache-model).

### cachefx

This directory contains the files and scripts for the cryptographic attack experiment for occupancy-based attacks.

> This code is a modified version of [CacheFX](https://github.com/0xADE1A1DE/CacheFX).

### low-occupancy

This directory contains the files and scripts for the experiment for low-occupancy-based attacks using our original results only.

> These files are generated using the source code provided in [randomized_caches](https://github.com/SEAL-IIT-KGP/randomized_caches).

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

### Clean
The output files can be cleaned using

```
bash buildAll.sh clean
```

---
---

## Generating figures and tables
### Figures

Use the following command to generate all figures using a fresh set of simulations (this may take days to finish):

```
bash genAllFigures.sh 0
```

Instead, we also provide the option to generate figures using our original results:

```
bash genAllFigures.sh 1
```

#### Generating individual figures

In order to plot a single figure, use the following steps:

```
cd <directory: cache-model - For figures 3-14 cachefx - For figures 15-16>

python3 get-figure.py <1/0: 1 - Use generated results 0 - Generate new results and use them> <figure_number>
```

**Figure 17:** We provide our simulation results to reproduce this figure, which can be done using the following steps:

```
cd low-occupancy

python3 get-figure.py
```

> [!IMPORTANT] 
> We do not provide the gem5 code required to reproduce these results. The code has been taken from [here](https://github.com/SEAL-IIT-KGP/randomized_caches/tree/main?tab=readme-ov-file) and we do not make any modifications to it. In order to run the high-associativity configurations used in our paper, use the following command (for 64-way configuration):

```
./build/X86/gem5.opt --outdir ./stats configs/example/spec06_config_multiprogram.py --benchmark=xz --num-cpus=2 --mem-size=8GB --mem-type=DDR4_2400_8x8 --cpu-type TimingSimpleCPU --caches --l2cache --l1d_size=512B --l1i_size=32kB --l2_size=16MB --l1d_assoc=8 --l1i_assoc=8 --l2_assoc=64 --mirage_mode=ceaser --l2_numSkews=2 --l2_TDR=1.75 --l2_EncrLat=3 --prog-interval=300Hz --maxinsts=1000000000 
```

> The `--l2_assoc` option can be tweaked to use the 128-way configuration. The remaining steps have been described in the above-mentioned link.

###

---

### Tables

Use the following command to generate all tables using a fresh set of simulations (this may take days to finish):

```
bash genAllTables.sh 0
```

Instead, we also provide the option to generate tables using our original results:

```
bash genAllTables.sh 1
```

> [!IMPORTANT] 
> **Tables 1 and 3:** We do not generate these tables here.

---
---
