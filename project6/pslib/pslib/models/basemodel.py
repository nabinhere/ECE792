class BaseModel:
    """
    Base class for all (power flow) models
    """

    def __init__(self):
        self.reg_data = {}
        self.fetch_data = {}
        
        self.addresses = {}
        self.values = {}

        # Automatically get model name from class name
        self.model_name = self.__class__.__name__

    def get_count(self):
        """
        Return the number of variables in the model
        """
        raise NotImplementedError
    
    def register_address(self, dae):
        """
        Register the addresses of the variables in the model
        """
        if not self.reg_data:
            return
        
        for type_name, name_to_size in self.reg_data.items():
            dae.register_address(self.__class__.__name__,
                                 type_name, name_to_size)
    
    def fetch_address(self, dae, system):
        """
        Fetch the addresses of the variables in the model using metadata
        """
        if not self.fetch_data:
            return
        
        # Allow model to resolve any dynamic indices
        self.resolve_indices(system)

        self.addresses = {}
        for type_name, var_info in self.fetch_data.items():
            self.addresses[type_name] = {}
            for dest_name, (src_model, src_name, index) in var_info.items():
                self.addresses[type_name][dest_name] = dae.get_address(
                    src_model, type_name, src_name, index
                )
    
    def fetch_values(self, dae):
        """
        Fetch the values of the variables in the model
        """
        self.values = {}

        # Give aliases for convenience
        sa = self.addresses
        sv = self.values

        # Only fetch AlgebVar values as that's what DAE currently supports
        if "AlgebVar" in sa:
            sv["AlgebVar"] = { }
            for v_name, addr in sa["AlgebVar"].items():
                sv["AlgebVar"][v_name] = dae.get_var_values("AlgebVar", addr) 
    
    def merge_g(self, dae):
        """
        Merge the residual contributions to the global 'dae.g' array.

        This generic implementation works for all models by iterating through all equation types and 
        names in self.addresses and adding the corresponding values to dae.g.
        """
        if "AlgebEqn" not in self.addresses:
            return
        if "AlgebEqn" not in self.values:
            return
        
        address = self.addresses["AlgebEqn"]
        value = self.values["AlgebEqn"]

        # Iterate through all equation names
        for eqn_name in address:
            if eqn_name in value:
                dae.g[address[eqn_name]] += value[eqn_name]
    
    def resolve_indices(self, system):
        """
        Resolve the indices of the variables
        """
        raise NotImplementedError
    
