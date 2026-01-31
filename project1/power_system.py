import pandas as pd
import matplotlib.pyplot as plt
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

def column_to_obj(df, cls):
    obj_dict = {}
    for col in df.columns:
        obj_dict[col] = df[col].tolist()
    return cls(**obj_dict)


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




