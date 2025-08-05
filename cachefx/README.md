# cachefx

This tool is used for our cryptographic attack implementation for occupancy-based attacks. These correspond to **_Figures 15-16_** in our paper. The `cachefx` directory contains the files and scripts required for these experiments.

> The original source code of this tool can found at: [CacheFX](https://github.com/0xADE1A1DE/CacheFX).

Given below is a brief description of the directories in `cachefx`
* `Attacker` represents code for the different attacker variants such as occupancy-based and eviction-based attackers.
* `Cache` contains code for various cache designs and can be updated to add any additional design implementations.
* `configs` represents a variety of configurations of designs defined in `Cache`.
* `crypto` contains code for cryptographic cipher implementations such as speck and qarma-64.
* `include` contains all header files. You may need to update files here accordingly while updating or creating any new source files.
* `MMU` represents code for the memory management unit.
* `PlaintextKeyPairGenerator` contains important code for key-based encryptions.
* `Profiling` contains complementary code for profiling.
* `results-original` contains our in-house results for various cache designs and configurations and can be used to easily reproduce plots and tables from the paper.
* `Victim` represents code for the different victim variants such as AES and SquareMult.