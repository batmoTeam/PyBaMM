import pybamm
import numpy as np
import os
import matplotlib.pyplot as plt
os.chdir(pybamm.__path__[0]+'/..')

# create the model
model = pybamm.lithium_ion.DFN()

# set the default model geometry
geometry = model.default_geometry

# set the default model parameters
param = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020)

# set the parameters for the model and the geometry
param.process_model(model)
param.process_geometry(geometry)

# mesh the domains
mesh = pybamm.Mesh(geometry, model.default_submesh_types, model.default_var_pts)

# discretise the model equations
disc = pybamm.Discretisation(mesh, model.default_spatial_methods)
disc.process_model(model)

# Solve the model at the given time points
solver = model.default_solver
n = 100
t_eval = np.linspace(0, 3600, n)
solution = solver.solve(model, t_eval)
