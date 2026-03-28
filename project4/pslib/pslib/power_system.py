from pslib.dae import DAE
from .parsers import create_system_from_file

system = create_system_from_file("pslib/data/case3.xlsx", "xlsx")
dae = DAE()

system.bus.make_int_map()

# First part of the initialization: register addresses
system.bus.register_address(dae)
system.branch.register_address(dae)
system.gen.register_address(dae)

# second part of the initialization: fetch addresses
system.bus.fetch_address(dae, system)
system.branch.fetch_address(dae, system)
system.gen.fetch_address(dae, system)

# Make Ybus to prepare for power flow
system.makeYbus()




