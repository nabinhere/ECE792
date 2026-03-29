import numpy as np

class Bus:
    def __init__(self, bus_i, type, Pd, Qd, Gs, Bs,
                 area, Vm, Va, baseKV, zone, Vmax, Vmin):
        self.bus_i = bus_i
        self.type = np.array(type)
        self.Pd = Pd
        self.Qd = Qd
        self.Gs = Gs
        self.Bs = Bs
        self.area = area
        self.Vm = np.array(Vm)
        self.Va = np.array(Va)
        self.baseKV = baseKV
        self.zone = zone
        self.Vmax = Vmax
        self.Vmin = Vmin

        self._int_map = {}
        self.ext_numbers = bus_i

        self.addresses = {}
        self.values = {}
    
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
                          "Vm_diff": np.count_nonzero(self.type==3),
                          "Va_diff": np.count_nonzero(self.type==3)})
        
        # register variables
        dae.register_address("Bus",
                             "AlgebVar",
                             {"Va": self.get_count(),
                             "Vm": self.get_count(),
                             "P_slack": np.count_nonzero(self.type==3),
                             "Q_slack": np.count_nonzero(self.type==3)})
        
        
    def fetch_address(self, dae, system):
        # fetch variable and equation addresses for the buses

        self.addresses = {
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

    # TODO: Consider refactoring to reduce the boilerplate code
    def fetch_values(self, dae):
        """
        Fetch values for buses
        """
        vm_addr = self.addresses["AlgebVar"]["Vm"]
        va_addr = self.addresses["AlgebVar"]["Va"]
        p_slack_addr = self.addresses["AlgebVar"]["P_slack"]
        q_slack_addr = self.addresses["AlgebVar"]["Q_slack"]   

        self.values.update({
            "AlgebVar": {
                "Va": dae.get_var_values("AlgebVar", va_addr),
                "Vm": dae.get_var_values("AlgebVar", vm_addr),
                "P_slack": dae.get_var_values("AlgebVar", p_slack_addr),
                "Q_slack": dae.get_var_values("AlgebVar", q_slack_addr),
            }
        }) 


    def calc_g(self, system):
        """
        Calculate contributions to the residual vector 'g'
        """
        # TODO: the code below only considers load. 'Gs' and 'Bs' should be considered in the future for corectness.

        # Note: the negative sign indicates power consumption (leaving)

        Va = self.values["AlgebVar"]["Va"]
        Vm = self.values["AlgebVar"]["Vm"]

        # Make a mask vector to identify the slack bus (es)
        slack_mask = (self.type==3)

        # These two are the unknown variables whose values are provided by 'fsolve'
        P_slack = self.values["AlgebVar"]["P_slack"]
        Q_slack = self.values["AlgebVar"]["Q_slack"]

        # calculate the net power consumption at each bus
        # P_net = P_load - P_slack (at the proper locations!)

        # net power consumptions
        P_net = np.array(self.Pd)
        Q_net = np.array(self.Qd)
        P_net[slack_mask] = P_net[slack_mask] - P_slack
        Q_net[slack_mask] = Q_net[slack_mask] - Q_slack

        self.values.update({
            "AlgebEqn": {
                "P_balance": -P_net,
                "Q_balance": -Q_net,
                "Va_diff": Va[slack_mask] - self.Va[slack_mask],
                "Vm_diff": Vm[slack_mask] - self.Vm[slack_mask],
            }
        })
        
    def merge_g(self, dae):
        """
        Merge the residual contributions to the global 'dae.g' array.
        """

        address = self.addresses["AlgebEqn"]
        value = self.values["AlgebEqn"]

        dae.g[address["P_balance"]] += value["P_balance"]
        dae.g[address["Q_balance"]] += value["Q_balance"]
        dae.g[address["Va_diff"]] += value["Va_diff"]
        dae.g[address["Vm_diff"]] += value["Vm_diff"]