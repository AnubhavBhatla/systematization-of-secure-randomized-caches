#ifndef CM_SKEWED_HPP_
#define CM_SKEWED_HPP_

#include "cache/cache.hpp"
#include "util/query.hpp"
#include "util/random.hpp"


/////////////////////////////////
// skewed cache

class SkewedCache : public CacheBase
{
  const uint32_t partition;
public:
  // treat N partition skewed cache as a s*N set w/N way cache
  SkewedCache(uint32_t nset, uint32_t nway,
              indexer_creator_t ic,
              tagger_creator_t tc,
              replacer_creator_t rc,
              uint32_t level, int32_t core_id, int32_t cache_id,
              uint32_t partition,
              uint32_t delay, bool LOAD_BALANCING)
    : CacheBase(nset*partition, nway/partition, ic, tc, rc, level, core_id, cache_id, delay),
      partition(partition), LOAD_BALANCING(LOAD_BALANCING) {}

  virtual ~SkewedCache() {}
  bool LOAD_BALANCING;
  virtual int32_t get_index(uint64_t *latency, uint64_t addr) {
    int32_t skew_idx = (uint32_t)get_random_uint64(partition); // get a random partition
    if (LOAD_BALANCING)
    {
      // LOAD BALANCING
      skew_idx = 0;
      uint32_t count = nway+1;
      for(uint32_t si=0; si<partition; si++) {
        if (replacer->count(indexer->index(latency, addr, si)) < count) {
          count = replacer->count(indexer->index(latency, addr, si));
          skew_idx = si;
        }
      }
      std::vector<uint32_t> equal_skews;
      for(uint32_t si=0; si<partition; si++) {
        if (replacer->count(indexer->index(latency, addr, si)) == count) {
          equal_skews.push_back(si);
        }
      }
      uint32_t rand_idx = (uint32_t)get_random_uint64(equal_skews.size());
      skew_idx = equal_skews[rand_idx];
    }
    return indexer->index(latency, addr, skew_idx); // return set index corresponding to this partition
  }

  virtual bool hit(uint64_t *latency, uint64_t addr, int32_t *idx, uint32_t *way) {
    for(int si=0; si<partition; si++) { // for each partition
      *idx = indexer->index(latency, addr, si);
      for(int i=0; i<nway; i++) { // check all the ways for tag match
        uint64_t meta = get_meta(NULL, *idx, i);
        if(tagger->match(meta, addr) && !CM::is_invalid(meta)) {
          *way = i;
          return true;
        }
      }
    }
    return false; // cache miss
  }

  virtual LocInfo query_loc(uint64_t addr) { // Returns a new set of metadata where you insert your 'addr' into every possible place it could have been inserted in 
    LocInfo rv(level, core_id, cache_id, this); // rv is a map from int to pair<int,int> rv[i] = (x,y) indicates that addr could be in set i from way x to way y
    for(int i=0; i<partition; i++) // for every possible partition
      rv.insert(indexer->index(NULL, addr, i), LocRange(0, nway-1)); 
  /*
  
  rv at this point tells you that for every possible set the address could have been mapped to, the address could be in way 0 to way nway-1

  */
    return rv;
  }

  virtual bool query_coloc(uint64_t addrA, uint64_t addrB){ // returns true if ever addrA and addrB map to the same set in some skew
    std::unordered_set<uint32_t> idxA, idxB;
    for(int i=0; i<partition; i++) {
      idxA.insert(indexer->index(NULL, addrA, i)); // get set of addrA under skew i
      idxB.insert(indexer->index(NULL, addrB, i)); // get set of addrB under skew i
    }
    for(auto idx: idxA) {
      if(idxB.count(idx)) return true; // if ever set(addrA,i) == set(addrB,j) for any (i,j), return true
    }
    return false; // completely orthogonal addresses, return false
  }

  static CacheBase *factory(uint32_t nset, uint32_t nway,
                            indexer_creator_t ic,
                            tagger_creator_t tc,
                            replacer_creator_t rc,
                            uint32_t level,
                            int32_t core_id,
                            int32_t cache_id,
                            uint32_t partition,
                            uint32_t delay, bool LOAD_BALANCING) {
    return (CacheBase *)(new SkewedCache(nset, nway, ic, tc, rc, level, core_id, cache_id, partition, delay, LOAD_BALANCING));
  }

  static cache_creator_t gen(uint32_t nset, uint32_t nway,
                             indexer_creator_t ic,
                             tagger_creator_t tc,
                             replacer_creator_t rc,
                             uint32_t partition,
                             uint32_t delay = 0,
                             bool LOAD_BALANCING=0) {
    using namespace std::placeholders;
    return std::bind(factory, nset, nway, ic, tc, rc, _1, _2, _3, partition, delay,LOAD_BALANCING);
  }
};

#endif
