#ifndef CM_REPLACE_HPP_
#define CM_REPLACE_HPP_

#include <unordered_map>
#include <list>
#include <vector>
#include <unordered_set>
#include <functional>
#include <string>
#include "util/random.hpp"
#include <algorithm>
#include <iostream>
#include <math.h>
#include <unistd.h>

///////////////////////////////////
// Base class

class ReplaceFuncBase : public DelaySim
{
protected:
  uint32_t nset, nway, INVALID_WAYS_PER_SKEW;
  bool GLOBAL_LRU, GLOBAL_RANDOM;
public:
  ReplaceFuncBase(uint32_t nset, uint32_t nway, uint32_t delay, uint32_t INVALID_WAYS_PER_SKEW, bool GLOBAL_RANDOM, bool GLOBAL_LRU)
    : DelaySim(delay), nset(nset), nway(nway), INVALID_WAYS_PER_SKEW(INVALID_WAYS_PER_SKEW), GLOBAL_LRU(GLOBAL_LRU), GLOBAL_RANDOM(GLOBAL_RANDOM) {
    }
  virtual uint32_t replace(uint64_t *latency, int32_t set) = 0;
  virtual void access(int32_t set, uint32_t way) = 0;
  virtual void invalid(int32_t set, uint32_t way) = 0;
  virtual uint32_t count(int32_t set) = 0;
  virtual std::string to_string(int32_t set) const = 0;
  virtual std::string to_string() const = 0;
  virtual ~ReplaceFuncBase() {}
};

///////////////////////////////////
// Random replacement

class ReplaceRandom : public ReplaceFuncBase
{
  std::unordered_map<uint32_t, std::unordered_set<uint32_t> > free_map;
public:
  ReplaceRandom(uint32_t nset, uint32_t nway, uint32_t delay) : ReplaceFuncBase(nset, nway, delay,0,0,0) {}
  virtual uint32_t replace(uint64_t *latency, int32_t set){
    // add latency
    latency_acc(latency);
    // if the set does not exist in the free map, insert all its ways
    if(!free_map.count(set)) {
      for(uint32_t i=0; i<nway; i++) free_map[set].insert(i);
    }

    // if the set has some element in the free map (invalid entry), return the first element, otherwise return a random way
    if(free_map[set].size() > 0)
      return *(free_map[set].begin());
    else
      return (uint32_t)get_random_uint64(nway);
  }
  virtual void access(int32_t set, uint32_t way) {
    // if way is present in the free map, remove it
    if(free_map[set].count(way))
      free_map[set].erase(way);
  }
  virtual void invalid(int32_t set, uint32_t way) {
    // insert the newly invalidated way into the free map
    free_map[set].insert(way);
  }
  virtual uint32_t count(int32_t set) {
    // calculate the number of valid ways
    if (!free_map.count(set)) {
      return 0;
    }
    else {
      return nway - free_map[set].size();
    }
  }

  // there is not need to print for random replacement
  virtual std::string to_string(int32_t set) const { return std::string(); }
  virtual std::string to_string() const { return std::string(); }

  virtual ~ReplaceRandom() {}

  static ReplaceFuncBase *factory(uint32_t nset, uint32_t nway, uint32_t delay) {
    return (ReplaceFuncBase *)(new ReplaceRandom(nset, nway, delay));
  }

  static replacer_creator_t gen(uint32_t delay = 0) {
    using namespace std::placeholders;
    return std::bind(factory, _1, _2, delay);
  }
};

///////////////////////////////////
// FIFO replacement

class ReplaceFIFO : public ReplaceFuncBase
{
protected:
  std::unordered_map<uint32_t, std::list<uint32_t> > used_map;
  std::unordered_map<uint32_t, std::unordered_set<uint32_t> > free_map;
  std::list<std::tuple<int32_t, uint32_t>> used_map_global;
  int numSAE = 0;

public:

  ReplaceFIFO(uint32_t nset, uint32_t nway, uint32_t delay, uint32_t INVALID_WAYS_PER_SKEW, bool GLOBAL_RANDOM, bool GLOBAL_LRU) : ReplaceFuncBase(nset, nway, delay, INVALID_WAYS_PER_SKEW,GLOBAL_RANDOM,GLOBAL_LRU) {
  }

