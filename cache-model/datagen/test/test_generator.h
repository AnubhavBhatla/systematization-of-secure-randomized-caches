//-----------------------------------------------------------------------------
// File          : test_generator.h
// Author        : Wei Song  <wsong83@gmail.com>
// Created       : 13.09.2015
// Last modified : 13.09.2015
//-----------------------------------------------------------------------------
// Description :
// Common components for all random tests
// *** Need C++11 support 
//-----------------------------------------------------------------------------
// Copyright (c) 2015 by Wei Song
// License: BSD
//          See LICENSE for more details.
//------------------------------------------------------------------------------
// Modification history :
// 13.09.2015 : created
//-----------------------------------------------------------------------------

#ifndef DG_TEST_GENERATOR_H
#define DG_TEST_GENERATOR_H

#include "random_generator.h"
#include <vector>
#include <fstream>

//-----------------------------------------------------------------------------
// Timer functions

void start_timer();             // start timer
void stop_timer();              // stop timer
double timer_span();            // get the span in seconds

//-----------------------------------------------------------------------------
// test reporting

template<typename T>
inline void test_report(const char *fn, const std::vector<T>& data) {
  std::ofstream hdl(fn);
  for(typename std::vector<T>::const_iterator it = data.begin(); it != data.end(); ++it)
    hdl << *it << std::endl;
  hdl.close();
}


#endif

// emacs local variable

// Local Variables:
// mode: C++
// End:
