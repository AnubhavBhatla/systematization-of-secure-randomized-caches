#include "util/cache_config_parser.hpp"
#include "util/json.hpp"
#include "cache/skewed.hpp"
#include <iostream>
#include <fstream>
#include <boost/format.hpp>

using json = nlohmann::json;

#define MAX_RECUR_LEVEL 40

template<typename T>
inline void obtain_config(T& rv, const json &db, const std::string &label, const std::string &ctype, const std::string &param) {
  if(db[label][ctype].count(param)) rv = db[label][ctype][param].get<T>();
}

class IndexCFGLoc {
public:
  std::string ctype;
  uint32_t delay;
  uint32_t rtable_size;
  uint32_t partition;
  indexer_creator_t creator;
  IndexCFGLoc(): ctype("norm"), delay(0), rtable_size(0), partition(0), creator(IndexNorm::gen()) {}
};

void indexer_config_decoder(IndexCFGLoc *cfg, const json &db, const std::string &ctype, int t = 0) {
  if(t > MAX_RECUR_LEVEL) {
    std::cerr << boost::format("Recursive more than %1% times when trying to decode index configuration %2%" ) % MAX_RECUR_LEVEL % ctype << std::endl;
    return;
  }

  assert(db["indexer"].count(ctype));

  if(db["indexer"][ctype].count("base"))
    indexer_config_decoder(cfg, db, db["indexer"][ctype]["base"].get<std::string>(), t+1);

  obtain_config(cfg->ctype,       db, "indexer", ctype, "type"       );
  obtain_config(cfg->delay,       db, "indexer", ctype, "delay"      );
  obtain_config(cfg->rtable_size, db, "indexer", ctype, "rtable_size");
  obtain_config(cfg->partition,   db, "indexer", ctype, "partition"  );

  if(t == 0) { // the end of recursively calls
    if     (cfg->ctype == "norm"  ) cfg->creator = IndexNorm::gen(cfg->delay);
    else if(cfg->ctype == "random") cfg->creator = IndexRandom::gen(cfg->rtable_size, cfg->delay);
    else if(cfg->ctype == "skew"  ) cfg->creator = IndexSkewed::gen(cfg->partition, cfg->delay);
  }
}

class TagCFGLoc {
public:
  std::string ctype;
  uint32_t delay;
  tagger_creator_t creator;
  TagCFGLoc(): ctype("norm"), delay(0), creator(TagNorm::gen()) {}
};

void tagger_config_decoder(TagCFGLoc *cfg, const json &db, const std::string &ctype, int t = 0) {
  if(t > MAX_RECUR_LEVEL) {
    std::cerr << boost::format("Recursive more than %1% times when trying to decode tagger configuration %2%" ) % MAX_RECUR_LEVEL % ctype << std::endl;
    return;
  }

  assert(db["tagger"].count(ctype));

  if(db["tagger"][ctype].count("base"))
    tagger_config_decoder(cfg, db, db["tagger"][ctype]["base"].get<std::string>(), t+1);

  obtain_config(cfg->ctype, db, "tagger", ctype, "type" );
  obtain_config(cfg->delay, db, "tagger", ctype, "delay");

  if(t == 0) { // the end of recursively calls
    if     (cfg->ctype == "norm"  ) cfg->creator = TagNorm::gen();
    else if(cfg->ctype == "cbl"   ) cfg->creator = TagCBL::gen();
  }
}

class ReplaceCFGLoc {
public:
  std::string ctype;
  uint32_t delay;
  uint32_t width;
  uint32_t INVALID_WAYS_PER_SKEW = 0;
  bool GLOBAL_RANDOM = 0;
  bool GLOBAL_LRU = 0;
  bool GLOBAL_RRIP = 0;
  bool GLOBAL_PLRU = 0;
  replacer_creator_t creator;
  ReplaceCFGLoc(): ctype("lru"), delay(0), width(0), creator(ReplaceLRU::gen()) {}
};

