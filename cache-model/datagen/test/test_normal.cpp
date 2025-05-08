//-----------------------------------------------------------------------------
// File          : test_poisson.cpp
// Author        : Wei Song  <wsong83@gmail.com>
// Created       : 14.09.2015
// Last modified : 14.09.2015
//-----------------------------------------------------------------------------
// Description :
// Test the results and speed of normal distribution
//-----------------------------------------------------------------------------
// Copyright (c) 2015 by Wei Song
// License: BSD
//          See LICENSE for more details.
//------------------------------------------------------------------------------
// Modification history :
// 14.09.2015 : created
//-----------------------------------------------------------------------------

#include "test_generator.h"
#include <iostream>
#include <boost/format.hpp>

void test_double_normal(double mean, double sigma, uint32_t size);

int main() {
  test_double_normal(0, 1000, 1<<20);
}

void test_double_normal(double mean, double sigma, uint32_t size) {
  std::vector<double> tdata(size);
  
  start_timer();
  for(std::vector<double>::iterator it = tdata.begin(); it != tdata.end(); ++it)
    *it = random_double_normal(mean, sigma);
  stop_timer();

  std::cout << "random_double_normal(" << mean << "," << sigma << ") generates " << size << " double in " << timer_span() << " second." << std::endl;
  
  boost::format fn_format("double_normal_%1%_%2%_%3%.rpt");
  fn_format % mean % sigma % size;
  test_report(fn_format.str().c_str(), tdata);

}

