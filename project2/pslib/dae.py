import numpy as np

class DAE:
    def __init__(self):
        self.m = 0  # next available address
        self.eqn_address = {}

    def register_eqn(self, model_name: str, var_type: str, eqn_dict: dict, bus_int):
        """
        register a specified type of equations for a given model 
        """
        num_p_eqn = eqn_dict["P"]   # number of P equations to be registered
        num_q_eqn = eqn_dict["Q"]   # number of Q equations to be registered
        P_balance_dict = {}
        Q_balance_dict = {}

        P_balance_address = np.array(range(self.m, self.m+num_p_eqn))
        Q_balance_address = np.array(range(self.m+num_p_eqn, self.m+num_p_eqn+num_q_eqn))

        for i, val in enumerate(bus_int):
            P_balance_dict[val] = P_balance_address[i]
            Q_balance_dict[val] = Q_balance_address[i]

        self.eqn_address[model_name] = {var_type:
                                        {"P_balance": P_balance_dict,
                                        "Q_balance": Q_balance_dict
                                        }
                                    }
                                    
        self.m += num_p_eqn + num_q_eqn     # update the next available equation address



    def get_eqn_address(self, model_name: str, var_type: str, var_name: str, bus_no: int | np.ndarray)->np.ndarray:
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


# #################################################################################
# #################################################################################
class Generator:
    def __init__(self):
        self.eqn_address = {}   # probably used to store the address of residual equations that a generator affects 
        self.eqn_residuals = {}  # probably used to store the residual contribution of a generator

    def fetch_eqn_address(self, dae, system):
        # get the internal bus number of the generator
        bus_int = system.bus.ext2int(self.bus)
        # get the P_balance and Q_balance equation addresses
        P_address = dae.get_eqn_address("Bus", "Algeb", "P_balance", bus_int)
        Q_address = dae.get_eqn_address("Bus", "Algeb", "Q_balance", bus_int)
        self.eqn_address = {"P_balance": P_address,
                            "Q_balance": Q_address}
        
    def residual(self, x):
        self.eqn_residuals = {"P_balance": self.Pg,
                              "Q_balance": self.Qg}
        

class Bus:
    def register_equations(self, dae):
        dae.register_eqn("Bus", "Algeb", 
                         {"P": self.get_count(),
                          "Q": self.get_count()}, self._int_map.values())
        
        dae.register_eqn("Bus", "Algeb", self._int_map.values)
    
    def fetch_equation_address(self, dae, system):
        bus_int = self.ext2int(self.bus_i)
        # get the P_balance and Q_balance equation addresses
        P_address = dae.get_eqn_address("Bus", "Algeb", "P_balance", bus_int)
        Q_address = dae.get_eqn_address("Bus", "Algeb", "Q_balance", bus_int)

        self.eqn_address = {"P_balance": P_address,
                            "Q_balance": Q_address}
        
class Branch:
    def __init__(self):
        self.eqn_address = {}
        self.eqn_residuals = {}

    def fetch_eqn_address(self, dae, system):
        fbus_int = system.bus.ext2it(self.fbus)
        tbus_int = system.bus.ext2int(self.tbus)

        P_address_fbus  = dae.get_eqn_address("Branch", "Algeb", "P_balance", fbus_int)
        P_address_tbus  = dae.get_eqn_address("Branch", "Algeb", "P_balance", tbus_int)
        Q_address_fbus  = dae.get_eqn_address("Branch", "Algeb", "Q_balance", fbus_int)
        Q_address_tbus  = dae.get_eqn_address("Branch", "Algeb", "Q_balance", tbus_int)
        self.eqn_address = {"P_balance_fbus": P_address_fbus,
                            "P_balance_tbus": P_address_tbus,
                            "Q_balance_fbus": Q_address_fbus,
                            "Q_balance_tbus": Q_address_tbus} 