import pybamm

param = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020)

model = pybamm.lithium_ion.DFN()
# get the list of input parameters for a given model
model.print_parameter_info()

sim = pybamm.Simulation(model, parameter_values=param)
sim.solve([0, 3600])
sim.plot()


# get the list of all the variables that can be computed in the model
model.variable_names()

# command to search variable
model.variables.search("electrolyte")

# retrieve the solution. It is dictionary
sol = sim.solution

# We retrive som variable from the solution dictionnary
t = sol['Time [s]']

# to finally recover the values
t.entries






