import numpy as np
from pslib.models.basemodel import BaseModel

class Generator(BaseModel):
    def __init__(self, bus, Pg, Qg, Qmax, Qmin, Vg, mBase, status, Pmax, Pmin, Pc1, Pc2,
                   Qc1min, Qc1max, Qc2min, Qc2max, ramp_agc, ramp_10, ramp_30, ramp_q, apf):
        super().__init__()      # call the constructor of the base class
        self.bus = bus
        self.Pg = np.array(Pg)     
        self.Qg = np.array(Qg)                
        self.Qmax = np.array(Qmax)
        self.Qmin = np.array(Qmin)
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

        self.residuals = {}


    def get_count(self):
        return len(self.bus)
    
    
    def set_metadata(self):
        """
        Set metadata for the generator model
        """
        self.reg_data = {
            "AlgebEqn": {
                "V_diff": self.get_count()
            },
            "AlgebVar": {
                "Q_gen": self.get_count()
            }
        }

        self.fetch_data = {
            "AlgebEqn": {
                "P_balance": ("Bus", "P_balance", None),
                "Q_balance": ("Bus", "Q_balance", None),
                "V_diff": ("Generator", "V_diff", None),
            },
            "AlgebVar": {
                "Q_gen": ("Generator", "Q_gen", None),
                "V": ("Bus", "Vm", None)
            }
        }


    def resolve_indices(self, system):
        """
        Resolve indices for fetch_data.
        """
        # Update all Bus indices
        bus_int = system.bus.ext2int(self.bus)

        # Give it an alias for convenience
        fd = self.fetch_data
        for type_name in fd:
            for dest_name in fd[type_name]:
                src_model, src_name, _ = fd[type_name][dest_name]
                if src_model == "Bus":
                    fd[type_name][dest_name] = (src_model, src_name, bus_int)
                    
    
    def calc_g(self, system):
        """
        Calculate the residual for the generator
        """

        Vm = self.values["AlgebVar"]["Vm"]

        self.values.update({
            "AlgebEqn": {
                "P_balance": self.Pg / 100,
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
        dae.g[address["V_diff"]] += value["V_diff"]