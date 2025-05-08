//-----------------------------------------------------------------------------
// File          : test_poisson.cpp
// Author        : Wei Song  <wsong83@gmail.com>
// Created       : 14.09.2015
// Last modified : 14.09.2015
//-----------------------------------------------------------------------------
// Description :
// Test the results and speed of poisson distribution
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

void test_uint_poisson(double mean, uint32_t size);
void test_double_exponential(double lambda, uint32_t size);

int main() {
  test_uint_poisson(10000, 1<<20);
  test_double_exponential(0.001, 1<<20);
}

void test_uint_poisson(double mean, uint32_t size) {
  std::vector<uint32_t> tdata(size);
  
  start_timer();
  for(std::vector<uint32_t>::iterator it = tdata.begin(); it != tdata.end(); ++it)
    *it = random_uint_poisson(mean);
  stop_timer();

  std::cout << "random_uint_poisson(" << mean << ") generates " << size << " 32-bit uint in " << timer_span() << " second." << std::endl;
  
  boost::format fn_format("uint32_possion_%1%_%2%.rpt");
  fn_format % mean % size;
  test_report(fn_format.str().c_str(), tdata);

}

void test_double_exponential(double lambda, uint32_t size) {
  std::vector<double> tdata(size);
  
  start_timer();
  for(std::vector<double>::iterator it = tdata.begin(); it != tdata.end(); ++it)
    *it = random_double_exponential(lambda);
  stop_timer();

  std::cout << "random_double_exponential(" << lambda << ") generates " << size << " double in " << timer_span() << " second." << std::endl;
  
  boost::format fn_format("double_exponential_%1%_%2%.rpt");
  fn_format % lambda % size;
  test_report(fn_format.str().c_str(), tdata);

}