  virtual uint32_t replace(uint64_t *latency, int32_t set) {
    // add latency
    latency_acc(latency);
    // if the set does not exist in the free map, insert all its ways
    if(!free_map.count(set)) {
      for(uint32_t i=0; i<nway; i++) free_map[set].insert(i);
    }

    // count the number of valid entries in the cache
    uint64_t valid_count = 0;
    for (int32_t i = 0; i < nset; i++) {
      if (free_map.count(i)) {
        valid_count += (nway - free_map[i].size());
      }
    }
    // if the cache is not at full capacity (only valid ways), return an invalid way from the set or perform an SAE
    // perform an SAE if the given set is already full, otherwise assign an invalid entry from this set and globally evict a random entry
    if (free_map[set].size() < 1) {
      numSAE++;
      return used_map[set].front();
    }
    else {
      if (valid_count < (nset*(nway-INVALID_WAYS_PER_SKEW))) {
        return *(free_map[set].begin());
      }
      else {
        if (GLOBAL_RANDOM && GLOBAL_LRU) {
          std::cerr<<"Please only use global random OR global LRU eviction, otherwise the global LRU will overwrite global Random "<<INVALID_WAYS_PER_SKEW<<"\n";
          exit(0);
        }
        if (GLOBAL_RANDOM)
        {
          uint32_t rand_set = nset;
          while (!used_map[rand_set].size()) {
            rand_set = (uint32_t)get_random_uint64(nset);
          }

          uint32_t rand_way = nway;
          while (std::find(used_map[rand_set].begin(), used_map[rand_set].end(), rand_way) == used_map[rand_set].end()) {
            rand_way = (uint32_t)get_random_uint64(nway);
          }
          
          used_map[rand_set].remove(rand_way);
          free_map[rand_set].insert(rand_way);
        }

        if (GLOBAL_LRU)
        {
          int32_t lru_set = std::get<0>(used_map_global.front());
          uint32_t lru_way = std::get<1>(used_map_global.front());
          used_map_global.remove(std::make_tuple(lru_set,lru_way));
          used_map[lru_set].remove(lru_way);
          free_map[lru_set].insert(lru_way);
        }
        
        return *(free_map[set].begin());
      }
    }
  }

  virtual void access(int32_t set, uint32_t way) {
    // if way is present in the free map, remove it, and add to the used map
    if(free_map[set].count(way)) {
      free_map[set].erase(way);
      used_map[set].push_back(way);
      used_map_global.push_back(std::make_tuple(set,way));
    }
  }

  virtual void invalid(int32_t set, uint32_t way) {
    // insert the newly invalidated way into the free map and remove from used map
    used_map[set].remove(way);
    free_map[set].insert(way);
    used_map_global.remove(std::make_tuple(set,way));
  }

  virtual uint32_t count(int32_t set) {
    // calculate the number of valid ways
    if (!free_map.count(set)) {
      return 0;
    }
    else {
      return nway - free_map[set].size();
    }
  }

  virtual std::string to_string(int32_t set) const;
  virtual std::string to_string() const;
  virtual ~ReplaceFIFO() {
  }

  static ReplaceFuncBase *factory(uint32_t nset, uint32_t nway, uint32_t delay,uint32_t INVALID_WAYS_PER_SKEW, bool GLOBAL_RANDOM, bool GLOBAL_LRU) {
    return (ReplaceFuncBase *)(new ReplaceFIFO(nset, nway, delay,INVALID_WAYS_PER_SKEW,GLOBAL_RANDOM,GLOBAL_LRU));
  }

  static replacer_creator_t gen(uint32_t delay = 0,uint32_t INVALID_WAYS_PER_SKEW=0, bool GLOBAL_RANDOM=0, bool GLOBAL_LRU=0) {
    using namespace std::placeholders;
    return std::bind(factory, _1, _2, delay,INVALID_WAYS_PER_SKEW,GLOBAL_RANDOM,GLOBAL_LRU);
  }
};


///////////////////////////////////
// LRU replacement

class ReplaceLRU : public ReplaceFIFO
{
  private :
  bool isFirst;
public:
  // based off FIFO
  ReplaceLRU(uint32_t nset, uint32_t nway, uint32_t delay, uint32_t INVALID_WAYS_PER_SKEW, bool GLOBAL_RANDOM, bool GLOBAL_LRU) : ReplaceFIFO(nset, nway, delay, INVALID_WAYS_PER_SKEW,GLOBAL_RANDOM,GLOBAL_LRU) {
    isFirst = true;}
 
  virtual void access(int32_t set, uint32_t way) {
    // if way is present in the free map, remove it, and add to the used map
    // otherwise, remove from used map and re-insert at the end
    if(free_map[set].count(way)) {
      free_map[set].erase(way);
      used_map[set].push_back(way);
      used_map_global.push_back(std::make_tuple(set,way));
      if (isFirst) {
        isFirst = false;
      }
    } else {
      used_map[set].remove(way);
      used_map[set].push_back(way);
      used_map_global.remove(std::make_tuple(set,way));
      used_map_global.push_back(std::make_tuple(set,way));
    }
  }

