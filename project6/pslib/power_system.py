from pslib.parsers import create_system_from_file
from dae import DAE
import numpy as np
from scipy.optimize import fsolve

# numpy print 10 digits
np.set_printoptions(precision=10)

system = create_system_from_file("pslib/data/case3", "xlsx")
dae = DAE()

system.bus.make_int_map()

# First part of the initialization: register addresses
system.bus.register_address(dae)
system.branch.register_address(dae)
system.gen.register_address(dae)

# second part of initialization: fetch addresses
system.bus.fetch_address(dae, system)
system.branch.fetch_address(dae, system)
system.gen.fetch_address(dae, system)

# Make Ybus to prepare for power flow
system.makeYbus()

dae.initialize_arrays()

# properly initialize values
y0 = np.array([0, 0, 0, 1.02, 1.0, 1.0, 0, 0, 0])      # initial values for 3-bus
# y0 = np.concatenate([np.zeros(system.bus.get_count()),     # Va
#                     np.ones(system.bus.get_count()),       # Vm
#                     [0, 0],        # for the slack p and Q
#                     np.zeros(system.gen.get_count())])    # for PV's Q

def system_residuals(y, system, dae):
    dae.y[:] = y
    dae.g[:] = 0

    system.bus.fetch_values(dae)
    system.branch.fetch_values(dae)
    system.gen.fetch_values(dae)

    # calculate residual contributions of each model
    system.bus.calc_g(system)
    system.branch.calc_g(system)
    system.gen.calc_g(system)

    system.bus.merge_g(dae)
    system.branch.merge_g(dae)
    system.gen.merge_g(dae)

    return np.array(dae.g)

sol, infodict, ier, mesg = fsolve(system_residuals, y0, args = (system, dae), full_output = True)
print(sol)
print(infodict)
print(ier)
print(mesg)