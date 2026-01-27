import pandas as pd
import matplotlib as plt

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