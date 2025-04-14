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

#ifndef AQAOA_WRAPPER_HPP
#define AQAOA_WRAPPER_HPP

#ifdef __cplusplus
extern "C" {
#endif

#include "aqaoa/handle.hpp"
#include "wrapper/core.hpp"

AOAStatevectorResult statevecAqaoaWrapper(AqAOAHandle *handle, size_t numNodes,
                                          size_t depth, size_t *polykeys,
                                          double *polyvals, size_t polysize,
                                          double *betas, double *gammas,
                                          size_t blockSize,
                                          const char *rxmethod);

double expvalAqaoaWrapper(AqAOAHandle *handle, size_t numNodes, size_t depth,
                          size_t *polynomialKeys, double *polynomialValues,
                          size_t polynomialSize, double *betas, double *gammas,
                          size_t blockSize, const char *rxmethod);

AOAGradientsResult gradientsAqaoaWrapper(AqAOAHandle *handle, size_t numNodes,
                                         size_t depth, size_t *polykeys,
                                         double *polyvals, size_t polysize,
                                         const double *betas,
                                         const double *gammas, size_t blockSize,
                                         const char *rxmethod);

AOASampleSet sampleAqaoaWrapper(AqAOAHandle *handle, size_t numNodes,
                                size_t depth, size_t *polykeys,
                                double *polyvals, size_t polysize,
                                double *betas, double *gammas,
                                uint32_t maxShots, const uint32_t numShots,
                                const double *randnums, size_t blockSize,
                                const char *rxmethod);

#ifdef __cplusplus
}
#endif

#endif // EXPVAL_WRAPPER_HPP
