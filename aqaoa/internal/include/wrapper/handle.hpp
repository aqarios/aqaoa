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

#ifndef HANDLE_WRAPPER_HPP
#define HANDLE_WRAPPER_HPP

#include "aqaoa/handle.hpp"
#include <cstddef>
#include <cstdint>

#ifdef __cplusplus
extern "C" {
#endif

AqAOAHandle *createHandle(size_t numNodes, int device, bool exact);
void destroyHandle(AqAOAHandle *handle);

#ifdef __cplusplus
}
#endif

#endif
