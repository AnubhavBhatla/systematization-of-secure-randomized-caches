//-----------------------------------------------------------------------------
// File          : random_generator.h
// Author        : Wei Song  <wsong83@gmail.com>
// Created       : 13.09.2015
// Last modified : 13.09.2015
//-----------------------------------------------------------------------------
// Description :
// Define the interfaces used in testing the Parallel Merging Sorters
//-----------------------------------------------------------------------------
// Copyright (c) 2015 by Wei Song
// License: BSD
//          See LICENSE for more details.
//------------------------------------------------------------------------------
// Modification history :
// 13.09.2015 : created
//-----------------------------------------------------------------------------

#ifndef DG_RANDOM_GENERATOR_H
#define DG_RANDOM_GENERATOR_H

#include <stdint.h>
#include <boost/random/mersenne_twister.hpp>
#include <boost/random/lagged_fibonacci.hpp>
#include <boost/random/ranlux.hpp>

#ifdef __cplusplus
extern "C" {
#endif

//------------------------------------------------------------------------------
// Various generators used for different randomizers

// generator for 64-bit integer
// length: 2^19937
// storage:  312*sizeof(uint32_t)
// Used by:
//   uint_uniform
extern boost::random::mt19937_64 gen64;

// set seed for gen64
void set_seed_gen64(uint64_t);

// set a random seed for gen64
void random_seed_gen64();

// generator for 32-bit integer
// length: 2^19937
// storage:  625*sizeof(uint32_t)
// Used by:
//   uint_poisson
extern boost::random::mt19937 gen32;

// set seed for gen32
void set_seed_gen32(uint32_t);

// set a random seed for gen32
void random_seed_gen32();

// generator for double
// length: ~2^2300000
// storage:  44497*sizeof(double)
// Used by:
//   double_uniform_01
//   double_exponential
//   double_normal
//   double_pareto
//   double_pareto_bounded
//   double_self_similar
//   uint_zipfian
extern boost::random::lagged_fibonacci44497 genDouble;

// set seed for genDouble
void set_seed_gen_double(double);

// set a random seed for genDouble
void random_seed_gen_double();

// generator for float
// length: ~10^171
// storage: 24*sizeof(float)
extern boost::random::ranlux3_01 genFloat;

// set seed for genFloat
void set_seed_gen_float(float);

// set a random seed for genFloat
void random_seed_gen_float();

/* integers in uniform distribution in [min, max]
 * width:    The width of the number produced.
 * min:      The minimal value to be generated.
 * max:      The maximal value to be generated.
 * [speed]   1M numbers in 0.05 sec
 */
uint64_t random_uint_uniform(uint32_t width, uint64_t min, uint64_t max);

/* double in uniform distribution in [0, 1)
 * [speed]   1M numbers in 0.04 sec
 */
double random_double_uniform_01();

/* integers in poisson distribution
 * mean:    The mean of the poisson distribution
 * [speed]   1M numbers poisson(10000) in 0.13 sec
 */
uint32_t random_uint_poisson(double mean);

/* doubles in exponential distribution
 * lambda:   reverse mean
 * [speed]   1M numbers exponential(0.001) in 0.84 sec
 */
double random_double_exponential(double lambda);

/* double in normal distribution
 * mean, sigma
 * [speed]   1M numbers normal(0,100) in 0.15 sec
 */
double random_double_normal(double mean, double sigma);

/* Pareto distribution
 * alpha: define shape
 * xM:    the minimal value, define scale
 * [speed]   1M numbers in 0.11 sec
 */
double random_double_pareto(double alpha, double xM);

/* Pareto bounded distribution
 * alpha: define shape
 * L:     the minimal value
 * H:     the maximal value
 * [speed]   1M numbers in 0.31 sec
 */
double random_double_pareto_bounded(double alpha, double L, double H);

/* Self-similar distribution (Pareto principle)
 * xM:    the maximal value
 * h:     the percentage
 * [speed]   1M numbers in 0.15 sec
 */
double random_double_self_similar(double xM, double h);

/* Zipfian's law
 * xM:    the maximal value
 * theta: 0<theta<1, skew
 * [speed]   1M numbers in 0.63 sec
 */
uint64_t random_uint_zipfian(uint64_t xM, double theta);

#ifdef __cplusplus
}
#endif

#endif

// emacs local variable

// Local Variables:
// mode: C++
// End:
