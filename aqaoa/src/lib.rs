// Modified by Aqarios GmbH
//
// Changes: Renamed all occurrences of 'cuaoa' to 'aqaoa'.
//
// Original License Notice:
//
// Copyright 2024 Jonas Blenninger
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

mod bindings;

pub mod core;
pub mod parameters;
pub mod random;

pub mod algorithms;
pub mod prelude;

pub use algorithms::polynomial::make_polynomial;
pub use algorithms::polynomial::make_polynomial_from_map;
pub use bindings::aqaoa::Handle;

#[cfg(feature = "py")]
pub mod py_bindings;