  virtual ~ReplaceLRU() {}

  static ReplaceFuncBase *factory(uint32_t nset, uint32_t nway, uint32_t delay, uint32_t INVALID_WAYS_PER_SKEW, bool GLOBAL_RANDOM, bool GLOBAL_LRU) {
    return (ReplaceFuncBase *)(new ReplaceLRU(nset, nway, delay,INVALID_WAYS_PER_SKEW,GLOBAL_RANDOM,GLOBAL_LRU));
  }

  static replacer_creator_t gen(uint32_t delay = 0,uint32_t INVALID_WAYS_PER_SKEW=0, bool GLOBAL_RANDOM=0, bool GLOBAL_LRU=0) {
    
    using namespace std::placeholders;
    return std::bind(factory, _1, _2, delay,INVALID_WAYS_PER_SKEW,GLOBAL_RANDOM,GLOBAL_LRU);
  }
};

///////////////////////////////////
// SRRIP replacement
//
// https://dblp.org/rec/bib/conf/isca/JaleelTSE10
//

class ReplaceRRIP : public ReplaceFuncBase
{
protected:
  std::unordered_map<uint32_t, std::vector<uint32_t> > rrpv_map;
  uint32_t rrpv_max;
  bool GLOBAL_RRIP;

public:
  ReplaceRRIP(uint32_t nset, uint32_t nway, uint32_t width, uint32_t delay,bool GLOBAL_RRIP,uint32_t INVALID_WAYS_PER_SKEW)
    : ReplaceFuncBase(nset, nway, delay,INVALID_WAYS_PER_SKEW,0,0), rrpv_max(1<<width), GLOBAL_RRIP(GLOBAL_RRIP) {
      if (GLOBAL_RRIP) {
        for (int i=0; i<nset; i++) {
          rrpv_map[i] = std::vector<uint32_t>(nway,rrpv_max);
        }
      }
    }

