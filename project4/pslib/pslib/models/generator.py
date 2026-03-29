import numpy as np

class Generator:
    def __init__(self, bus, Pg, Qg, Qmax, Qmin, Vg, mBase, status, Pmax, Pmin, Pc1, Pc2,
                   Qc1min, Qc1max, Qc2min, Qc2max, ramp_agc, ramp_10, ramp_30, ramp_q, apf):
        self.bus = bus
        self.Pg = Pg
        self.Qg = Qg
        self.Qmax = Qmax
        self.Qmin = Qmin
        self.Vg = np.array(Vg)
        self.mBase = mBase
        self.status = status
        self.Pmax = Pmax
        self.Pmin = Pmin
        self.Pc1 = Pc1
        self.Pc2 = Pc2
        self.Qc1min = Qc1min
        self.Qc1max = Qc1max
        self.Qc2min = Qc2min
        self.Qc2max = Qc2max
        self.ramp_agc = ramp_agc
        self.ramp_10 = ramp_10
        self.ramp_30 = ramp_30
        self.ramp_q = ramp_q
        self.apf = apf

        self.addresses = {}
        self.residuals = {}
        self.values = {}

    def get_count(self):
        return len(self.bus)
    
    def register_address(self, dae):
        """
        Register equations and variables for the generator
        """
        dae.register_address("Generator", "AlgebEqn", {"V_diff": self.get_count()})
        dae.register_address("Generator", "AlgebVar", {"Q_gen": self.get_count()})

    def fetch_address(self, dae, system):
        """
        Fetch equation and variable addresses for the generator
        """
        bus_int = system.bus.ext2int(self.bus)
        P_addr = dae.get_address("Bus", "AlgebEqn", "P_balance", bus_int)
        Q_addr = dae.get_address("Bus", "AlgebEqn", "Q_balance", bus_int)
        V_diff_addr = dae.get_address("Generator", "AlgebEqn", "V_diff")
        Vm_addr = dae.get_address("Bus", "AlgebVar", "Vm", bus_int)
        Q_gen_addr = dae.get_address("Generator", "AlgebVar", "Q_gen")
        Va_addr = dae.get_address("Bus", "AlgebVar", "Va", bus_int)

        self.addresses.update(
            {"AlgebEqn":{
                "P_balance": P_addr,
                "Q_balance": Q_addr,
                "V_diff": V_diff_addr,
            },
            "AlgebVar": {
                "Q_gen": Q_gen_addr,
                "Vm": Vm_addr,
                "Va": Va_addr,
            }
            }
        )


    def fetch_eqn_address(self, dae, system):
        # get the internal bus number of the generator
        bus_int = system.bus.ext2int(self.bus)
        # get the P_balance and Q_balance equation addresses
        P_address = dae.get_eqn_address("Bus", "Algeb", "P_balance", bus_int)
        Q_address = dae.get_eqn_address("Bus", "Algeb", "Q_balance", bus_int)
        self.eqn_address = {"P_balance": P_address,
                            "Q_balance": Q_address}
        return self.eqn_address
        
    def residual(self, x):
        self.eqn_residuals = {"P_balance": self.Pg,
                              "Q_balance": self.Qg}
        
    def fetch_values(self,dae):
        """
        Fetch values for the generator
        """
        Q_gen_addr = self.addresses["AlgebVar"]["Va"]
        vm_addr = self.addresses["AlgebVar"]["Vm"]

        self.values.update({
        "AlgebVar": {
            "Q_gen": dae.get_var_values("AlgebVar", Q_gen_addr),
            "Vm": dae.get_var_values("AlgebVar", vm_addr),
        }
        })

    def calc_g(self, system):
        """
        Calculate the residual for the generator
        """

        Vm = self.values["AlgebVar"]["Vm"]

        self.values.update({
            "AlgebEqn": {
                "P_balance": self.Pg,
                "Q_balance": self.values["AlgebVar"]["Q_gen"],
                "V_diff": Vm - self.Vg,
            }
        })

    def merge_g(self, dae):
        """
        Merge the generator's residual contributions to the global 'dae.g' array
        """
        address = self.addresses["AlgebEqn"]
        value = self.values["AlgebEqn"]

        dae.g[address["P_balance"]] += value["P_balance"]
        dae.g[address["Q_balance"]] += value["Q_balance"]
        dae.g[address["v_diff"]] += value["v_diff"]