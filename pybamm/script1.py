import matplotlib.pyplot as plt
import numpy as np
import pybamm
import logging

plt.close('all')

h = logging.FileHandler("logtest", mode = 'w')
pybamm.logger.addHandler(h)
pybamm.set_logging_level("VERBOSE")

param = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020)

param['Negative electrode diffusivity [m2.s-1]'] = 1
param['Positive electrode diffusivity [m2.s-1]'] = 1

CRates = [0.1, 1, 2]
sols = list()

for CRate in CRates:
    param['Current function [A]'] = 5 * CRate

    model = pybamm.lithium_ion.DFN()

    # get the list of input parameters for a given model
    model.print_parameter_info()

    sim = pybamm.Simulation(model, parameter_values=param)
    n = 100
    t_eval = np.linspace(0, 3600 / CRate, n)
    sol = sim.solve(t_eval)
    t = sol["Time [h]"]
    u = sol["Terminal voltage [V]"]
    sols.append({'t' : t, 'u': u})

plt.ion()

# sim.plot()

# get the list of all the variables that can be computed in the model
model.variable_names()

# command to search variable
model.variables.search("electrolyte")

# retrieve the solution. It is dictionary
# sol = sim.solution

# We retrive som variable from the solution dictionnary
t = sol['Time [s]']

# to finally recover the values
t.entries

v = sol['Negative electrode surface area to volume ratio [m-1]']

v1 = sol['Maximum negative particle surface concentration [mol.m-3]']
v2 = sol['Maximum negative particle concentration [mol.m-3]']

plt.figure()
ax = plt.gca()
plt.plot(v1.entries, label='surface concentration')
plt.plot(v2.entries, label='concentration')
ax.legend()
ax.set_title('Maximum particle concentration in negative electrode')
plt.figure()
t = sol["Time [h]"]
u = sol["Terminal voltage [V]"]
plt.plot(t.entries, u.entries)

dosave = False

if dosave:
    with open('readme.txt', 'w') as f:
        f.write('t = [')
        for tt in t.entries:
            f.write("{0}, ".format(tt))
        f.write('\n\nu = [')
        for uu in u.entries:
            f.write("{0}, ".format(uu))




