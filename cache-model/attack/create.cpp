#include "attack/create.hpp"
#include "cache/cache.hpp"
#include "util/query.hpp"
#include "util/random.hpp"

bool obtain_targeted_evict_set(
                               uint32_t num,
                               std::list<uint64_t>& candidate,
                               L1CacheBase * cache,
                               uint64_t target,
                               traverse_test_t traverse,
                               uint32_t trial
                               )
{
  for(int i=0; trial==0 || i<trial; i++) {
    candidate.clear();
    get_random_list(candidate, num, 1ull << 60);
    if(traverse(cache, candidate, target))
      return true;
  }
  return false;
}

bool
produce_targeted_evict_set(
                           uint32_t candidate_size,
                           std::list<uint64_t>& evset_rv,
                           uint32_t evset_size,
                           L1CacheBase * cache,
                           uint32_t level,
                           uint64_t target
                           )
{
  std::list<LocInfo> locs;
  cache->query_loc(target, &locs); // locs will now have the target inserted into every possible place it could have gone to...
  /*
  
  query_loc(addr,&locs) goes to a coherentCache function which calls cache->query_loc (see comments of this func in skewed.hpp) for all caches in the coherent cache structure
  In our case, this will contain a list of all sets in L1 this could go to (which is pretty useless)
  and a list of all sets in L2 this could go to (useful!, also our L2 is a skewed cache)
  
  */
  auto it = locs.begin();
  for(int i=1; i<level; i++) it++; // in our case, level is 2 (L2) so this just makes sure we don't try to build an evictSet for L1
  CacheBase *c = it->cache; // In our case this should be a skewed cache (CEASER-S)

  std::unordered_set<uint64_t> candidate, evset;
  get_random_set64(candidate, candidate_size, 1ull << 60); // haven't seen this function in depth but am hoping this is just a random init func
  for(auto addr : candidate) {
    if(c->query_coloc(CM::normalize(target), CM::normalize(addr))) // for CEASER-S, returns true if target and addr map to same set under any skew
      evset.insert(addr); // if so, put it into evset
    if(evset.size() == evset_size) break;
  }
  if(evset.size() == evset_size) {
    evset_rv.insert(evset_rv.end(), evset.begin(), evset.end()); // set evset_rv = evset 
    return true;
  } else
    return false;
}

bool getNewEvset (uint32_t candidate_size,std::list<uint64_t>& evset_rv,uint32_t evset_size,L1CacheBase * cache,uint32_t level,uint64_t target) {
  std::list<LocInfo> locs;
  cache->query_loc(target, &locs);
  auto it = locs.begin();
  for(int i=1; i<level; i++) it++;
  CacheBase *c = it->cache;

  std::unordered_set<uint64_t> evset;
  while (evset.size() != evset_size) {
    uint64_t addr = get_random_uint64(1ull << 60);
      if(c->query_coloc(CM::normalize(target), CM::normalize(addr)))
        evset.insert(addr);
    }
    evset_rv.insert(evset_rv.end(), evset.begin(), evset.end());
    return true;
}

uint32_t
obtain_cache_prime_set(
                       uint32_t num,
                       std::list<uint64_t>& prime_set,
                       L1CacheBase * cache,
                       hit_func_t hit
                       )
{
  get_random_list(prime_set, num, 1ull << 60);

  size_t ssize;
  uint64_t pass = 0;
  do {
    ssize = prime_set.size();
    uint32_t miss = 0;
    for(auto it=prime_set.rbegin(); it != prime_set.rend(); it++) {
      if(!hit(*it)) miss++;
      cache->read(*it);
    }
 
    miss = 0;
    for(auto it=prime_set.begin(); it != prime_set.end();) {
      bool h = hit(*it);
      cache->read(*it);
      if(!h) {
        miss++;
        it = prime_set.erase(it);
      } else it++;
    }
    pass++;
  } while(ssize != prime_set.size() && pass < 20);

  if(ssize == prime_set.size()) {
    //std::cout << "prime size: " << ssize << std::endl;
    return pass;
  }
  else
    return 0;
}
