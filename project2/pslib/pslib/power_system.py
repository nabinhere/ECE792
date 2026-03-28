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
from pslib.plot import plot_bus_voltage, interactive_plot


current_dir = Path(__file__).parent
parent_dir = current_dir.parent
file_path = parent_dir/"data"/"case3.xlsx"
system = create_system_from_file(file_path)
system.bus.make_int_map()

Ybus = system.makeYbus()
print(Ybus)

