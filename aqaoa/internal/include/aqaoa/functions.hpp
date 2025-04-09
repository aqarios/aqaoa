/* Copyright 2024 Jonas Blenninger
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

#ifndef FUNCTIONS_HPP
#define FUNCTIONS_HPP

#include "aqaoa/aqaoa.hpp"
#include "aqaoa/handle.hpp"
#include <cstddef>
#include <tuple>

void initializeHandle(AqAOAHandle *handle, size_t numNodes, size_t *polykeys,
                      double *polyvals, size_t polysize, size_t blockSize);

double calculateExpectationValue(AqAOAHandle *handle);
cuDoubleComplex *retrieveStatevector(AqAOAHandle *handle);
double *retrieveCostHamiltonian(AqAOAHandle *handle);
size_t *retrievePolykeys(AqAOAHandle *handle);
double *retrievePolyVals(AqAOAHandle *handle);

void initializeStatevector(AqAOAHandle *handle);

void calcCostHamiltonian(AqAOAHandle *handle, const char *method);
void calcCostHamiltonian(AqAOAHandle *handle);

void applyCostHamiltonian(AqAOAHandle *handle, double gamma);
void calcCostHamiltonian(AqAOAHandle *handle);

void applyRxGate(AqAOAHandle *handle, double beta, int32_t adjoint,
                 const char *method);
void applyRxGate(AqAOAHandle *handle, double beta, int32_t adjoint);
void applyRxGateQO(AqAOAHandle *handle, double beta, int32_t adjoint);

SampleSet sampleStatevector(AqAOAHandle *handle, uint32_t maxShots,
                            const uint32_t numShots, const double *randnums);
void calculateGradients(AqAOAHandle *handle, size_t depth, const double *betas,
                        const double *gammas, double *betaGradients,
                        double *gammaGradients, const char *rxmethod);
int64_t *findMinima(AqAOAHandle *handle, double *maximum, size_t *numMatches);

#endif
