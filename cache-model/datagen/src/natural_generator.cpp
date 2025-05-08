//-----------------------------------------------------------------------------
// File          : natural_generator.cpp
// Author        : Wei Song  <wsong83@gmail.com>
// Created       : 14.09.2015
// Last modified : 14.09.2015
//-----------------------------------------------------------------------------
// Description :
// Generate random data comply with distribution mimic nature
//-----------------------------------------------------------------------------
// Copyright (c) 2015 by Wei Song
// License: BSD
//          See LICENSE for more details.
//------------------------------------------------------------------------------
// Modification history :
// 14.09.2015 : created
//-----------------------------------------------------------------------------

#include "random_generator.h"
#include <cmath>
#include <map>
#include <cassert>
#include <cstdio>

/* Pareto distribution
 * alpha: define shape
 * xM:    the minimal value, define scale
 */
double random_double_pareto(double alpha, double xM) {
  assert(alpha > 0);
  assert(xM > 0);

  double v = random_double_uniform_01();
  while(v == 0) { v = random_double_uniform_01(); }

  return xM / pow(v, 1/alpha);
}

/* Pareto bounded distribution
 * alpha: define shape
 * L:     the minimal value
 * H:     the maximal value
 */
double random_double_pareto_bounded(double alpha, double L, double H) {
  assert(alpha > 0);
  assert(L > 0);
  assert(H > L);

  double u = random_double_uniform_01();
  while(u == 0) { u = random_double_uniform_01(); }

  double x = -(u*pow(H,alpha)-u*pow(L,alpha)-pow(H,alpha)) / (pow(H*L,alpha));
  
  return pow(x, -1.0/alpha);
}

/* Self-similar distribution (Pareto principle)
 * xM:    the maximal value
 * h:     0<h<1, the percentage
 */
double random_double_self_similar(double xM, double h) {
  assert(xM >0);
  assert(h > 0);
  assert(h < 1);

  return 1 + xM * pow(random_double_uniform_01(), log(h)/log(1.0 - h));
}


namespace {
  // helper for zipfian
  std::map<uint64_t, std::map<double, double> > zeta_cache;
  double zeta(uint64_t xM, double theta) {
    if(zeta_cache.count(xM) && zeta_cache[xM].count(theta))
      return zeta_cache[xM][theta];

    double v = 0;
    double v_step_pre = 0;
    double v_step = 0;
    uint64_t index = 1;
    uint64_t i_step = 1;
    double delta = 0;
    double delta_th = 0.0001;
    while(index <= xM) {
      v_step_pre = v_step;
      v_step = pow((double)(index), -theta);
      delta = v_step_pre - v_step;
      v += v_step * i_step + delta * 0.5 * (i_step - 1);
      if(delta < delta_th) {
        i_step *= 8;
        delta_th /= 20.0;
      }

      if(i_step == 1 || index + i_step <= xM || index == xM)
        index += i_step;
      else {
        i_step = xM - index;
        index = xM;
      }      
    }

    zeta_cache[xM][theta] = v;
    return v;
  }

  std::map<uint64_t, std::map<double, double> > eta_cache;
  double eta(uint64_t xM, double theta) {
    if(eta_cache.count(xM) && eta_cache[xM].count(theta))
      return eta_cache[xM][theta];

    double v = (1.0 - pow((2.0/xM), (1.0-theta))) / 
               (1.0 - zeta(2,theta)/zeta(xM, theta));

    eta_cache[xM][theta] = v;
    return v;
  }
}

/* Zipfian's law
 * xM:    the maximal value
 * theta: 0<theta<1, skew
 */
uint64_t random_uint_zipfian(uint64_t xM, double theta) {
  assert(theta > 0);
  assert(theta < 1);
  assert(xM > 0);
  assert(xM < 0xefffffffffffffff);

  double alpha = 1.0 / (1.0 - theta);
  double u = random_double_uniform_01();
  double uz = u * zeta(xM, theta);

  if(uz < 1.0)
    return 1;
  else if(uz < 1.0 + pow(0.5, theta))
    return 2;
  else
    return (uint64_t)(xM * pow(eta(xM, theta) * (u - 1.0) + 1.0, alpha)); 
}
  
