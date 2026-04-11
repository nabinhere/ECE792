class BaseModel:
    """
    Base class for all (power flow) models
    """

    def __init__(self):
        self.addresses = {}
        self.values = {}

    def get_count(self):
        """
        Return the number of variables in the model
        """
        raise NotImplementedError
    
    def register_address(self, dae):
        """
        Register the addresses of the variables in the model
        """
        raise NotImplementedError
    
    def fetch_address(self, dae):
        """
        Fetch the addresses of the variables in the model
        """
        raise NotImplementedError