  virtual uint32_t replace(uint64_t *latency, int32_t set) {
    // add latency

    latency_acc(latency);
    if (!GLOBAL_RRIP) {
      if(!rrpv_map.count(set))
        rrpv_map[set] = std::vector<uint32_t>(nway, rrpv_max);

      // find entry in the set with maximum RRPV
      uint32_t pos = 0, pmax = 0;
      for(uint32_t i=0; i<nway; i++)
        if(rrpv_map[set][i] > pmax) { pos = i; pmax = rrpv_map[set][i]; }

      // increment all RRPVs with the difference
      if(pmax < rrpv_max - 1) {
        uint32_t diff = rrpv_max - 1 - pmax;
        for(uint32_t i=0; i<nway; i++) rrpv_map[set][i] += diff;
      }

      // calculate cache capacity
      uint32_t cacheCapacity = 0;
      for (int i=0; i<nset; i++) {
        for (int j=0; j<nway; j++) {
          if (!rrpv_map.count(i)) {
            break;
          }
          if (rrpv_map[i][j] != rrpv_max) {
            cacheCapacity++;
          }
        }
      }      

      if (pmax == rrpv_max && cacheCapacity >= nset*(nway - INVALID_WAYS_PER_SKEW)) {
        // we need to evict something!
        pos = 0;
        pmax = 0;
        for (uint32_t i = 0; i < nway; i++) {
          if (rrpv_map[set][i] < rrpv_max && rrpv_map[set][i] > pmax) {
            pos = i;
            pmax = rrpv_map[set][i];
          }
        }

        if(pmax < rrpv_max - 1) {
          uint32_t diff = rrpv_max - 1 - pmax;
          for(uint32_t i=0; i<nway; i++) {
            if (rrpv_map[set][i] != rrpv_max) {
              rrpv_map[set][i] += diff;
            }
          }
        }

        return pos;

      }

      return pos;
    }

    // first we need to check : is SAE necessary?
    bool isSAENecessary = true;
    for (int i=0; i<nway; i++) {
      if (rrpv_map[set][i] == rrpv_max) {
        isSAENecessary = false; // there's an invalid way in this set, so SAE is not necessary
      }
    }
    
    if (isSAENecessary) {
      // find entry in the set with maximum RRPV
      uint32_t pos = 0, pmax = 0;
      std :: vector<uint32_t> cands;
      for(uint32_t i=0; i<nway; i++) {
        if(rrpv_map[set][i] > pmax) { pos = i; pmax = rrpv_map[set][i]; } 
      }     
      for (uint32_t i=0; i<nway; i++) {
        if (rrpv_map[set][i] == pmax) {
          cands.push_back(i);
        }
      }
      // change rrpv values of everyone
      if (pmax < rrpv_max - 1) {
        uint32_t diff = rrpv_max - 1 - pmax;
        for (int i=0; i<nset; i++) {
          for (int j=0; j<nway; j++) {
            if (rrpv_map[i][j] <= rrpv_max - 1) {
              rrpv_map[i][j] = std::min(rrpv_map[i][j] + diff,rrpv_max - 1); // We can't move it beyond rrpv_max - 1
            }
            else {
              rrpv_map[i][j] = rrpv_max; // don't change the rrpv value of invalid entries
            }
          }
        }
      }
      return cands[0];

    }
    else {

      // first lets check cache capacity = number of valid entries in cache
      uint32_t cacheCapacity = 0;
      for (int i=0; i<nset; i++) {
        for (int j=0; j<nway; j++) {
          if (rrpv_map[i][j] != rrpv_max) {
            cacheCapacity++;
          }
        }
      }


      // need to check if we need to do global eviction
      // need to do global eviction if and only if cache capacity >= nset*(nway - INVALID_WAYS_PER_SKEW)
      if (cacheCapacity < nset*(nway - INVALID_WAYS_PER_SKEW)) {
        std::vector<uint32_t> invalidWaysList;
        for (int i=0; i<nway; i++) {
          if (rrpv_map[set][i] == rrpv_max) {
            invalidWaysList.push_back(i);
          }
        }

        return invalidWaysList[0];

      }
      else {
        // need to do global eviction
        // first lets see globally what maximum *valid* rrpv position is
        uint32_t posSet = 0;
        uint32_t posWay = 0;
        uint32_t pmax = 0;
        for (int i=0; i<nset; i++) {
          for (int j=0; j<nway; j++) {
            if (rrpv_map[i][j] != rrpv_max && rrpv_map[i][j] > pmax) {
              // its a valid entry with a higher rrpv value
              posSet = i;
              posWay = j;
              pmax = rrpv_map[i][j];
            }
          }
        }
        // first we need to determine how much to increment every valid entry's rrpv values by
        uint32_t diff = rrpv_max - 1 - pmax;
        if (diff) {
          // we need to change everyone's rrpv values
          for (int i=0; i<nset; i++) {
            for (int j=0; j<nway; j++) {
              if (rrpv_map[i][j] != rrpv_max) {
                rrpv_map[i][j] += diff; // this is guaranteed to be <= rrpv_max - 1
              }
            }
          }
        }

        // now, among the guys having rrpv values = rrpv_max - 1, choose a random guy
        std::vector<std::pair<uint32_t,uint32_t>> replacementCandidates;
        for (int i=0; i<nset; i++) {
          for (int j=0; j<nway; j++) {
            if (rrpv_map[i][j] == rrpv_max - 1) {
              replacementCandidates.push_back(std::make_pair(i,j));
            }
          }
        }

        std::pair<uint32_t,uint32_t> evictedGuy;

        evictedGuy = replacementCandidates[get_random_uint64(replacementCandidates.size())];

        rrpv_map[evictedGuy.first][evictedGuy.second] = rrpv_max; // invalidate the evicted guy

        // finally select a random invalid way from this set and return it
        std::vector<uint32_t> insertionCandidates;
        for (int i=0; i<nway; i++) {
          if (rrpv_map[set][i] == rrpv_max) {
            // existence of invalid ways in this set is guaranteed :P
            insertionCandidates.push_back(i);
          }
        }

        return insertionCandidates[0];

      }
    }

  }

  virtual void access(int32_t set, uint32_t way) {
    // insert invalid entry at RRPV_MAX-2, otherwise insert at MRU position, this logic remains same regardless of whether global or not
    if(rrpv_map[set][way] == rrpv_max)
      rrpv_map[set][way] = rrpv_max - 2;
    else
      rrpv_map[set][way] = 0;
  }

  virtual void invalid(int32_t set, uint32_t way) {
    // invalidate entry by keeping it at RRPV_MAX position, again remains same regardless of global or not
    if(rrpv_map.count(set))
      rrpv_map[set][way] = rrpv_max;
  }

  virtual uint32_t count(int32_t set) {
    // calculate the number of valid ways
    uint32_t invalid_count = 0;
    if (!rrpv_map.count(set)) { // no valid ways here
      return 0;
    }
    for(uint32_t i=0; i<nway; i++) {
      if(rrpv_map[set][i] == rrpv_max) { invalid_count++; }
    }
    return nway - invalid_count;
  }

  virtual std::string to_string(int32_t set) const;
  virtual std::string to_string() const;
  virtual ~ReplaceRRIP() {}

