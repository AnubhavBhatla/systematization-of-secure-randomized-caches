/*
 * Copyright 2022 The University of Adelaide
 *
 * This file is part of CacheFX.
 *
 * Created on: Feb 25, 2020
 *     Author: thomas
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <Cache/CustomCache.h>

#include <crypto/speck.h>
#include <iostream>

const char* CustomCache::CACHE_TYPESTR = "custom";

int ctr = 1;
// int tmp = 0;

std::vector<std::pair<int32_t,int32_t>> dataBlocks;

CustomCache::CustomCache(size_t replAlgorithm, size_t sets, size_t ways, size_t partitions, size_t invalidWays, bool loadBalancing)
    : _replAlgorithm(replAlgorithm), _nSets(sets), _nWays(ways), _nPartitions(partitions), _invalidFirst(true), _nInvalidWays(invalidWays), _loadBalancing(loadBalancing)
{
  // srand(47);
  if ((_nWays % _nPartitions) != 0)
  {
    _nPartitions = 1;
  }

  _cacheEntries.resize(_nWays);
  for (size_t w = 0; w < _nWays; w++)
  {
    _cacheEntries[w].resize(_nSets);
    for (size_t s = 0; s < _nSets; s++)
    {
      _cacheEntries[w][s].tag = TAG_INIT;
      _cacheEntries[w][s].accessTime = 0;
      _cacheEntries[w][s].flags = 0;
    }
  }
  initKeys();
}

void CustomCache::initKeys()
{
  // ASAN overflow: speck64ExpandKey() accesses 4th
  // element of type uint32_t*
  uint32_t K[] = {0x06FADE60, 0xCAB4BEEF, 0x04866840, 0x80866808};

  _key = new uint32_t[27];

  speck64ExpandKey(K, _key);
}

CustomCache::~CustomCache() { delete[] _key; }

int32_t CustomCache::readCl(tag_t cl, const CacheContext& context,
                             std::list<CacheResponse>& response)
{

  std::vector<cacheEntry*> vSet = getVirtualSet(cl); // all the sets that cl can map to
  const size_t partitionSize = (_nWays / _nPartitions); // the number of ways per partition

  int32_t replaceWay = -1; // the way in which we will insert
  for (size_t w = 0; w < _nWays; w++) {
    if (vSet[w]->tag == cl) { // cache hit
      access(*vSet[w]);
      response.push_back(CacheResponse(true));
      return 1;
    }
    if (vSet[w]->tag == TAG_NONE || vSet[w]->tag == TAG_INIT)
      replaceWay = w;
  }

  if (getLoadBalancing()) {
    replaceWay = -1;
    int32_t count[_nPartitions]; // keep count of number of invalid ways per partition
    for (size_t p = 0; p < _nPartitions; p++) {
        count[p] = 0;
        for (size_t w = 0; w < partitionSize; w++) {
            if (vSet[p*partitionSize + w]->tag == TAG_NONE || vSet[p*partitionSize + w]->tag == TAG_INIT)
                count[p]++;
        }
    }
    int32_t max_p = 0;
    int32_t max_count = -1;
    for (size_t p = 0; p < _nPartitions; p++) {
        if (count[p] > max_count)
            max_count = count[p];
    }
    std::vector<int32_t> equal_p;
    for(size_t p = 0; p < _nPartitions; p++) {
        if (count[p] == max_count)
            equal_p.push_back(p);
    }

    int32_t rand_idx = random() % (equal_p.size());
    max_p = equal_p[rand_idx]; // out partition is chosen
    for (size_t w = max_p*partitionSize; w < (max_p+1)*partitionSize; w++) {
        if (vSet[w]->tag == TAG_NONE || vSet[w]->tag == TAG_INIT)
            replaceWay = w;
    }
  }

  int32_t invalid_count = 0;
  for (size_t w = 0; w < _nWays; w++) {
    for (size_t s = 0; s < _nSets; s++) {
      if (_cacheEntries[w][s].tag == TAG_NONE || _cacheEntries[w][s].tag == TAG_INIT)
        invalid_count++;
    }
  }

  if (invalid_count > _nSets*_nPartitions*getNInvalidWays()) {
    if (replaceWay != -1) {
      vSet[replaceWay]->tag = cl; // just insert here
      access(*vSet[replaceWay]);
      int32_t chosenPartition = (replaceWay/partitionSize);
      int32_t setUnderChosenPartition = getIdx(cl,chosenPartition);

      dataBlocks.push_back(std::make_pair(setUnderChosenPartition,replaceWay));
      
      response.push_back(CacheResponse(false));
      return 0;
    }
    else if (replaceWay == -1) {
      if (getReplAlgorithm() == REPL_LRU) {
          uint64_t lru = ctr + 1;
          int idx = -1;
          for (int w = 0; w < _nWays; w++) {
            if (vSet[w]->accessTime < lru) {
              idx = w;
              lru = vSet[w]->accessTime;
            }
          }
          replaceWay = idx;
      }
      else {
        replaceWay = random() % _nWays;
      }
      response.push_back(CacheResponse(false, vSet[replaceWay]->tag));
      vSet[replaceWay]->tag = cl;
      access(*vSet[replaceWay]);
      return 0;
    }
  }
  else {
    if (replaceWay == -1) {
      if (getReplAlgorithm() == REPL_LRU) {
          uint64_t lru = ctr + 1;
          int idx = -1;
          for (int w = 0; w < _nWays; w++) {
            if (vSet[w]->accessTime < lru) {
              idx = w;
              lru = vSet[w]->accessTime;
            }
          }
          replaceWay = idx;
      }
      else {
        replaceWay = random() % _nWays;
      }
      response.push_back(CacheResponse(false, vSet[replaceWay]->tag));
      vSet[replaceWay]->tag = cl;
      access(*vSet[replaceWay]);
      return 0;
    }
    else if (replaceWay != -1 && getReplAlgorithm() == REPL_GRAN) {
      int32_t old_replace = replaceWay;
      int32_t replaceEntry = random() % (dataBlocks.size());

      int32_t replaceSet = dataBlocks[replaceEntry].first;
      replaceWay = dataBlocks[replaceEntry].second;
      _cacheEntries[replaceWay][replaceSet].tag = TAG_NONE;

      vSet[old_replace]->tag = cl;

      int32_t old_replace_set = getIdx(cl,(old_replace/partitionSize));
      dataBlocks[replaceEntry].first = old_replace_set;
      dataBlocks[replaceEntry].second = old_replace;

      access(*vSet[old_replace]);
      response.push_back(CacheResponse(false));
      return 0;
    }
    else {
      vSet[replaceWay]->tag = cl;
      access(*vSet[replaceWay]);
      response.push_back(CacheResponse(false));
      return 0;
    }
  }
}

void CustomCache::access(cacheEntry& ce) {
  ce.accessTime = ctr;
  ctr++;
}

int32_t CustomCache::evictCl(tag_t cl, const CacheContext& context,
                              std::list<CacheResponse>& response)
{
  exit(1);
  std::vector<cacheEntry*> vSet = getVirtualSet(cl);

  for (size_t w = 0; w < _nWays; w++)
  {
    if (vSet[w]->tag == cl)
    {
      vSet[w]->tag = TAG_NONE;
      response.push_back(CacheResponse(true, cl));
      return 1;
    }
  }

  response.push_back(CacheResponse(false));
  return 0;
}

const char* CustomCache::getCacheType() const { return CACHE_TYPESTR; }

size_t CustomCache::getNLines() const { return _nSets * _nWays; }

size_t CustomCache::getNWays() const { return _nWays; }

size_t CustomCache::getNSets() const { return _nSets; }

size_t CustomCache::getNInvalidWays() const { return _nInvalidWays; }

bool CustomCache::getLoadBalancing() const { return _loadBalancing; }

size_t CustomCache::getEvictionSetSize() const { return _nWays; }

size_t CustomCache::getGHMGroupSize() const { return _nWays; }

int32_t CustomCache::getNPartitions() const { return _nPartitions; }

size_t CustomCache::getReplAlgorithm() const { return _replAlgorithm; }

tag_t CustomCache::getIdx(tag_t cl, size_t partition) const
{
  uint64_t v, tweak;
  uint32_t* vPtr = (uint32_t*)&v;

  v = cl & 0xFFFFFFFFFFFFFFFF;
  tweak = (partition & 0xFF) * 0x0101010101010101;

  // Tweak via XEX construction

  v ^= tweak;
  speck64Encrypt(vPtr + 0, vPtr + 1, _key);
  v ^= tweak;

  return v % _nSets;
}

std::vector<cacheEntry*> CustomCache::getVirtualSet(tag_t cl)
{
  std::vector<cacheEntry*> vSet(_nWays);
  const size_t partitionSize = (_nWays / _nPartitions);
  for (size_t p = 0; p < _nPartitions; p++)
  {
    const tag_t idx = getIdx(cl, p);
    for (size_t w = 0; w < partitionSize; w++)
    {
      vSet[p * partitionSize + w] =
          &(_cacheEntries[p * partitionSize + w][idx]);
    }
  }
  return vSet;
}

std::vector<tag_t> CustomCache::getWayIndices(tag_t cl) const
{
  std::vector<tag_t> wayIndices(_nWays);
  const size_t partitionSize = (_nWays / _nPartitions);
  for (size_t p = 0; p < _nPartitions; p++)
  {
    const tag_t idx = getIdx(cl, p);
    for (size_t w = 0; w < partitionSize; w++)
      wayIndices[p * partitionSize + w] = idx;
  }
  return wayIndices;
}

int32_t CustomCache::hasCollision(tag_t cl1, const CacheContext& ctx1,
                                   tag_t cl2, const CacheContext& ctx2) const
{
  std::vector<tag_t> wayIndices1 = getWayIndices(cl1);
  std::vector<tag_t> wayIndices2 = getWayIndices(cl2);

  for (size_t w = 0; w < _nWays; w++)
  {
    if (wayIndices1[w] == wayIndices2[w])
    {
      return 1;
    }
  }
  return 0;
}

size_t CustomCache::getNumParams() const { return 2; }

uint32_t CustomCache::getParam(size_t idx) const
{
  if (idx == 0)
  {
    return _nPartitions;
  }
  else if (idx == 1)
  {
    return _invalidFirst;
  }
  return 0;
}
