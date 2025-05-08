DataGen
==========================

A collection of random data generation functions (DPI friendly C++).
Used for generate long sequence of random data to test my sorters.

Reasoning:
The random generation function in current C++/Verilog tools failed to generate data wide and fast enough.

Available distributions:
* uniform
* exponential
* poisson
* guass (normal)
* pareto
* self-similar
* Zipf

Requirement
* Boost Random Library
* C++ 11 support