  static ReplaceFuncBase *factory(uint32_t nset, uint32_t nway, uint32_t width, uint32_t delay, bool GLOBAL_RRIP,uint32_t INVALID_WAYS_PER_SKEW) {
    return (ReplaceFuncBase *)(new ReplaceRRIP(nset, nway, width, delay,GLOBAL_RRIP,INVALID_WAYS_PER_SKEW));
  }

  static replacer_creator_t gen(uint32_t width, uint32_t delay = 0, bool GLOBAL_RRIP=0,uint32_t INVALID_WAYS_PER_SKEW=0) {
    using namespace std::placeholders;
    return std::bind(factory, _1, _2, width, delay,GLOBAL_RRIP,INVALID_WAYS_PER_SKEW);
  }
};

// WARNING: Deprecated function, not used. Please see ReplaceRPLRU. That is the class which is actually used
class ReplacePLRU : public ReplaceFuncBase {
  protected:
  std::unordered_map<uint32_t, std::vector<uint32_t> > valid_map;
  bool GLOBAL_PLRU;
  uint32_t globValidCtr;
  int numSAE = 0;
  int traverseTree(std::vector<int> &tree, int currPos, int start, int end, int height, int currHeight, int nway, std::unordered_map<uint32_t, std::vector<uint32_t> > &valid_map) {

    if (currHeight == 0) {
      int globSet,globWay;
      if (tree[currPos] == 1) {
        globSet = start/nway;
        globWay = start%nway;
      }
      else {
        globSet = (end - 1)/nway;
        globWay = (end - 1)%nway;
      }
      if (valid_map[globSet][globWay]) {
        return globSet*nway + globWay;
      }
      else {
        tree[currPos] = 1 - tree[currPos];
        if (tree[currPos] == 1) {
          globSet = start/nway;
          globWay = start%nway;
        }
        else {
          globSet = (end - 1)/nway;
          globWay = (end - 1)%nway;
        }
        if (valid_map[globSet][globWay]) {
          return globSet*nway + globWay;
        }
        else {
          return -1;
        }
      }
    }
    else {
      int ogOutput;
      if (tree[currPos] == 1)  {
        ogOutput = traverseTree(tree,currPos+1,start,(start + end)/2,height,currHeight-1,nway,valid_map);
      }
      else {
        ogOutput = traverseTree(tree,currPos + pow(2,currHeight),(start + end)/2,end,height,currHeight-1,nway,valid_map);
      }
      if (ogOutput > 0) {
        return ogOutput;
      }
      else {
        tree[currPos] = 1 - tree[currPos];
        if (tree[currPos] == 1)  {
          ogOutput = traverseTree(tree,currPos+1,start,(start + end)/2,height,currHeight-1,nway,valid_map);
        }
        else {
          ogOutput = traverseTree(tree,currPos + pow(2,currHeight),(start + end)/2,end,height,currHeight-1,nway,valid_map);
        }
        if (ogOutput > 0) {
          return ogOutput;
        }
        else {
          return -1;
        }
      }
  
    }
  
  }
  
  std::vector<int> plruBits;

  public:
  ReplacePLRU(uint32_t nset, uint32_t nway, uint32_t width, uint32_t delay,bool GLOBAL_PLRU,uint32_t INVALID_WAYS_PER_SKEW, uint32_t plruBits)
    : ReplaceFuncBase(nset, nway, delay,INVALID_WAYS_PER_SKEW,0,0),GLOBAL_PLRU(GLOBAL_PLRU) {
      globValidCtr = 0;
      for (int i=0; i < nset; i++) {
        valid_map[i] = std::vector<uint32_t>(nway,0);
      }
      uint32_t prevBits = 1;
      for (int i=4; i <= nset*nway; i *= 2) {
        prevBits = 2*prevBits + 1;
      }
      for (int i=0; i < prevBits; i++) {
        this->plruBits.push_back(0);
      }
    }
  
