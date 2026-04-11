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
    
    def fetch_address(self, dae):
        """
        Fetch the addresses of the variables in the model
        """
        raise NotImplementedError
    
    def resolve_incdices(self, system):
        """
        Resolve the indices of the variables
        """
        raise NotImplementedError
    
    