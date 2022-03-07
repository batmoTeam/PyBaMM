import matplotlib.pyplot as plt
import numpy as np
import pybamm
import logging
import importlib

importlib.reload(pybamm)

plt.close('all')

# h = logging.FileHandler("logtest", mode='w')
# pybamm.logger.addHandler(h)
# pybamm.set_logging_level("VERBOSE")

param = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020)

param['Negative electrode diffusivity [m2.s-1]'] = 1e1
param['Positive electrode diffusivity [m2.s-1]'] = 1e1

CRates = [0.1, 1, 2]
sols = list()

CRate = CRates[1]
CRate = 1

param['Current function [A]'] = 5 * CRate

model = pybamm.lithium_ion.DFN()

# get the list of input parameters for a given model
model.print_parameter_info()

sim = pybamm.Simulation(model, parameter_values=param)
n = 100

t_eval = np.linspace(0, 3600 / CRate, n)
t_eval = np.concatenate([t_eval, [0.1]])
t_eval = np.sort(t_eval)

sol = sim.solve(t_eval)
plt.ion()

sim.plot()

##


def getfirst(varname):
    u = sol[varname].entries
    return u[:, 1]


def getstr(varabrev, varname):
    u = getfirst(varname)
    u = "{0} = [".format(varabrev) + ",".join(["{0}".format(val) for val in u]) + "];\n"
    return u


def gettstr(varabrev, varname):
    u = sol[varname].entries
    u = "{0} = [".format(varabrev) + ",".join(["{0}".format(val) for val in u]) + "];\n"
    return u

u_e_sep = getfirst('Separator electrolyte potential [V]')
u_p = getfirst('Positive electrode potential [V]')
u_n = getfirst('Negative electrode potential [V]')
u_e_p = getfirst('Positive electrolyte potential [V]')
u_e_n = getfirst('Negative electrolyte potential [V]')
u_cc_n = sol['Negative current collector potential [V]']

with open('readme.m', 'w') as f:
    f.write(getstr('x_n_pybamm', 'x_n [m]'))
    f.write(getstr('x_p_pybamm', 'x_p [m]'))
    f.write(getstr('u_e_sep_pybamm', 'Separator electrolyte potential [V]'))
    f.write(getstr('u_p_pybamm', 'Positive electrode potential [V]'))
    f.write(getstr('u_n_pybamm', 'Negative electrode potential [V]'))
    f.write(getstr('u_e_p_pybamm', 'Positive electrolyte potential [V]'))
    f.write(getstr('u_e_n_pybamm', 'Negative electrolyte potential [V]'))
    f.write(gettstr('t_pybamm', 'Time [s]'))
    f.write(gettstr('u_pybamm', 'Terminal voltage [V]'))
##

plt.close('all')

plt.figure()
plt.plot(u_p, label='electrode')
plt.plot(u_e_p, label='electrolyte')
plt.title('Positive electrode')
plt.legend()

plt.figure()
plt.plot(u_p - u_p[0], label='electrode')
plt.plot(u_e_p - u_e_p[0], label='electrolyte')
plt.title('Positive electrode (difference with value at origin)')
plt.legend()

plt.figure()
plt.plot(u_n, label='electrode')
plt.plot(u_e_n, label='electrolyte')
plt.title('Negative electrode')
plt.legend()

plt.figure()
plt.plot(u_e_sep)
plt.title('separator')
plt.legend()


##
plt.figure()
plt.plot(u_n)
plt.title('potential negative electrode')


##


u = sol['Terminal voltage [V]'].entries
t = sol['Time [s]'].entries

with open('readme.txt', 'w') as f:
    f.write('t = [')
    for tt in t:
        f.write("{0}, ".format(tt))
    f.write('\n\nu = [')
    for uu in u:
        f.write("{0}, ".format(uu))
