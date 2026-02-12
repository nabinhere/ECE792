import pandas as pd
from . import excel
from . import json

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