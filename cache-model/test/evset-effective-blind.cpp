#include "test/common.hpp"
#include <cmath>
#include <map>

inline int probe (L1CacheBase *entry, std::list<uint64_t> evset) {
  auto first = evset.cbegin();
  int missCount = 0;
  // get the last element in the window
  auto last = std::next(first, 1);
  while(first != evset.cend()) {
    // iterate from the first element to the last, read the element "repeat" number of times
    for(auto it=first; it!=last; it++)
        missCount += (1 - hit(CM::normalize(*it)));
    
    // advance the first and last iterators
    std::advance(first, 1);
    std::advance(last, 1);
  }
//   std::cout<<"Returning "<<missCount<<"\n";
  return missCount;  
}

int main(int argc, char* argv[]) {
  if(argc > 9 || argc < 8) {
    //                            0            1                 2          3           4              5       6      7     8
    std::cerr << "Usage: evset-effective <cache-config> <traverse-cfg> cache-level evset-size candidate-size tests warmup [mode]" << std::endl;
    return 1;
  }

  if(!cache_config_parser("config/cache.json", argv[1], &ccfg)) return 1;
  traverse_func_t traverse_func = traverse_config_parser("config/traverse.json", argv[2], &tcfg);

  uint32_t cache_level    = std::stoi(std::string(argv[3]));
  uint32_t ccfg_level     = cache_level - 1;
  uint32_t evset_size     = std::stoi(std::string(argv[4]));
  uint32_t candidate_size = std::stoi(std::string(argv[5]));
  uint32_t max_tests      = std::stoi(std::string(argv[6]));
  uint8_t warmup          = std::stoi(std::string(argv[7]));
  int      mode           = 0;
  if(argc == 8) {
    mode = std::stoi(std::string(argv[7]));
    if(mode < 0 || mode > 2) {
      std::cerr << "Available mode: 0, report; 1, debug; 2, output." << std::endl;
      return 1;
    }
  }

  // initialise the cache
  cache_init();

  // instantiation of the cache
  L1CacheBase *entry = (L1CacheBase *)l1_caches[0];

  // for (int i=0; i<16384; i++) {
  //   entry->read(get_random_uint64(1ull << 60));
  // }

  // records the eviction stats
  uint32_t evict_mean = init_mean_stat();
  if (warmup == 100){
    entry->warmup(100);
  }

    std::map<int,int> accessedMissMap;
    std::map<int,int> unaccessedMissMap;

  for(int i=0; i<max_tests; i++) {
    if (warmup != 100) {
      entry->warmup(warmup);
    }
    std::cout<<"Iteration number "<<i<<"\n";
    uint32_t trials = 1;
    std::list<uint64_t> evset;
    // select a random target address that we want to evict
    uint64_t target = get_random_uint64(1ull << 60);
    set_hit_check_func(target, entry, cache_level, traverse_func);
    // create an eviction set for target address
    while(!produce_targeted_evict_set(candidate_size, evset, evset_size, entry, cache_level, target)) {}
    // prime it
    traverse_func(entry, evset); // in our case this is list_traverse
    // read the target address
    entry->read(target);
    // prime the cache with the eviction set
    // now we need to probe
    int misses = probe(entry,evset); // assume we have some function to probe that returns the number of misses on probing
    if (warmup != 100) {
      entry->warmup(warmup);
    }
    // prime cache again
    traverse_func(entry,evset);
    // probe again
    int misses2 = probe(entry,evset);

    accessedMissMap[misses]++;
    unaccessedMissMap[misses2]++;

    // a hit means that there was no eviction of target
  }
    std::cout<<"For when target was accessed\n";
    for (auto it : accessedMissMap) {
        std::cout<<it.first<<" "<<it.second<<"\n";
    }
    std::cout<<"For when target wasn't accessed\n";
    for (auto it : unaccessedMissMap) {
        std::cout<<it.first<<" "<<it.second<<"\n";
    }

  // stop collecting stats
//   close_mean_stat(evict_mean);
  cache_release();
  return 0;
}
