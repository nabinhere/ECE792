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
    file_dict = pd.read_excel("case14.xlsx", sheet_name = ['bus', 'branch', 'gen'], 
                         header = 0, )
    return file_dict

if __name__ == "__main__":
    data = read_from_excel("case14.xslx")
    print(data)

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
    print(f"\n Type of branch df: {type(branch_df)}")
