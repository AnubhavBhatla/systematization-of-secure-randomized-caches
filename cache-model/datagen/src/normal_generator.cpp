//-----------------------------------------------------------------------------
// File          : normal_generator.cpp
// Author        : Wei Song  <wsong83@gmail.com>
// Created       : 14.09.2015
// Last modified : 14.09.2015
//-----------------------------------------------------------------------------
// Description :
// Generate random data comply with normal distribution
//-----------------------------------------------------------------------------
// Copyright (c) 2015 by Wei Song
// License: BSD
//          See LICENSE for more details.
//------------------------------------------------------------------------------
// Modification history :
// 14.09.2015 : created
//-----------------------------------------------------------------------------

#include "random_generator.h"
#include <boost/random/normal_distribution.hpp>
#include <cassert>

/* double in normal distribution
 * mean, sigma
 */
double random_double_normal(double mean, double sigma) {

  // get the random distribution
  boost::random::normal_distribution<double> ranGen(mean, sigma);
  return ranGen(genDouble);
}
