/*
 * Copyright 2022 The University of Adelaide
 *
 * This file is part of CacheFX.
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

#include <PlaintextKeyPairGenerator/AESPlaintextKeyPairGenerator.h>
#include <PlaintextKeyPairGenerator/PlaintextKeyPairGenerator.h>

#include <algorithm>
#include <cstdint>
#include <vector>
#include <iostream>

#include <Random.h>

using namespace std;

static uint8_t mix(uint8_t a, uint8_t b) { return (a & 0xf) | (b & 0xf0); }

AESPlaintextKeyPairGenerator::AESPlaintextKeyPairGenerator(
    const uint64_t keyLength, const uint64_t length)
    : PlaintextKeyPairGenerator(keyLength, length)
{
  generateKey();
}

void AESPlaintextKeyPairGenerator::generateKey()
{
  keyA.resize(keyLength);
  keyB.resize(keyLength);

  for (int32_t i = 0; i < 16; i++)
  {
    keyA[i] = Random::get()->rand();
    keyB[i] = Random::get()->rand();
  }
  keyB[0] = mix(keyB[0], keyA[0] ^ 0x10);
  keyB[4] = mix(keyB[4], keyA[4] ^ 0x20);
  keyB[8] = mix(keyB[8], keyA[8] ^ 0x30);
  keyB[12] = mix(keyB[12], keyA[12] ^ 0x40);

  // fix the keys
  // keyA[0] = 65;
  // keyA[1] = 77;
  // keyA[2] = 206;
  // keyA[3] = 60;
  // keyA[4] = 249;
  // keyA[5] = 196;
  // keyA[6] = 3;
  // keyA[7] = 58;
  // keyA[8] = 128;
  // keyA[9] = 153;
  // keyA[10] = 97;
  // keyA[11] = 209;
  // keyA[12] = 8;
  // keyA[13] = 26;
  // keyA[14] = 97;
  // keyA[15] = 198;
    
  // keyB[0] = 91;
  // keyB[1] = 201;
  // keyB[2] = 219;
  // keyB[3] = 156;
  // keyB[4] = 216;
  // keyB[5] = 15;
  // keyB[6] = 179;
  // keyB[7] = 32;
  // keyB[8] = 191;
  // keyB[9] = 252;
  // keyB[10] = 7;
  // keyB[11] = 80;
  // keyB[12] = 78;
  // keyB[13] = 128;
  // keyB[14] = 161;
  // keyB[15] = 209;
  

  return;
}

void AESPlaintextKeyPairGenerator::generatePlaintext()
{
  plaintext.clear();
  uint8_t byte = 0;
  transform(keyA.begin(), keyA.end(), back_inserter(plaintext),
            [&byte](const uint8_t key) {
              uint8_t randKey = Random::get()->rand();
              switch (byte)
              {
              case 0:
              case 4:
              case 8:
              case 12:
                randKey = mix(randKey, key);
                break;
              }
              byte++;
              return randKey;
            });
  // plaintext[0] = 68;
  // plaintext[1] = 97;
  // plaintext[2] = 183;
  // plaintext[3] = 114;
  // plaintext[4] = 240;
  // plaintext[5] = 114;
  // plaintext[6] = 152;
  // plaintext[7] = 5;
  // plaintext[8] = 143;
  // plaintext[9] = 34;
  // plaintext[10] = 150;
  // plaintext[11] = 101;
  // plaintext[12] = 13;
  // plaintext[13] = 254;
  // plaintext[14] = 107;
  // plaintext[15] = 215;
  
  
  // exit(0);
}

const std::vector<uint8_t>& AESPlaintextKeyPairGenerator::getPlaintext()
{
  generatePlaintext();
  return plaintext;
}