void replacer_config_decoder(ReplaceCFGLoc *cfg, const json &db, const std::string &ctype, int t = 0) {
  if(t > MAX_RECUR_LEVEL) {
    std::cerr << boost::format("Recursive more than %1% times when trying to decode replacer configuration %2%" ) % MAX_RECUR_LEVEL % ctype << std::endl;
    return;
  }

  assert(db["replacer"].count(ctype));

  if(db["replacer"][ctype].count("base"))
    replacer_config_decoder(cfg, db, db["replacer"][ctype]["base"].get<std::string>(), t+1);

  obtain_config(cfg->ctype, db, "replacer", ctype, "type" );
  obtain_config(cfg->delay, db, "replacer", ctype, "delay");
  obtain_config(cfg->width, db, "replacer", ctype, "width");
  obtain_config(cfg->INVALID_WAYS_PER_SKEW,db,"replacer",ctype,"INVALID_WAYS_PER_SKEW");
  obtain_config(cfg->GLOBAL_RANDOM,db,"replacer",ctype,"GLOBAL_RANDOM");
  obtain_config(cfg->GLOBAL_LRU,db,"replacer",ctype,"GLOBAL_LRU");
  obtain_config(cfg->GLOBAL_RRIP,db,"replacer",ctype,"GLOBAL_RRIP");
  obtain_config(cfg->GLOBAL_PLRU,db,"replacer",ctype,"GLOBAL_PLRU");

  if(t == 0) { // the end of recursively calls
    if     (cfg->ctype == "norm"  ) cfg->creator = ReplaceLRU::gen(cfg->delay);
    else if(cfg->ctype == "lru"   ) cfg->creator = ReplaceLRU::gen(cfg->delay,cfg->INVALID_WAYS_PER_SKEW,cfg->GLOBAL_RANDOM,cfg->GLOBAL_LRU);
    else if(cfg->ctype == "random") cfg->creator = ReplaceRandom::gen(cfg->delay);
    else if(cfg->ctype == "fifo"  ) cfg->creator = ReplaceFIFO::gen(cfg->delay,cfg->INVALID_WAYS_PER_SKEW,cfg->GLOBAL_RANDOM,cfg->GLOBAL_LRU);
    else if(cfg->ctype == "rrip"  ) cfg->creator = ReplaceRRIP::gen(cfg->width, cfg->delay,cfg->GLOBAL_RRIP,cfg->INVALID_WAYS_PER_SKEW);
    else if(cfg->ctype == "plru"  ) cfg->creator = ReplacePLRU::gen(cfg->width, cfg->delay,cfg->GLOBAL_PLRU,cfg->INVALID_WAYS_PER_SKEW);
    else if(cfg->ctype == "rplru" ) cfg->creator = ReplaceRPLRU::gen(cfg->width,cfg->delay,cfg->GLOBAL_PLRU,cfg->INVALID_WAYS_PER_SKEW);
  }
}

class HashCFGLoc {
public:
  std::string ctype;
  uint32_t delay;
  llc_hash_creator_t creator;
  HashCFGLoc(): ctype("norm"), delay(0), creator(LLCHashNorm::gen()) {}
};

void hasher_config_decoder(HashCFGLoc *cfg, const json &db, const std::string &ctype, int t = 0) {
  if(t > MAX_RECUR_LEVEL) {
    std::cerr << boost::format("Recursive more than %1% times when trying to decode hasher configuration %2%" ) % MAX_RECUR_LEVEL % ctype << std::endl;
    return;
  }

  assert(db["hasher"].count(ctype));

  if(db["hasher"][ctype].count("base"))
    hasher_config_decoder(cfg, db, db["hasher"][ctype]["base"].get<std::string>(), t+1);

  obtain_config(cfg->ctype, db, "hasher", ctype, "type" );
  obtain_config(cfg->delay, db, "hasher", ctype, "delay");

  if(t == 0) { // the end of recursively calls
    if     (cfg->ctype == "norm"  ) cfg->creator = LLCHashNorm::gen();
    else if(cfg->ctype == "hash"  ) cfg->creator = LLCHashHash::gen();
  }
}