  virtual uint32_t replace(uint64_t *latency, int32_t set) {
    latency_acc(latency);
    uint32_t validCount = 0;
    for (int i=0; i<nset; i++) {
      for (int j=0; j<nway; j++) {
        if (valid_map[i][j] == 1) {
          validCount++;
        }
      }
    }

    bool replNeeded = true;
    bool isInvalidWayPresent = false;
    for (int i=0; i < nway; i++) {
      if (valid_map[set][i] == 0 || valid_map[set][i] == 2) {
        replNeeded = false;
        isInvalidWayPresent = true;
        break;
      }
    }
    replNeeded = replNeeded || (validCount >= nset*(nway - INVALID_WAYS_PER_SKEW));

    if (!replNeeded) {
      for (int i=0; i < nway; i++) {
        if (valid_map[set][i] == 0) {
          valid_map[set][i] = 1;
          globValidCtr++;
          return i;
        }
      }
    }
    else {
      if (isInvalidWayPresent) {
        // global eviction
        uint32_t candidateLineStart = 0;
        uint32_t candidateLineEnd = nset*nway;
        uint32_t bitToConsider = 0;
        uint32_t height = log2(nset*nway) - 1;
        int globSet = -1;
        int globWay = -1;
        int globNet = traverseTree(plruBits,bitToConsider,candidateLineStart,candidateLineEnd,height,height,nway,valid_map);
        if (globNet == -1) {
          std::cerr << "bro ded\n";
          exit(1);
        }
        globSet = globNet/nway;
        globWay = globNet%nway;
        globValidCtr--;
        valid_map[globSet][globWay] = 0;

        for (int i=0; i < nway; i++) {
          if (valid_map[set][i] == 0) {
            globValidCtr++;
            valid_map[set][i] = 1;
            return i;
          }
        }

      }
      else {
        // SAE
        std::cerr << "SAE\n";
        numSAE++;
        return get_random_uint64(nway);
      }
    }
}
  virtual void access(int32_t set, uint32_t way) {

  uint32_t start = 0;
  uint32_t end = nway*nset;
  uint32_t height = log2(nway*nset) - 1;
  uint32_t bitToConsider = 0;

  while (start != end - 1) {

    if ((set*nway + way) < (start + end)/2) {
      plruBits[bitToConsider] = 0; // to mark that left half is more recently used
      end = (start + end)/2;
      bitToConsider += 1;
    }
    else {
      plruBits[bitToConsider] = 1; // to mark that right half is more recently used
      start = (start + end)/2;
      bitToConsider += pow(2,height);
    }
    height--;

  }

  }

  virtual void invalid(int32_t set, uint32_t way) {
   globValidCtr--;
   valid_map[set][way] = 0;
   access(set,way);
  }

  virtual uint32_t count(int32_t set) {
    // calculate the number of valid ways
    uint32_t invalid_count = 0;
    for (int i=0; i < nway; i++) {
      if (valid_map[set][i] == 1) {
        invalid_count++;
      }
    }
    return invalid_count;
  }

  virtual std::string to_string(int32_t set) const;
  virtual std::string to_string() const;
  virtual ~ReplacePLRU() {
    std::cerr << "numSAE = " << numSAE << "\n";
  }

  static ReplaceFuncBase *factory(uint32_t nset, uint32_t nway, uint32_t width, uint32_t delay, bool GLOBAL_PLRU,uint32_t INVALID_WAYS_PER_SKEW) {
    return (ReplaceFuncBase *)(new ReplacePLRU(nset, nway, width, delay,GLOBAL_PLRU,INVALID_WAYS_PER_SKEW,0));
  }

  static replacer_creator_t gen(uint32_t width, uint32_t delay = 0, bool GLOBAL_PLRU=0,uint32_t INVALID_WAYS_PER_SKEW=0) {
    using namespace std::placeholders;
    return std::bind(factory, _1, _2, width, delay,GLOBAL_PLRU,INVALID_WAYS_PER_SKEW);
  }
};

class ReplaceRPLRU : public ReplaceFuncBase {
  protected:
  bool GLOBAL_PLRU = false;
  std::vector<std::vector<bool>> valid_map;

  // per set lru
  std::vector<std::vector<int>> perSetLRU;

  // global list
  std::vector<std::vector<std::pair<int,int>>> globalTimestampLists;

  // local plru
  std::vector<std::vector<bool>> plruBitsVector;

  void printListSizes() {
    std::cerr << "Printing sizes\n";
    for (int i=0; i < nway; i++) {
      std::cerr << globalTimestampLists[i].size() << " ";
    }
    std::cerr << "\n";
  }

  void fixLists() {

    for (int i = 0; i < nway; i++) {
      auto& vec = globalTimestampLists[i];
      for (int j = vec.size() - 1; j >= 0; j--) {
        int set = vec[j].first;
        int way = vec[j].second;
        if (set > nset || way > nway) {
          std::cerr << "Absurd " << set << " " << way << " " << j << " " << vec.size() << "\n";
          exit(1);
        }
        if (!valid_map[set][way]) {
          // Swap with last element and pop
          std::cerr << "Popping " << set << " " << way << "\n";
          vec[j] = vec.back();
          vec.pop_back();
        }
      }
    }
    

    for (int i=nway - 1; i >= 0; i--) {
      if (globalTimestampLists[i].size() > ((nset*(nway - INVALID_WAYS_PER_SKEW))/(nway))) {
        int random_idx = get_random_uint64(globalTimestampLists[i].size());
        int demotedSet = globalTimestampLists[i][random_idx].first;
        int demotedWay = globalTimestampLists[i][random_idx].second;

        globalTimestampLists[i][random_idx].first = globalTimestampLists[i][globalTimestampLists[i].size() - 1].first;
        globalTimestampLists[i][random_idx].second = globalTimestampLists[i][globalTimestampLists[i].size() - 1].second;
        globalTimestampLists[i].pop_back();

        if (i == 0) {
          std::cerr << "Something went wrong\n";
          exit(1);
        }

        if (demotedSet > nset || demotedWay > nway) {
          std::cerr << "Pushing " << demotedSet << " " << demotedWay << " into " << i-1 << "\n";
        }
        globalTimestampLists[i-1].push_back(std::make_pair(demotedSet,demotedWay));
      }
    }
  }

