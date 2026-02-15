import pandas as pd
from .excel import read_from_excel
from . import json
from pslib.system import PowerSystem
from pslib.models.bus import Bus
from pslib.models.branch import Branch
from pslib.models.generator import Generator


__all__ = ['excel']

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
    system = PowerSystem()

    model_objects = {}
    for key, cls in name_to_class.items():
        model_objects[key]=  column_to_obj(data[key], cls)
        
    return PowerSystem(**model_objects)
     