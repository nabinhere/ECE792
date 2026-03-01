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

    def register_equations(self, dae):
        """
        Register Algebraic and Differential equations for the buses
        """

        dae.register_eqn("Bus", "Algeb", 
                         {"P": self.get_count(),
                          "Q": self.get_count()}, self._int_map.values())
        
        dae.register_eqn("Bus", "Algeb", self._int_map.values)
    
    def fetch_equation_address(self, dae, system):
        bus_int = system.bus.ext2int(self.bus_i)
        # get the P_balance and Q_balance equation addresses
        P_address = dae.get_eqn_address("Bus", "Algeb", "P_balance", bus_int)
        Q_address = dae.get_eqn_address("Bus", "Algeb", "Q_balance", bus_int)

        self.eqn_address = {"P_balance": P_address,
                            "Q_balance": Q_address}