  int traverseTree(std::vector<bool> &tree, int currPos, int start, int end, int height, int currHeight, int nway) {

    if (currHeight == 0) {
      if (tree[currPos]) {
        return start;
      }
      else {
        return end - 1;
      }
    }
    else {
      int ogOutput;
      if (tree[currPos])  {
        return traverseTree(tree,currPos+1,start,(start + end)/2,height,currHeight-1,nway);
      }
      else {
        return traverseTree(tree,currPos + pow(2,currHeight),(start + end)/2,end,height,currHeight-1,nway);
      }
    }
  
  }


  public:
  ReplaceRPLRU(uint32_t nset, uint32_t nway, uint32_t width, uint32_t delay,bool GLOBAL_PLRU,uint32_t INVALID_WAYS_PER_SKEW, uint32_t plruBits)
    : ReplaceFuncBase(nset, nway, delay,INVALID_WAYS_PER_SKEW,0,0),GLOBAL_PLRU(GLOBAL_PLRU) {

      if (!GLOBAL_PLRU) {

        for (int i=0; i < nset; i++) {
          valid_map.push_back(std::vector<bool>(nway,false));

          uint32_t prevBits = 1;
          for (int j=4; j <= nway; j*=2) {
            prevBits = 2*prevBits + 1;
          }
          std::vector<bool> innerPlruBitsVector;
          for (int j=0; j < prevBits; j++) {
            innerPlruBitsVector.push_back(false);
          }
          plruBitsVector.push_back(innerPlruBitsVector);

        }

      }
      else {
        
        for (int i=0; i < nway; i++) {
          std::vector<std::pair<int,int>> empty;
          globalTimestampLists.push_back(empty);
        }
  
        for (int i=0; i < nset; i++) {
          
          std::vector<bool> boolVec;
          std::vector<int> lruVec;
          
          for (int j=0; j < nway; j++) {
            boolVec.push_back(false);
            lruVec.push_back(j);
          }
          
          valid_map.push_back(boolVec);
          perSetLRU.push_back(lruVec);
  
        }
      }


    }
  
