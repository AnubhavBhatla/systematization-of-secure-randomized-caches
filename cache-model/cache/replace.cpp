#include <cstdint>
#include "util/delay.hpp"
#include "cache/definitions.hpp"
#include "cache/replace.hpp"
#include <boost/format.hpp>

///////////////////////////////////////////////////////////////////////////
// THE WHOLE POINT OF THIS FILE IS TO PRINT STUFF /////////////////////////
///////////////////////////////////////////////////////////////////////////

std::string ReplaceFIFO::to_string(int32_t set) const {
  std::string rv;
  if(used_map.count(set)) {
    for(auto w : used_map.at(set)) rv += (boost::format("%1%, ") % w).str();
  }
  rv += "[";
  if(free_map.count(set)) {
    for(auto w : free_map.at(set)) rv += (boost::format(" %1%") % w).str();
  }
  rv += " ]";
  return rv;
}

std::string ReplaceFIFO::to_string() const {
  std::string rv;
  for(int i=0; i<nset; i++) {
    rv += (boost::format("set %1%: ") % i).str();
    rv += to_string(i);
    rv += "\n";
  }
  return rv;
}

std::string ReplaceRRIP::to_string(int32_t set) const {
  std::string rv;
  if(rrpv_map.count(set))
    for(auto w : rrpv_map.at(set)) rv += (boost::format(" %1%") % w).str();
  else
    for(int i=0; i<nway; i++) rv += (boost::format(" %1%") % rrpv_max).str();
  return rv;
}

std::string ReplaceRRIP::to_string() const {
  std::string rv;
  for(int i=0; i<nset; i++) {
    rv += (boost::format("set %1%: ") % i).str();
    rv += to_string(i);
    rv += "\n";
  }
  return rv;
}

std::string ReplacePLRU::to_string(int32_t set) const {
  std::string rv;
    for(int i=0; i<nway; i++) rv += (boost::format(" %1%") % i).str();
  return rv;
}

std::string ReplacePLRU::to_string() const {
  std::string rv;
  for(int i=0; i<nset; i++) {
    rv += (boost::format("set %1%: ") % i).str();
    rv += to_string(i);
    rv += "\n";
  }
  return rv;
}

std::string ReplaceRPLRU::to_string(int32_t set) const {
  std::string rv;
    for(int i=0; i<nway; i++) rv += (boost::format(" %1%") % i).str();
  return rv;
}

std::string ReplaceRPLRU::to_string() const {
  std::string rv;
  for(int i=0; i<nset; i++) {
    rv += (boost::format("set %1%: ") % i).str();
    rv += to_string(i);
    rv += "\n";
  }
  return rv;
}
