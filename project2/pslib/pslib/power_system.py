import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import json
from pslib.models import bus, generator, branch 
import parsers
from parsers import excel, json, column_to_obj
from pslib.parsers import create_system_from_data, read_from_excel
from pslib.parsers.excel import read_from_excel
from pslib import plot, print_data


# read power system data from an excel file
data = excel.read_from_excel("case14.xslx")
print_data(data)

# Save data to a json file
json.save_to_json(data = data, path = "power_system_data.json")

# load data from a json file
data = parsers.json.load_data_from_json("power_system_data.json")
print_data(data)

bus = column_to_obj(data['bus'], bus.Bus)
branch = column_to_obj(data['branch'], branch.Branch)
generator = column_to_obj(data['gen'], generator.Generator)

# verification code
print(bus.Vm[0])
print(branch.angmax[0])
print(generator.Pmax[0])

# plot bus voltage -- uncomment
# plot_bus_voltage(bus)

# Plot with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12,5))

# voltage magnitude plot
ax1.plot(bus.bus_i, bus.Vm, 'r-o')
ax1.set_xlabel('Bus Number')
ax1.set_ylabel('Voltage Magnitude (p.u.)')
ax1.set_title('Bus Voltage Magnitude Plot')
ax1.grid()

# voltage angle plot
ax2.plot(bus.bus_i, bus.Va, 'r-o')
ax2.set_xlabel('Bus Number')
ax2.set_ylabel('Voltage Angle (deg)')
ax2.set_title('Bus Voltage Angle Plot')
ax2.grid()

fig.suptitle("Bus Voltage and Magnitude Plots")

plt.tight_layout()

# save the plot
plt.savefig('bus voltage and magnitude plot', dpi=400, format="png", bbox_inches="tight")

# plt.show()

# create an HTML based interactive plot
plot.interactive_plot(bus)