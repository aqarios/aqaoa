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

use crate::{
    bindings::{self, aqaoa::Handle},
    core::{AOASampleSet, Gradients, LBFGSParameters, OptimizationResult, Polynomial, RXMethod},
};
use num::complex::Complex64;

use super::aoa::{AOAAssociatedFunctions, AOAInterface, AOA};

pub struct AqAOA {
    aoa: AOA,
}

impl AOAInterface for AqAOA {
    fn create(aoa: AOA) -> AqAOA {
        AqAOA { aoa }
    }
    fn aoa(&self) -> &AOA {
        &self.aoa
    }

    fn set_aoa(&mut self, aoa: AOA) {
        self.aoa = aoa;
    }

    fn mutable_aoa(&mut self) -> &mut AOA {
        &mut self.aoa
    }
}

impl AOAAssociatedFunctions for AqAOA {
    fn statevector(
        handle: &Handle,
        num_qubits: usize,
        depth: usize,
        polynomial: &Polynomial,
        betas: &[f64],
        gammas: &[f64],
        block_size: Option<usize>,
        rxmethod: Option<RXMethod>,
    ) -> Result<Vec<Complex64>, String> {
        bindings::aqaoa::statevector(
            handle,
            num_qubits,
            depth,
            polynomial.keys.as_slice(),
            polynomial.values.as_slice(),
            betas,
            gammas,
            block_size,
            rxmethod,
        )
    }

    fn sample(
        handle: &Handle,
        num_qubits: usize,
        depth: usize,
        polynomial: &Polynomial,
        betas: &[f64],
        gammas: &[f64],
        num_shots: u32,
        randnums: &[f64],
        block_size: Option<usize>,
        rxmethod: Option<RXMethod>,
    ) -> Result<AOASampleSet, String> {
        bindings::aqaoa::sample(
            handle,
            num_qubits,
            depth,
            polynomial.keys.as_slice(),
            polynomial.values.as_slice(),
            betas,
            gammas,
            num_shots + 1,
            num_shots,
            randnums,
            block_size,
            rxmethod,
        )
    }

    fn optimize(
        handle: &Handle,
        num_qubits: usize,
        depth: usize,
        polynomial: &Polynomial,
        betas: &[f64],
        gammas: &[f64],
        lbfgs_parameters: Option<&LBFGSParameters>,
        block_size: Option<usize>,
        rxmethod: Option<RXMethod>,
    ) -> Result<OptimizationResult, String> {
        bindings::aqaoa::optimize(
            handle,
            num_qubits,
            depth,
            polynomial.keys.as_slice(),
            polynomial.values.as_slice(),
            betas,
            gammas,
            lbfgs_parameters,
            block_size,
            rxmethod,
        )
    }

    fn gradients(
        handle: &Handle,
        num_qubits: usize,
        depth: usize,
        polynomial: &Polynomial,
        betas: &[f64],
        gammas: &[f64],
        block_size: Option<usize>,
        rxmethod: Option<RXMethod>,
    ) -> Result<Gradients, String> {
        bindings::aqaoa::gradients(
            handle,
            num_qubits,
            depth,
            polynomial.keys.as_slice(),
            polynomial.values.as_slice(),
            betas,
            gammas,
            block_size,
            rxmethod,
        )
    }

    fn expectation_value(
        handle: &Handle,
        num_qubits: usize,
        depth: usize,
        polynomial: &Polynomial,
        betas: &[f64],
        gammas: &[f64],
        block_size: Option<usize>,
        rxmethod: Option<RXMethod>,
    ) -> Result<f64, String> {
        bindings::aqaoa::expval(
            handle,
            num_qubits,
            depth,
            polynomial.keys.as_slice(),
            polynomial.values.as_slice(),
            betas,
            gammas,
            block_size,
            rxmethod,
        )
    }
}