class CacheCFGLoc {
public:
  std::string ctype;
  uint32_t delay;
  uint32_t number;
  uint32_t nset;
  uint32_t nway;
  uint32_t partition;
  std::string indexer;
  std::string tagger;
  std::string replacer;
  std::string hasher;
  cache_creator_t creator;
  bool LOAD_BALANCING = false;
  CacheCFGLoc()
    : ctype("norm"), delay(0),
      number(1), nset(64), nway(8),
      partition(1),
      indexer("norm"), tagger("norm"), replacer("lru"), hasher("norm") {} 
};

void cache_config_decoder(CacheCFGLoc *cfg, const json &db, const std::string &ctype, int t = 0) {
  if(t > MAX_RECUR_LEVEL) {
    std::cerr << boost::format("Recursive more than %1% times when trying to decode cache configuration %2%" ) % MAX_RECUR_LEVEL % ctype << std::endl;
    return;
  }

  assert(db["cache"].count(ctype));

  if(db["cache"][ctype].count("base"))
    cache_config_decoder(cfg, db, db["cache"][ctype]["base"].get<std::string>(), t+1);

  obtain_config(cfg->ctype,    db, "cache", ctype, "type"     );
  obtain_config(cfg->delay,    db, "cache", ctype, "delay"    );
  obtain_config(cfg->number,   db, "cache", ctype, "number"   );
  obtain_config(cfg->nset,     db, "cache", ctype, "set"      );
  obtain_config(cfg->nway,     db, "cache", ctype, "way"      );
  obtain_config(cfg->partition,db, "cache", ctype, "partition");
  obtain_config(cfg->indexer,  db, "cache", ctype, "indexer"  );
  obtain_config(cfg->tagger,   db, "cache", ctype, "tagger"   );
  obtain_config(cfg->replacer, db, "cache", ctype, "replacer" );
  obtain_config(cfg->hasher,   db, "cache", ctype, "hasher"   );
  obtain_config(cfg->LOAD_BALANCING,db,"cache",ctype,"LOAD_BALANCING");

  if(t == 0) { // the end of recursively calls
    IndexCFGLoc   index_config;   indexer_config_decoder(  &index_config,   db, cfg->indexer );
    TagCFGLoc     tag_config;     tagger_config_decoder(   &tag_config,     db, cfg->tagger  );
    ReplaceCFGLoc replace_config; replacer_config_decoder( &replace_config, db, cfg->replacer);

    if(cfg->ctype == "norm"  )
      cfg->creator = CacheBase::gen(cfg->nset, cfg->nway, index_config.creator, tag_config.creator, replace_config.creator, cfg->delay);
    else if(cfg->ctype == "skew")
      cfg->creator = SkewedCache::gen(cfg->nset, cfg->nway, index_config.creator, tag_config.creator, replace_config.creator, cfg->partition, cfg->delay,cfg->LOAD_BALANCING);
  }
}

bool cache_config_parser(const std::string& fn, const std::string& cfg, CacheCFG *ccfg) {
  json db;
  std::ifstream db_file(fn);
  if(db_file.good()) {
    db_file >> db;
    db_file.close();
    //std::cout << db.dump(4) << std::endl;
  } else {
    std::cerr << boost::format("Fail to open config file `%1%") % fn << std::endl;
    return false;
  }

  if(!db.count("config") || !db["config"].count(cfg)) {
    std::cerr << boost::format("Fail to find the specific config `%1%'. ") % cfg << std::endl;
    return false;
  }

  std::vector<std::string> cache_cfgs = db["config"][cfg].get< std::vector<std::string> >();

  for(int level = 0; level < MAX_CACHE_LEVEL; level++) {
    if(level >= cache_cfgs.size()) {
      ccfg->enable[level] = false;
      continue;
    } else ccfg->enable[level] = true;

    std::string ctype = cache_cfgs[level];

    CacheCFGLoc   cache_config;   cache_config_decoder(    &cache_config,   db, ctype               );
    HashCFGLoc    hash_config;    hasher_config_decoder(   &hash_config,    db, cache_config.hasher );

    ccfg->number[level] = cache_config.number;
    ccfg->cache_gen[level] = cache_config.creator;
    ccfg->hash_gen[level] = hash_config.creator;

    ccfg->nset[level] = cache_config.nset;
    ccfg->nway[level] = cache_config.nway;
    ccfg->skew_partition[level] = cache_config.partition;
  }

  return true;
}
