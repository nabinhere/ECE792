import numpy as np

class DAE:
    def __init__(self):
        self.m = 0  # next available address
        self.eqn_address = {}

    def register_eqn(self, model_name: str, var_type: str, eqn_dict: dict, bus_int):
        """
        register a specified type of equations for a given model 
        """
        # initialize a dictionary for a given model
        if model_name not in self.eqn_address:
            self.eqn_address[model_name] = {}
        
        # create a specified type of equation for a given model
        if var_type not in self.eqn_address[model_name]:
            self.eqn_address[model_name][var_type] = {}

        # Assign equation addresses
        for eqn_name, num_eqn in eqn_dict.items():
            if eqn_name not in self.eqn_address[model_name][var_type]:
                self.eqn_address[model_name][var_type][eqn_name] = {}
            
            address_dict = {}
            eqn_address = range(self.m, self.m+num_eqn)
            self.m += num_eqn
            for i, val in enumerate(bus_int):
                address_dict[val] = eqn_address[i]

            self.eqn_address[model_name][var_type][eqn_name].update(address_dict)


    def get_eqn_address(self, model_name: str, var_type: str, var_name: str, bus_no):
        """Get the address of the equation that is initially registered by 
        a given model using a model, variable type, variable name, bus numbers
        
        Parameters
        -----------
        model_name: str
            name of the power system model
        
        var_type: str
            Type of variable. Can be either algebraic or differential

        var_name: str
            Variable name
        
        bus_no: int or np.ndarray
            internal bus number associated witht the given model

        Returns
        -----------
        np.ndarray of addresses of var_name equation of type var_type affected by model model_name
        """
        eqn_address = []
        for val in bus_no:
            eqn_address.append(self.eqn_address[model_name][var_type][var_name][val])

        return eqn_address