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