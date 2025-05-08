//-----------------------------------------------------------------------------
// File          : test_generator.cpp
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

#include "test_generator.h"
#include <chrono>

//-----------------------------------------------------------------------------
// Timer functions

std::chrono::high_resolution_clock::time_point timer_start, timer_end;

void start_timer() {
  timer_start = std::chrono::high_resolution_clock::now();
}

void stop_timer() {
  timer_end = std::chrono::high_resolution_clock::now();
}

double timer_span() {
  return std::chrono::duration_cast<std::chrono::duration<double>>(timer_end - timer_start).count();
}
