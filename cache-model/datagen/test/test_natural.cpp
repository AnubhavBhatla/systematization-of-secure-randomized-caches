//-----------------------------------------------------------------------------
// File          : test_natural.cpp
// Author        : Wei Song  <wsong83@gmail.com>
// Created       : 15.09.2015
// Last modified : 15.09.2015
//-----------------------------------------------------------------------------
// Description :
// Test the results and speed of natual distributions
//-----------------------------------------------------------------------------
// Copyright (c) 2015 by Wei Song
// License: BSD
//          See LICENSE for more details.
//------------------------------------------------------------------------------
// Modification history :
// 15.09.2015 : created
//-----------------------------------------------------------------------------

#include "test_generator.h"
#include <iostream>
#include <boost/format.hpp>

void test_double_pareto(double alpha, double xM, uint32_t size);
void test_double_pareto_bounded(double alpha, double L, double H, uint32_t size);
void test_double_self_similar(double xM, double h, uint32_t size);
void test_uint_zipfian(uint64_t xM, double theta, uint32_t size);

int main() {
  test_double_pareto(3.1, 1000, 1<<20);
  test_double_pareto_bounded(4.3, 0.01, 1000, 1<<20);
  test_double_self_similar(4294967295, 0.9, 1<<20);
  test_uint_zipfian(1000, 0.7, 1<<20);
}


void test_double_pareto(double alpha, double xM, uint32_t size) {
  std::vector<double> tdata(size);
  
  start_timer();
  for(std::vector<double>::iterator it = tdata.begin(); it != tdata.end(); ++it)
    *it = random_double_pareto(alpha, xM);
  stop_timer();

  std::cout << "random_double_pareto(" << alpha << "," << xM << ") generates " << size << " double in " << timer_span() << " second." << std::endl;
  
  boost::format fn_format("double_pareto_%1%_%2%_%3%.rpt");
  fn_format % alpha % xM % size;
  test_report(fn_format.str().c_str(), tdata);

}

void test_double_pareto_bounded(double alpha, double L, double H, uint32_t size) {
  std::vector<double> tdata(size);
  
  start_timer();
  for(std::vector<double>::iterator it = tdata.begin(); it != tdata.end(); ++it)
    *it = random_double_pareto_bounded(alpha, L, H);
  stop_timer();

  std::cout << "random_double_pareto(" << alpha << "," << L << "," << H << ") generates " << size << " double in " << timer_span() << " second." << std::endl;
  
  boost::format fn_format("double_pareto_%1%_%2%_%3%_%4%.rpt");
  fn_format % alpha % L % H % size;
  test_report(fn_format.str().c_str(), tdata);

}

void test_double_self_similar(double xM, double h, uint32_t size) {
  std::vector<double> tdata(size);
  
  start_timer();
  for(std::vector<double>::iterator it = tdata.begin(); it != tdata.end(); ++it)
    *it = random_double_self_similar(xM, h);
  stop_timer();

  std::cout << "random_double_self_similar(" << xM << "," << h << ") generates " << size << " double in " << timer_span() << " second." << std::endl;
  
  boost::format fn_format("double_self_similar_%1%_%2%_%3%.rpt");
  fn_format % xM % h % size;
  test_report(fn_format.str().c_str(), tdata);

}

void test_uint_zipfian(uint64_t xM, double theta, uint32_t size) {
  std::vector<uint64_t> tdata(size);
  
  start_timer();
  for(std::vector<uint64_t>::iterator it = tdata.begin(); it != tdata.end(); ++it)
    *it = random_uint_zipfian(xM, theta);
  stop_timer();

  std::cout << "random_uint_zipfian(" << xM << "," << theta << ") generates " << size << " double in " << timer_span() << " second." << std::endl;
  
  boost::format fn_format("uint_zipfian_%1%_%2%_%3%.rpt");
  fn_format % xM % theta % size;
  test_report(fn_format.str().c_str(), tdata);

}

