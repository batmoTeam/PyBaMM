import pybamm
import numpy as np
import os
import matplotlib.pyplot as plt
os.chdir(pybamm.__path__[0] + '/..')

pybamm.set_logging_level("VERBOSE")

# create the model
model = pybamm.lithium_ion.DFN()

# set the default model geometry
geometry = model.default_geometry

# set the default model parameters
param = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020)

# set the parameters for the model and the geometry
param.process_model(model)
param.process_geometry(geometry)

# example to get value of a variable after processing
model.variables['Negative electrode surface area to volume ratio [m-1]']
model.variables['Positive electrode surface area to volume ratio [m-1]']

# j0_p = param.gamma_p * param.j0_p(c_e_p, c_s_surf_p, T) / param.C_r_p
param.process_symbol(model.param.gamma_p)
param.process_symbol(model.param.C_r_p)
param.process_symbol(model.param.j0_p_dimensional)
#self.j0_p_dimensional(c_e_dim, c_s_surf_dim, T_dim) / self.j0_p_ref_dimensional
param.process_symbol(model.param.j0_p_ref_dimensional)

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

t = solution["Time [h]"]
u = solution["Terminal voltage [V]"]
