import numpy as np

class DAE:
    def __init__(self):
        self.m = 0  # next available address
        self.eqn_address = {}

    def register_eqn(self, model_name: str, var_type: str, eqn_dict: dict, bus_int):
        """
        register a specified type of equations for a given model 
        """
        num_p_eqn = eqn_dict["P_balance"]   # number of P equations to be registered
        num_q_eqn = eqn_dict["Q_balance"]   # number of Q equations to be registered
        P_balance_dict = {}
        Q_balance_dict = {}

        P_balance_address = np.array(range(self.m, self.m+num_p_eqn))
        Q_balance_address = np.array(range(self.m+num_p_eqn, self.m+num_p_eqn+num_q_eqn))

        for i, val in enumerate(bus_int):
            P_balance_dict[val] = P_balance_address[i]
            Q_balance_dict[val] = Q_balance_address[i]

        self.eqn_address.update({model_name:
                                {var_type:
                                        {"P_balance": P_balance_dict,
                                        "Q_balance": Q_balance_dict
                                        }
                                    }})
                                    
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