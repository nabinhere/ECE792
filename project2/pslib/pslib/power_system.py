from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import json
from pslib.models import bus, generator, branch 
from pslib import parsers
from pslib.parsers import excel, json, column_to_obj
from pslib.parsers import create_system_from_data, read_from_excel, create_system_from_file
from pslib.parsers.excel import read_from_excel
from pslib import plot, print_data


current_dir = Path(__file__).parent
parent_dir = current_dir.parent
file_path = parent_dir/"data"/"case3.xlsx"
system = create_system_from_file(file_path)
system.bus.make_int_map()

Ybus = system.makeYbus()
print(Ybus)


# bus = system.bus
# branch = system.branch
# generator = system.gen


# # # verification code
# print(bus.Vm[0])
# print(branch.angmax[0])
# print(generator.Pmax[0])


# # # Plot with subplots
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12,5))

# # voltage magnitude plot
# ax1.plot(bus.bus_i, bus.Vm, 'r-o')
# ax1.set_xlabel('Bus Number')
# ax1.set_ylabel('Voltage Magnitude (p.u.)')
# ax1.set_title('Bus Voltage Magnitude Plot')
# ax1.grid()

# # voltage angle plot
# ax2.plot(bus.bus_i, bus.Va, 'r-o')
# ax2.set_xlabel('Bus Number')
# ax2.set_ylabel('Voltage Angle (deg)')
# ax2.set_title('Bus Voltage Angle Plot')
# ax2.grid()

# fig.suptitle("Bus Voltage and Magnitude Plots")

# plt.tight_layout()

# # # save the plot
# plt.savefig('bus voltage and magnitude plot', dpi=400, format="png", bbox_inches="tight")

# plt.show()

# # # # create an HTML based interactive plot
# # # plot.interactive_plot(bus)