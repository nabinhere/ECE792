import numpy as np

class DAE:
    def __init__(self):
        self.addresses = {}
        self.next_addresses = {}

        self.g = {}
        self.y = {}

    def initialize_arrays(self):
         self.g = np.array(self.next_addresses["AlgebEqn"])
         self.y = np.array(self.next_addresses["AlgebVar"])

    def register_address(self, model_name: str, type_name: str, var_dict: dict[str, int])-> None:
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
            internal bus numbers for the given variables
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
                self.addresses[model_name][type_name][name] = np.arange(self.next_addresses[type_name],
                                                                        self.next_addresses[type_name] + size)
                self.next_addresses[type_name] += size


    def get_address(self, model_name: str, type_name: str, name: str, index: int | list[int] | range | np.ndarray = None):
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
        addr_array = self.addresses[model_name][type_name][name]

        # return entire array address if index is not provided
        if index is None:
             return addr_array
        
        if isinstance(index, (int, np.integer)):
             return addr_array[index]
        
        if isinstance(index, (list, range, np.ndarray)):
             return addr_array[index]
        
        raise ValueError(f"Index must be integer, list, range, or numpy array. Got {type(index)}.")
    
    def system_residuals(y0):
         """
         Compute the residuals of the whole system model.

         Parameters
         --------------
         y0: numpy array
            Residuals of the system model having the same length as 'y0'.
         """
         pass
