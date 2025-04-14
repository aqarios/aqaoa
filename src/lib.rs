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

mod aqaoa;
mod brute_force;
mod core;
mod handle;
mod pymodule;
mod utils;

pub use core::Parameters;

use pyo3::prelude::*;

#[pymodule]
#[pyo3(name = "_core")]
fn pyaqaoa(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    pymodule::register_pyaqaoa(m)?;
    Ok(())
}
