/*

  Prime+Prune+Probe  

*/
#include "test/common.hpp"
#include <cmath>

bool primeprune(std::list<uint64_t> &prime_set, L1CacheBase *entry, uint64_t evict_pre, uint64_t period) {
  prime_set.clear();
  for (int i=0; i<2048*16; i++) {
    prime_set.push_back(get_random_uint64(1ull << 60));
  }

  size_t ssize;
  uint64_t pass = 0;
  do {
    
    ssize = prime_set.size();
    uint32_t miss = 0;
    for(auto it=prime_set.rbegin(); it != prime_set.rend(); it++) {
      if(!hit(*it)) miss++;
      entry->read(*it);
    }

    miss = 0;
    for(auto it=prime_set.begin(); it != prime_set.end();) {
      bool h = hit(*it);
      entry->read(*it);
      if(!h) {
        miss++;
        it = prime_set.erase(it);
      } else it++;
    }
    pass++;

  } while((reporter.check_cache_evict(2) - evict_pre < period) && (ssize != prime_set.size())); 

  if (ssize != prime_set.size())
    return 0;
  else 
    return 1;
}

int main(int argc, char* argv[]) {
  if(argc <= 6) {
    //                        0             1                 2          3         4         5      6-n
    std::cerr << "Usage: evset-attack <cache-config> <traverse-cfg> cache-level max-evict tests evsizes[0..n]" << std::endl;
    return 1;
  }
  if(!cache_config_parser("config/cache.json", argv[1], &ccfg)) return 1;
  traverse_func_t traverse_func = traverse_config_parser("config/traverse.json", argv[2], &tcfg);
  uint32_t cache_level    = std::stoi(std::string(argv[3]));
  uint32_t ccfg_level     = cache_level - 1;
  uint64_t period         = std::stoi(std::string(argv[4]));
  uint32_t max_tests      = std::stoi(std::string(argv[5]));
  std::vector<size_t> evset_sizes(argc-6);
  std::vector<uint32_t> stat_handlers(argc-6);
  int stat_n = argc-6;

  std::cout << "Config: " << argv[1] << " Period: " << period << " Tests: " << max_tests << std::endl;
  
  for(int i=0; i<stat_n; i++) {
    evset_sizes[i] = std::stoi(std::string(argv[6+i]));
    stat_handlers[i] = init_mean_stat();
  }
  cache_init();
  L1CacheBase *entry = (L1CacheBase *)l1_caches[0];
  reporter.register_cache_access_tracer(2);

  for(int test=0; test<max_tests; test++) {
    std::cout << "Test " << test << std::endl;

    std::unordered_set<uint64_t> evset;
    std::list<uint64_t> prime_set;

    uint64_t target = get_random_uint64(1ull << 60);
    CacheBase *target_cache = get_target_cache(target, entry, 2).cache;

    hit = std::bind(query_hit, std::placeholders::_1, target_cache);
    check = std::bind(query_check, target, target_cache, std::placeholders::_1);

    uint64_t evict_pre = reporter.check_cache_evict(2);
    uint64_t access_pre = reporter.check_cache_access(2);

    // get_random_list(prime_set, 2048*16, 1ull << 60);

    // size_t ssize;
    // uint64_t pass = 0;
    // do {
      
    //   ssize = prime_set.size();
    //   uint32_t miss = 0;
    //   for(auto it=prime_set.rbegin(); it != prime_set.rend(); it++) {
    //     if(!hit(*it)) miss++;
    //     entry->read(*it);
    //   }

    //   miss = 0;
    //   for(auto it=prime_set.begin(); it != prime_set.end();) {
    //     bool h = hit(*it);
    //     entry->read(*it);
    //     if(!h) {
    //       miss++;
    //       it = prime_set.erase(it);
    //     } else it++;
    //   }
    //   pass++;

    // } while((reporter.check_cache_evict(2) - evict_pre < period) && (ssize != prime_set.size())); 
    bool prunedone;

    while ((reporter.check_cache_evict(2) - evict_pre < period) && (evset.size() < evset_sizes[0])) {
      prunedone = false;
      while (!prunedone) {
        prunedone = primeprune(prime_set, entry, evict_pre, period);
        // if (!prunedone)
          // std::cout << "Evset Failed" << std::endl;
        if (!(reporter.check_cache_evict(2) - evict_pre < period)) {
          // std::cout << "Ran out of evictions" << std::endl;
          break;
        }
      }

      if (!prunedone)
        break;
        
      // std::cout << "Evictions after pruning: " << (reporter.check_cache_evict(2) - evict_pre) << std::endl;
      // std::cout << "Prime Set Size: " << prime_set.size() << " Success? " << prunedone << std::endl;

      int prevsize = -1;
      while ((prevsize != evset.size()) && (evset.size() < evset_sizes[0])) {
        // std::cout << "Here" << std::endl;
        prevsize = evset.size();
        entry->read(target);
        // int count = 0;
        for(auto it=prime_set.begin(); it != prime_set.end(); it++) {
          // std::cout << count++ << std::endl;
          bool h = hit(*it);
          entry->read(*it);
          if(!h) {
            // std::cout << "Here2" << std::endl; 
            evset.insert(*it);
            it = prime_set.erase(it);
            break;
          }
        }
        // std::cout << "Eviction Set Size: " << evset.size() << std::endl;
      }
    }

    std::cout << "Total Evictions: " << (reporter.check_cache_evict(2) - evict_pre) << std::endl;
    std::cout << "Total Accesses: " << (reporter.check_cache_access(2) - access_pre) << std::endl;

    for(int i=0; i<stat_n; i++) {
      record_mean_stat(stat_handlers[i], ((evset.size() >= evset_sizes[i])) ? 1.0 : 0.0);
      std::cout << period << ", Inter, " << ((evset.size() >= evset_sizes[i])) << std::endl;
    }
  }
  std::cout << period;
  for(auto stat:stat_handlers) {
    std::cout << "," << get_mean_mean(stat);
    close_mean_stat(stat);
  }
  std::cout << std::endl;
  cache_release();
  return 0;
}

// uint32_t
// obtain_cache_prime_set(
//                        uint32_t num,
//                        std::list<uint64_t>& prime_set,
//                        L1CacheBase * cache,
//                        hit_func_t hit
//                        )
// {
//   get_random_list(prime_set, num, 1ull << 60);

//   size_t ssize;
//   uint64_t pass = 0;
//   do {
//     ssize = prime_set.size();
//     uint32_t miss = 0;
//     for(auto it=prime_set.rbegin(); it != prime_set.rend(); it++) {
//       if(!hit(*it)) miss++;
//       cache->read(*it);
//     }
 
//     miss = 0;
//     for(auto it=prime_set.begin(); it != prime_set.end();) {
//       bool h = hit(*it);
//       cache->read(*it);
//       if(!h) {
//         miss++;
//         it = prime_set.erase(it);
//       } else it++;
//     }
//     pass++;
//   } while(ssize != prime_set.size() && pass < 20);

//   if(ssize == prime_set.size()) {
//     //std::cout << "prime size: " << ssize << std::endl;
//     return pass;
//   }
//   else
//     return 0;
// }