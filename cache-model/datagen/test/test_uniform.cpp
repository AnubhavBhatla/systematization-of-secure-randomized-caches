//-----------------------------------------------------------------------------
// File          : test_uniform.cpp
// Author        : Wei Song  <wsong83@gmail.com>
// Created       : 13.09.2015
// Last modified : 13.09.2015
//-----------------------------------------------------------------------------
// Description :
// Test the results and speed of random uniform distribution
//-----------------------------------------------------------------------------
// Copyright (c) 2015 by Wei Song
// License: BSD
//          See LICENSE for more details.
//------------------------------------------------------------------------------
// Modification history :
// 13.09.2015 : created
//-----------------------------------------------------------------------------

#include "test_generator.h"
#include <iostream>
#include <boost/format.hpp>

void test_uint_uniform(uint32_t width, uint32_t size);
void test_double_uniform_01(uint32_t size);


int main() {
  test_uint_uniform(64, 1<<20);
  test_double_uniform_01(1<<20);
}

void test_uint_uniform(uint32_t width, uint32_t size) {
  std::vector<uint64_t> tdata(size);
  
  start_timer();
  for(std::vector<uint64_t>::iterator it = tdata.begin(); it != tdata.end(); ++it)
    *it = random_uint_uniform(width, 0, (uint64_t)(1) << 63);
  stop_timer();

  std::cout << "random_uint_uniform() generates " << size << " " << width << "-bit uint in " << timer_span() << " second." << std::endl;
  
  boost::format fn_format("uint%1%_uniform_%2%.rpt");
  fn_format % width % size;
  test_report(fn_format.str().c_str(), tdata);

}

void test_double_uniform_01(uint32_t size){
  std::vector<double> tdata(size);
  
  start_timer();
  for(std::vector<double>::iterator it = tdata.begin(); it != tdata.end(); ++it)
    *it = random_double_uniform_01();
  stop_timer();

  std::cout << "random_double_uniform_01() generates " << size << " double in " << timer_span() << " second." << std::endl;
  
  boost::format fn_format("double_uniform_01_%1%.rpt");
  fn_format % size;
  test_report(fn_format.str().c_str(), tdata);

}
