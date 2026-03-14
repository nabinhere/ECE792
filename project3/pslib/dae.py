import numpy as np

class DAE:
    def __init__(self):
        self.m = 0  # next available address
        self.nvar = 0
        self.eqn_address = {}
        self.var_address = {}

        self.addresses = {}
        self.next_addresses = {}


    def register_address(self, model_name: str, type_name: str, var_dict: dict[str, int], bus_int: list)-> None:
        """
        Register equation and variable addresses for a given model

        Parameters
        --------------
        model_name: str
            Name of the model (e.g., Bus)
        type_name: str
            Full type name (e.g., "AlgebEqn", "StateVar", "Observed")
        var_dict: dict
            Dictionary variable names and their sizes
        bus_int: list
            internal bus numbersfor the given variables
        """
        # initialize a variable dictionary for a given model
        if model_name not in self.addresses:
            self.addresses[model_name] = {}
        
        # create a specified type of variable for a given model
        if type_name not in self.addresses[model_name]:
            self.addresses[model_name][type_name] = {}

        # Initialize next_address for this type if it doesn't already exist
        if type_name not in self.next_addresses:
            self.next_addresses[type_name] = 0

        # Assign variable/equation addresses
        for name, size in var_dict.items():
            if name not in self.addresses[model_name][type_name]:
                self.addresses[model_name][type_name][name] = {}
            
            # initialize the address dict to be assigned
            address_dict = {}
            address_range = range(self.next_addresses[type_name], self.next_addresses[type_name] + size)
            self.next_addresses[type_name] += size

            for i, val in enumerate(bus_int):
                address_dict[val] = address_range[i]
            
            self.addresses[model_name][type_name][name].update(address_dict)

    def get_address(self, model_name: str, type_name: str, name: str, bus_no):
        """
        Get the address of a type (equation, variable, etc.)

        Parameters
        --------------
        model_name: str
            Name of the model (e.g., Bus)
        type_name: str
            Full type name (e.g., "AlgebEqn", "StateVar", "Observed")
        var_dict: dict
            Dictionary variable names and their sizes
        bus_int: list
            internal bus numbersfor the given variables
        """

        var_address = []
        for val in bus_no:
            var_address.append(self.addresses[model_name][type_name][name][val])

        return var_address
