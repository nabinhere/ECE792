import os
import pathlib
import pandas as pd
from .excel import read_from_excel
from .json import load_data_from_json
from pslib.system import PowerSystem
from pslib.models.bus import Bus
from pslib.models.branch import Branch
from pslib.models.generator import Generator


__all__ = ['excel', 'json']

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


name_to_class = {
    'bus': Bus,
    'branch': Branch,
    'gen': Generator
}


def create_system_from_data(data: dict) -> PowerSystem:
    """
    Convert raw data dict to PowerSystem object.

    Parameters
    ------------
    data: dict
        Dictionary of Dataframes from read_from_excel()

    Returns
    ----------
    PowerSystem
        Initialized system object with vectorized components
    """
    system = PowerSystem(data['bus'], data['branch'], data['gen'])

    model_objects = {}
    for key, cls in name_to_class.items():
        model_objects[key]=  column_to_obj(data[key], cls)
        
    return PowerSystem(**model_objects)

# create system directly from the file
def create_system_from_file(file_path:str, sugg_type:str|None = None)->PowerSystem:
    """
    Create a PoserSystem object directly from a file

    Parameters
    -------------
    file_path: str
        path to the raw data file
    sugg_type: str, optional
        suggested type of the file from the user
    """
    # If provided, use the suggested file type
    if sugg_type:
        file_type = sugg_type.lower()
    else:
        file_type = pathlib.Path(file_path).suffix.lower()
        file_type = file_type.split(".")[-1]
    
    if file_type in ["xlsx", "xls", "excel"]:
            data = read_from_excel(file_path)
    elif file_type == "json":
        data = load_data_from_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    return create_system_from_data(data)
    

        



     