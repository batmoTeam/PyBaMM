import pybamm
import numpy as np
import os
import matplotlib.pyplot as plt
os.chdir(pybamm.__path__[0]+'/..')

# create the model
model = pybamm.lithium_ion.DFN()
model.print_parameter_info()

# set the default model geometry
geometry = model.default_geometry
paramDefault = model.default_parameter_values

# set the default model parameters
paramChen = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020)

# paramChen.process_model(model)
# model.print_parameter_info()