  virtual uint32_t replace(uint64_t *latency, int32_t set) {
    latency_acc(latency);

    if (!GLOBAL_PLRU) {
      
      if (INVALID_WAYS_PER_SKEW > 0) {
        std::cerr << "Not designed for invalid ways per skew >= 1" << "\n";
        exit(1);
      }

      // now check if this set has invalid ways
      for (int i=0; i < nway; i++) {
        if (valid_map[set][i] == 0) {
          return i;
        }
      }

      int candidateStart = 0;
      int candidateEnd = nway;
      int bitToConsider = 0;
      int height = log2(nway) - 1;
      return traverseTree(plruBitsVector[set],bitToConsider,candidateStart,candidateEnd,height,height,nway);

    }
    
    // first find out if replacement is needed
    bool isReplNeeded = true;
    bool isInvalidWayPresent = false;
    for (int i=0; i < nway; i++) {
      if (!valid_map[set][i]) {
        isReplNeeded = false;
        isInvalidWayPresent = true;
      } 
    }

    int validCount = 0;
    for (int i=0; i < nset; i++) {
      for (int j=0; j < nway; j++) {
        if (valid_map[i][j]) {
          validCount++;
        }
      }
    }


    isReplNeeded = isReplNeeded || (validCount >= (nset*(nway - INVALID_WAYS_PER_SKEW)));

    if (!isReplNeeded) {

      for (int i=0; i < nway; i++) {
        if (!valid_map[set][i]) {
          return i;
        }
      }

    }
    else {

      if (isInvalidWayPresent) {

        // Eviction path
        if (globalTimestampLists[0].size() != ((nset * (nway - INVALID_WAYS_PER_SKEW)) / nway)) {
          std::cerr << "Shouldn't happen\n";
          exit(1);
        }

        uint64_t random_idx = get_random_uint64(globalTimestampLists[0].size());
        int evset = globalTimestampLists[0][random_idx].first;
        int evway = globalTimestampLists[0][random_idx].second;

        // Evict from valid map
        valid_map[evset][evway] = false;

        // Remove (evset, evway) from globalTimestampLists[0]
        globalTimestampLists[0][random_idx] = globalTimestampLists[0].back();
        globalTimestampLists[0].pop_back();

        // Now allocate in current set
        for (int i = 0; i < nway; i++) {
          if (!valid_map[set][i]) {
            return i;
          }
        }

        std::cerr << "Should not reach here!\n";
        exit(1); 

      }
      else {

        std::vector<bool> sanity(nway,false);
        int zeroWay = -1;
        for (int i=0; i < nway; i++) {
          sanity[perSetLRU[set][i]] = true;
          if (perSetLRU[set][i] == 0) {
            zeroWay = i;
          }
        }
        bool finalOne = true;
        for (int i=0; i < nway; i++) {
          finalOne = finalOne && sanity[i];
        }
        if (!finalOne) {
          std::cerr << "Problem in per set lru\n";
          exit(1);
        }

        return zeroWay;

      }
    
    }

  }
  virtual void access(int32_t set, uint32_t way) {


    if (!valid_map[set][way] && GLOBAL_PLRU) {
      valid_map[set][way] = true;
      // Update per-set LRU
      for (int i = 0; i < nway; i++) {
        if (perSetLRU[set][i] > perSetLRU[set][way]) {
          perSetLRU[set][i]--;
        }
      }
      perSetLRU[set][way] = nway - 1;
      bool found = false;
      // Remove from all levels if already present
      for (int level = 0; level < nway; level++) {
        auto& list = globalTimestampLists[level];
        for (int i = list.size() - 1; i >= 0; i--) {
          if (list[i].first == set && list[i].second == way) {
            found = true;
            list[i] = list.back();
            list.pop_back();
            break;
          }
        }
      }

      if (found) {
        std::cerr << "Found " << set << " " << way << "\n";
        exit(1);
      }

      // Insert into MRU list
      if (set > nset || way > nway) {
        std::cerr << "Pushing back " << set << " " << way << "\n";
      }
      globalTimestampLists[nway - 1].emplace_back(set, way);
      fixLists();
    }
    else if (!valid_map[set][way] && !GLOBAL_PLRU) {
      valid_map[set][way] = true;
      // Update plruBitsVector
      uint32_t start = 0;
      uint32_t end = nway;
      uint32_t height = log2(nway) - 1;
      uint32_t bitToConsider = 0;
      while (start != end - 1) {
        if (way < (start + end) / 2) {
          plruBitsVector[set][bitToConsider] = 0; // to mark that left half is more recently used
          end = (start + end) / 2;
          bitToConsider += 1;
        }
        else {
          plruBitsVector[set][bitToConsider] = 1; // to mark that right half is more recently used
          start = (start + end) / 2;
          bitToConsider += pow(2, height);
        }
        height--;
      }

    }

  }

  virtual void invalid(int32_t set, uint32_t way) {
    valid_map[set][way] = false;

    if (GLOBAL_PLRU) {
      for (int i=0; i < nway; i++) {

        int removeIdx = -1;
        for (int j=0; j < globalTimestampLists[i].size(); j++) {
          auto x = globalTimestampLists[i][j];
          if (x.first == set && x.second == way) {
            removeIdx = j;
          }
        }
        if (removeIdx != -1) {
          globalTimestampLists[i][removeIdx] = globalTimestampLists[i].back();
          globalTimestampLists[i].pop_back();
        }
  
      }
    }

  }

  virtual uint32_t count(int32_t set) {

    int validCount = 0;
    for (int i=0; i < nway; i++) {
      validCount += (valid_map[set][i]);
    }
    return validCount;

  }

  virtual std::string to_string(int32_t set) const;
  virtual std::string to_string() const;
  virtual ~ReplaceRPLRU() {}

  static ReplaceFuncBase *factory(uint32_t nset, uint32_t nway, uint32_t width, uint32_t delay, bool GLOBAL_PLRU,uint32_t INVALID_WAYS_PER_SKEW) {
    return (ReplaceFuncBase *)(new ReplaceRPLRU(nset, nway, width, delay,GLOBAL_PLRU,INVALID_WAYS_PER_SKEW,0));
  }

  static replacer_creator_t gen(uint32_t width, uint32_t delay = 0, bool GLOBAL_PLRU=0,uint32_t INVALID_WAYS_PER_SKEW=0) {
    using namespace std::placeholders;
    return std::bind(factory, _1, _2, width, delay,GLOBAL_PLRU,INVALID_WAYS_PER_SKEW);
  }
};


#endif
