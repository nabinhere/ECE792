import pandas as pd
import matplotlib as plt
import json

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



if __name__ == "__main__":
    data = read_from_excel("case14.xslx")

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

    # Save data to a json file
    save_to_json(data = data, path = "power_system_data.json")
