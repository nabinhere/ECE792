import numpy as np

class Bus:
    def __init__(self, bus_i, type, Pd, Qd, Gs, Bs,
                 area, Vm, Va, baseKV, zone, Vmax, Vmin):
        self.bus_i = bus_i
        self.type = type
        self.Pd = Pd
        self.Qd = Qd
        self.Gs = Gs
        self.Bs = Bs
        self.area = area
        self.Vm = Vm
        self.Va = Va
        self.baseKV = baseKV
        self.zone = zone
        self.Vmax = Vmax
        self.Vmin = Vmin

        self._int_map = {}
        self.ext_numbers = bus_i

        self.eqn_address = {}
    
    def get_count(self):
        return len(self.bus_i)
    
    def ext2int(self, ext_numbers):
        """
        Convert an array of external bus numbers to internal bus numbers.
        """
        self.ext_numbers = ext_numbers
        return np.vectorize(self._int_map.get)(ext_numbers)
    
    def make_int_map(self):
        """
        Make the map from external bus number to internal bus number.

        This function should be called before adding all bus data
        """
        self._int_map = {}
        for i, ext_number in enumerate(self.ext_numbers):
            self._int_map[ext_number] = i

    def register_address(self, dae):
        """
        Register variables and equations for the buses
        """
        # register equations
        dae.register_address("Bus", "AlgebEqn", 
                         {"P_balance": self.get_count(),
                          "Q_balance": self.get_count(),
                          "Vm_diff": self.type.count(3),
                          "Va_diff": self.type.count(3)})
        
        # register variables
        dae.register_address("Bus",
                             "AlgebVar",
                             {"Va": self.get_count(),
                             "Vm": self.get_count(),
                             "P_slack": self.type.count(3),
                             "Q_slack": self.type.count(3)})
        
        
    def fetch_address(self, dae, system):
        # fetch variable and equation addresses for the buses

        self.adresses = {
            "AlgebEqn": {
                "P_balance": dae.get_address("Bus", "AlgebEqn", "P_balance"),
                "Q_balance": dae.get_address("Bus", "AlgebEqn", "Q_balance"),
                "Vm_diff": dae.get_address("Bus", "AlgebEqn", "Vm_diff"),
                "Va_diff": dae.get_address("Bus", "AlgebEqn", "Va_diff"),
            },
            "AlgebVar": {
                "Va": dae.get_address("Bus", "AlgebVar", "Va"),
                "Vm": dae.get_address("Bus", "AlgebVar", "Vm"),
                "P_slack": dae.get_address("Bus", "AlgebVar", "P_slack"),
                "Q_slack": dae.get_address("Bus", "AlgebVar", "Q_slack"),
            },
        }