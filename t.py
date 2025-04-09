import numpy as np
import pyaqaoa

W = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0]])

# Initialize the aqaoa class with the optimization problem.
# For further initialization options, please refer to the aqaoa interface.
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

