import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import json
from bus import Bus
from generator import Generator
from branch import Branch

def read_from_excel(path: str)->dict:
    """
    Read power system data from Excel file.

    parameters
    -----------
    path: str
        path to the Excel file
    Returns
    --------
    dict
        Dictionary containing three pandas DataFrames
        -bus: Dataframe
            cotains bus data
        -gen: DataFrame
            contains bus data
        - branch: DataFrame
            contains branch data
    """
    file_dict = pd.read_excel("case14.xlsx", sheet_name = None, 
                         header = 0)
    return file_dict

def save_to_json(data: dict, path: str)->None:
    """
    Save data dictionary to json file

    Parameters
    -----------
    data: dict
        dictionary containing three pandas DataFrames: 
            - bus, gen, and branch
    
    path: str
        string containing the relative path to save the json file

    """
    data_dict = {}
    for key in data.keys():
        data_dict[key] = data[key].to_dict()
    
    with open(path, 'w') as json_file:
        json_file.write(json.dumps(data_dict))

def load_data_from_json(file_path: str) -> dict:
    """
    Load data from json file and convert into a dictionary of dataframes
    
    Parameters
    -----------
    file_path: str
        relative path to the json file
    
    Return
    ----------
    dict
        Dictionary containing three pandas DataFrames
        -bus: Dataframe
            cotains bus data
        -gen: DataFrame
            contains bus data
        - branch: DataFrame
            contains branch data
    """
    data_dict = {}
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        for key in data.keys():
            data_dict[key] = pd.DataFrame(data[key])
    
    return data_dict

def print_data(data: dict)->None:
    """
    Print Power system data

    Parameters
    ------------
    data: dict
        Dictionary containing three pandas DataFrames
        -bus: Dataframe
            cotains bus data
        -gen: DataFrame
            contains bus data
        - branch: DataFrame
            contains branch data
    """

    # Access individual DataFrames
    bus_df = data['bus']
    gen_df = data['gen']
    branch_df = data['branch']

    # print first few rows of each DataFrame
    print("\nBus Data:")
    print(bus_df.head())
    print("\nGenerator Data:")
    print(gen_df.head())
    print("\nBranch Data:")
    print(branch_df.head())

def column_to_obj(df:pd.DataFrame, cls:object)->object:
    """
    Convert DataFrames into objects

    Parameters
    --------------
    df: pd.DataFrame
        pandas DataFrame containing the power system component information
    cls: 
        class   

    Returns
    -----------
    an instance of the cls with parameters unpacked from df
    """
    obj_dict = {}
    for col in df.columns:
        obj_dict[col] = df[col].tolist()
    return cls(**obj_dict)

def plot_bus_voltage(bus: object)->None:
    """
    Plot bus voltage using matplotlib.pyplot

    Parameter
    -------------
    bus: object
        an instalce of the Bus class
    """
    plt.figure(figsize=(10, 6))
    plt.plot(bus.bus_i, bus.Vm, 'b-o', label = 'Voltage Magnitude')
    plt.xlabel('Bus Number')
    plt.ylabel('Voltage Magnitude')
    plt.title('Bus Voltage Magnitude Plot')
    plt.legend('Vmag')
    plt.grid()

    # save the plot
    plt.savefig('bus_voltage_magnitude_plot', dpi=400, format="png", bbox_inches="tight")

    plt.show()

def interactive_plot(bus: object):
    """
    Create Interactive plot using plotly.graph_objects

    Parameter
    ------------
    bus: object
        as instance of the Bus class
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=bus.bus_i, y=bus.Vm, name="Voltage Magnitude"))

    fig.update_layout(
        title="Bus Voltage Profile",
        xaxis_title="Bus Number",
        yaxis_title="Voltage (p.u.)"
    )  

    # save as HTML file
    fig.write_html("voltage_profile_interactive.html")
    
    
if __name__ == "__main__":
    # read power system data from an excel file
    data = read_from_excel("case14.xslx")
    print_data(data)

    # Save data to a json file
    save_to_json(data = data, path = "power_system_data.json")

    # load data from a json file
    data = load_data_from_json("power_system_data.json")
    print_data(data)

    bus = column_to_obj(data['bus'], Bus)
    branch = column_to_obj(data['branch'], Branch)
    generator = column_to_obj(data['gen'], Generator)

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
    interactive_plot(bus)