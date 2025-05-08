//-----------------------------------------------------------------------------
// File          : generator.cpp
// Author        : Wei Song  <wsong83@gmail.com>
// Created       : 13.09.2015
// Last modified : 13.09.2015
//-----------------------------------------------------------------------------
// Description :
// The base components used by other random generators
//-----------------------------------------------------------------------------
// Copyright (c) 2015 by Wei Song
// License: BSD
//          See LICENSE for more details.
//------------------------------------------------------------------------------
// Modification history :
// 13.09.2015 : created
//-----------------------------------------------------------------------------

#include "random_generator.h"

#include <sys/types.h>
#include <unistd.h>
#include <ctime>
#include <iostream>

// generate a random seed
uint64_t gen_random_seed() {
  time_t t;
  time(&t);
  pid_t pid = getpid();
  uint64_t seed = pid * t;
  std::cout << "Generate random seed " << seed << std::endl;
  return seed;
}

//------------------------------------------------------------------------------
// Various generators used for different randomizers

// generator for 64-bit integer
// length: 2^19937
// storage:  312*sizeof(uint32_t)
boost::random::mt19937_64 gen64;

// set seed for gen64
void set_seed_gen64(uint64_t seed) {
  gen64.seed(seed);
}

// set a random seed for gen64
void random_seed_gen64() { 
  gen64.seed(gen_random_seed());
}

// generator for 32-bit integer
// length: 2^19937
// storage:  625*sizeof(uint32_t)
boost::random::mt19937 gen32;

// set seed for gen32
void set_seed_gen32(uint32_t seed) {
  gen32.seed(seed);
}

// set a random seed for gen32
void random_seed_gen32() {
  gen32.seed(gen_random_seed());
}

// generator for double
// length: ~2^2300000
// storage:  44497*sizeof(double)
boost::random::lagged_fibonacci44497 genDouble;

// set seed for genDouble
void set_seed_gen_double(double seed) {
  genDouble.seed(seed);
}

// set a random seed for genDouble
void random_seed_gen_double() {
  genDouble.seed(gen_random_seed());
}

// generator for float
// length: ~10^171
// storage: 24*sizeof(float)
boost::random::ranlux3_01 genFloat;

// set seed for genFloat
void set_seed_gen_float(float seed) {
  genFloat.seed(seed);
}

// set a random seed for genFloat
void random_seed_gen_float() {
  genFloat.seed(gen_random_seed());
}

