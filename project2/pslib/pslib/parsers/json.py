import json
import pandas as pd

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