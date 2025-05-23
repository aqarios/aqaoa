/* 
 * Modified by Aqarios GmbH
 * 
 * Changes: Renamed all occurrences of 'cuaoa' to 'aqaoa'.
 *
 * Original License Notice:
 *
 * Copyright 2024 Jonas Blenninger
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include "aqaoa/brute_force.hpp"
#include "aqaoa/functions.hpp"
#include <cstdint>
#include <iostream>

BFSol brute_force_aqaoa(AqAOAHandle *handle, size_t numNodes, size_t *polykeys,
                        double *polyvals, size_t polysize, size_t blockSize) {
  BFSol solution;
  cudaSetDevice(handle->device);
  initializeHandle(handle, numNodes, polykeys, polyvals, polysize, blockSize);
  calcCostHamiltonian(handle);
  solution.bitStrings =
      findMinima(handle, &solution.cost, &solution.numMatches);
  return solution;
}
