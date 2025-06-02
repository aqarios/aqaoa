# AqAOA 

> [!TIP]
> **Want to run AqAOA on the cloud?** See the [Usage on AWS](#usage-on-aws) section to learn how to launch an EC2 instance with the simulator preinstalled using the official AMI.

## Table of Contents

1. [Overview](#overview)
2. [Original Project Attribution](#original-project-attribution)
3. [Changes from CUAOA](#changes-from-cuaoa)
4. [Overview](#overview)
5. [Usage on AWS](#usage-on-aws)
6. [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Conda Environment Requirement](#conda-environment-requirement)
   - [Installing from Source](#installing-from-source)
   - [Security Note](#security-note)
   - [Docker Installation](#docker-installation)
   - [Troubleshooting](#troubleshooting)
7. [Usage](#usage)
8. [License and Compliance](#license-and-compliance)
9. [Citation](#citation)

## Original Project Attribution

This project is based on [CUAOA](https://github.com/jflxb/cuaoa). CUAOA is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) files for details.

[![arXiv](https://img.shields.io/badge/arXiv-2407.13012-b31b1b.svg)](https://arxiv.org/abs/2407.13012)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12750207.svg)](https://doi.org/10.5281/zenodo.12750207)

## Changes from CUAOA
- Renamed most user visible instances of `cuaoa` to `aqaoa` in the code
- Renamed internal directory `cuaoa` to [`aqaoa`](./aqaoa)

## Overview

AqAOA is a GPU accelerated QAOA simulation framework utilizing the [NVIDIA CUDA toolkit](https://developer.nvidia.com/cuda-toolkit). This framework offers a complete interface for QAOA simulations, enabling the calculation of (exact) expectation values, direct access to the statevector, fast sampling, and high-performance optimization methods using an advanced state-of-the-art gradient calculation technique. The framework is designed for use in Python and Rust, providing flexibility for integration into a wide range of applications, including those requiring fast algorithm implementations leveraging QAOA at its core.

## Usage on AWS 

[![Launch on AWS](https://img.shields.io/badge/Launch%20on-AWS-orange?logo=amazon-aws&style=for-the-badge)](https://aws.amazon.com/marketplace/pp/prodview-umagmbgnitfe2)

AqAOA is available as a preconfigured Amazon Machine Image (AMI) on the [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-umagmbgnitfe2), allowing you to run high-performance QAOA simulations on GPU-backed EC2 instances with minimal setup.

### Steps to Get Started

1. Go to the [AqAOA AMI on AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-umagmbgnitfe2).
2. Subscribe to the AMI and follow the instructions to launch an EC2 instance.
3. Choose a GPU-enabled EC2 instance type (*see overview below*).
4. Connect to your instance via SSH and start using the AqAOA Python interface.

### Overview of EC2 GPU Instances

Below is an overview of GPU instances. These instances vary by GPU model, memory, and compute power. Choose based on the scale of your simulations:

| Instance       | GPU         | GPU Memory | vCPU | vCPU Memory | Price                                                        |
| -------------- | ----------- | ---------- | ---- | ----------- | ------------------------------------------------------------ |
| `g4dn.xlarge`  | NVIDIA T4   | 16 GiB     | 4    | 16 GiB      | [G4 prices](https://aws.amazon.com/ec2/instance-types/g4/)   |
| `g5.xlarge`    | NVIDIA A10G | 24 GiB     | 4    | 16 GiB      | [G5 prices](https://aws.amazon.com/ec2/instance-types/g5/)   |
| `g6.xlarge`    | NVIDIA L4   | 24 GiB     | 4    | 16 GiB      | [G6 prices](https://aws.amazon.com/ec2/instance-types/g6/)   |
| `g6e.xlarge`   | NVIDIA L40S | 48 GiB     | 4    | 32 GiB      | [G6e prices](https://aws.amazon.com/ec2/instance-types/g6e/) |

> 💡 **Recommended**: Start with `g4dn.xlarge` for general use and scale up for more demanding simulations.

### After Launch

Once the instance is running:

```bash
# Connect to your instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Activate the environment (if not already activated)
conda activate aqaoa

# Run the verification script to ensure everything is working as expected
python ~/verify.py
```

Refer to the [Usage](#usage) section for usage examples.

### Virtual Environment Information

The AqAOA simulator is preinstalled in a Miniforge-based environment (`aqaoa`) which should already be activated when you log in. You generally do **not** need to install AqAOA into a new environment. If a new environment is required, or you do not want to use the provided Miniforge-based environment you can simply install the package using any python dependency manger, e.g. with pip simply run:

```bash
pip install ~/aqaoa/pyaqaoa-0.1.1-cp311-cp311-linux_x86_64.whl
```

The following prebuilt wheels are available:

- `~/aqaoa/pyaqaoa-0.1.1-cp311-cp311-linux_x86_64.whl`
- `~/aqaoa/pyaqaoa-0.1.1-cp312-cp312-linux_x86_64.whl`

## Installation

To streamline the installation of our project, utilize the [`install.sh`](./install.sh) script. This script automates the process by cloning the repository, building the project, and installing it on your system.
We plan to make AqAOA installable via pip in the upcoming future.

### Prerequisites

Before proceeding with the installation, ensure the following tools are installed on your system:

- [Rust and Cargo](https://www.rust-lang.org/tools/install): Required to compile the Rust libraries.
- [g++](https://gcc.gnu.org/): Required to compile the C++ library.
- [CUDA and nvcc](https://developer.nvidia.com/cuda-downloads): Required for CUDA-accelerated computations and the compilation.
- [git](https://git-scm.com/): Required for cloning the repository.
- [pip](https://pip.pypa.io/en/stable/installing/): Necessary for Python package installations.
- [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html): A crucial tool for environment and package management.
- [uv](https://docs.astral.sh/uv/): Another crucial tool for environment and package management.
- [Python >= 3.11](https://www.python.org/downloads/): Required for running the Python code. Other versions may work but have not been tested.

### Conda Environment Requirement

> [!IMPORTANT] 
> The installation script must be run within an active `conda` environment tailored for this project. If such an environment is not yet set up, follow these instructions to create and activate one:

```sh
# Create a new conda environment
conda create -n your-env-name python=3.11

# Activate the conda environment
conda activate your-env-name
```

Replace `your-env-name` with a desired name for your conda environment.

Within the activated `conda` environment, the script will install the following essential packages:

1. [`custatevec`](https://docs.nvidia.com/cuda/cuquantum/latest/custatevec/index.html): A library for state vector manipulation in CUDA,
2. [`lbfgs`](https://github.com/chokkan/liblbfgs): An implementation of the L-BFGS optimization algorithm in C.

Make sure to read and understand the license of `cuStateVec` prior to running the installation script.

### Installing from Source

To initiate the installation, execute the following command in your terminal:

```sh
./install.sh
```

For a more detailed output during the installation process, include the `--verbose` option:

```sh
./install.sh --verbose
```

### Security Note

> [!CAUTION] 
> Running scripts directly from the internet poses a risk. It is recommended to first download and review the script before execution:

```sh
# Review the script's contents
less install.sh

# Execute the script after review
bash install.sh
```

### Docker Installation

To provide an alternative installation method using Docker, follow the steps below to build and run the AqAOA application within a Docker container.

This section guides you through building the Docker image and running the AqAOA application in a container.

#### Prerequisites

- Ensure that Docker is installed on your system. You can download it from the [official Docker website](https://www.docker.com/get-started).
- Verify that your system has an NVIDIA GPU and that the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) is installed to enable GPU support within Docker containers.

#### Building the Docker Image

Open a terminal and navigate to the root directory of the AqAOA project. Then, execute the following command to build the Docker image:

```bash
docker buildx build --tag aqaoa-image --load .
```

This command uses Docker Buildx to build the image and tags it as `aqaoa-image`.

#### Running the Docker Container

After successfully building the image, run the following command to start a container:

```bash
docker run --rm -it --gpus all aqaoa-image
```

This command runs the `aqaoa-image` container interactively with access to all available GPUs.

**Parameters Explained:**

- `--rm`: Automatically removes the container when it exits. This option is optional but helps prevent clutter from stopped containers.
- `-it`: Allocates a pseudo-TTY and keeps STDIN open, allowing interactive terminal access.
- `--gpus all`: Grants the container access to all available GPU devices.

For more detailed information on these and other Docker run options, please refer to the [Docker CLI documentation](https://docs.docker.com/engine/reference/commandline/run/).

By following these steps, you can build and run the AqAOA application within a Docker container, leveraging your system's GPU resources. 

### Troubleshooting

> [!TIP] 
> If you encounter any issues during installation:
>
> - Double-check the [prerequisites](#prerequisites) to ensure all necessary tools are installed.
> - Verify that the `conda` environment is activated before running the installation script.
> - Review permissions if encountering errors related to script execution. Adjusting script permissions with `chmod +x install.sh` may be required.

For further assistance, please visit our [Issues page](https://github.com/aqarios/aqaoa/issues) and describe the problem you're facing. We are committed to providing support and resolving installation queries.

## Usage

With AqAOA installed, you can start simulating QAOA. The essential steps for a simulation are:

1. Define the objective and convert it to one of the expected formats.
2. Create the handle required for interactions with the simulator.
3. Create the AqAOA class to access the simulator's functionality.

First, we define a simple MaxCut problem and use it throughout this usage guide. We will focus on creating the problem from the graph's adjacency matrix.

```python
import numpy as np
import pyaqaoa

W = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]])

# Initialize the AqAOA class with the optimization problem.
# For further initialization options, please refer to the AqAOA interface.
sim = pyaqaoa.AqAOA(W, depth=2)

# Create the handle for interactions with the simulator. We must specify the minimum 
# number of qubits required during the simulations using the given handle. 
# As the current MaxCut problem consists of 3 nodes, we set this value to 3. 
# Setting it to a higher value than needed will not affect the correctness of the 
# simulations but will consume more memory.
num_qubits = 3
handle = pyaqaoa.create_handle(num_qubits)

expectation_value = sim.expectation_value(handle)  # Calculate the expectation value.
print(expectation_value)
# -1.3724677

sv = sim.statevector(handle)  # Retrieve the state vector.
print(sv)

sampleset = sim.sample(handle, num_shots=1)  # Obtain samples.
# The sampling process can also be seeded using the `seed` parameter:
# sampleset = sim.sample(handle, num_shots=1, seed=...)

# To access the samples in the sample set, use:
samples = sampleset.samples()
print(samples)
# [[False True True]]
# The objective value associated with each sample set can be accessed with:
costs = sampleset.energies()
print(costs)
# [-1]

gradients, ev = sim.gradients(handle)  # Calculate the gradients.
# Calculating the gradients will also compute the respective expectation value.
# You can also calculate the gradients for a given set of parameters with:
# gradients, ev = sim.gradients(
#     handle, 
#     betas=np.array([0.0, 1.0]), 
#     gammas=np.array([0.4, 1.3])
# )
# To access the gradients, you can use:
print(gradients.betas)
# [ 0.52877299 -0.86224096]
print(gradients.gammas)
# [-0.35863235 -0.50215632]

optimize_result = sim.optimize(
    handle
)  # Optimize the parameters using the built-in optimizer.
# This runs the optimization with default parameters. You can also control the 
# optimization by passing a `pyaqaoa.LBFGSParameters` object, for example:
# optimize_result = sim.optimize(
#     handle, 
#     lbfgs_parameters=pyaqaoa.LBFGSParameters(max_iterations=10)
# )
# The optimized parameters are automatically set in the `sim` object but can be 
# accessed with: 
# `optimize_result.parameters.betas` and 
# `optimize_result.parameters.gammas`.

# We can now recalculate the expectation value to see the effect:
expval_after_optimization = sim.expectation_value(handle)
print(expval_after_optimization)
# -1.99999999

# Sampling after optimization now also gives us the expected results:
sampleset_after_optimization = sim.sample(handle, num_shots=1)
print(sampleset_after_optimization.samples())
# array([[False, True, False]])
```

To use `AqAOA` with an arbitrary optimization problem, you can use the `from_map` function. For example, for the MaxCut problem used in the previous example:

```python
terms = {
    (0, 1): 2.0, (1, 2): 2.0,
    (0,): -1.0, (1,): -2.0, (2,): -1.0
}
sim = pyaqaoa.AqAOA.from_map(num_qubits, terms, depth=2)
```

The remaining interactions with the `sim` object remain the same.

To release the allocated memory you can use the `.destory()` method on the handle:

```python
handle.destroy()
```


## License and Compliance

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

By using this software, you agree to comply with the licenses of all dependencies used in this project. Notably, the `cuStateVec` library has its own licensing terms which must be adhered to.

- [`cuStateVec License`](https://docs.nvidia.com/cuda/cuquantum/latest/custatevec/license.html)

## Citation

This project is a derivative of [CUAOA](https://github.com/jflxb/cuaoa). If you use this software in your research or publication, please cite both the original authors and this derivative:

### Original Project Citation

Please cite the original work by CUAOA authors as follows:

```bibtex
@misc{stein2024cuaoanovelcudaacceleratedsimulation,
      title={CUAOA: A Novel CUDA-Accelerated Simulation Framework for the QAOA}, 
      author={Jonas Stein and Jonas Blenninger and David Bucher and Josef Peter Eder and Elif Çetiner and Maximilian Zorn and Claudia Linnhoff-Popien},
      year={2024},
      eprint={2407.13012},
      archivePrefix={arXiv},
      primaryClass={quant-ph},
      url={https://arxiv.org/abs/2407.13012}, 
}
```

```bibtex
@software{blen_CUAOA_2024,
  author={Blenninger, Jonas and
                  Stein, Jonas and
                  Bucher, David and
                  Eder, Peter J. and
                  Çetiner, Elif and
                  Zorn, Maximilian and
                  Linnhoff-Popien, Claudia},
  title={{CUAOA: A Novel CUDA-Accelerated Simulation Framework for the QAOA}},
  month=jul,
  year=2024,
  publisher={Zenodo},
  version={0.1.0},
  doi={10.5281/zenodo.12750207},
  url={https://doi.org/10.5281/zenodo.12750207}
}
```

