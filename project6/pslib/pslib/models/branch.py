import numpy as np


class Branch:
    def __init__(self, fbus, tbus, r, x, b, rateA, rateB, rateC,
                 ratio, angle, status, angmin, angmax):
            # ensure numeric fields are numpy arrays for elementwise ops
            self.fbus = np.array(fbus, dtype=int)
            self.tbus = np.array(tbus, dtype=int)
            self.r = np.array(r, dtype=float)
            self.x = np.array(x, dtype=float)
            self.b = np.array(b, dtype=float)
            self.rateA = np.array(rateA, dtype=float)
            self.rateB = np.array(rateB, dtype=float)
            self.rateC = np.array(rateC, dtype=float)
            self.ratio = np.array(ratio, dtype=float)
            self.angle = np.array(angle, dtype=float)
            self.status = np.array(status, dtype=int)
            self.angmin = np.array(angmin, dtype=float)
            self.angmax = np.array(angmax, dtype=float)

            self.addresses = {}
            self.eqn_residuals = {}

            self.values = {}
        
    def get_count(self):
        return len(self.fbus)
    
    def register_address(self, dae):
        """
        Register the equations for branches.

        Branches use equations from the Bus model.
        No new equations created by branches
        """
        pass
    
    def fetch_address(self, dae, system):
        """
        Fetch DAE equation addresses for the given system
        """

        bus_int = list(range(system.bus.get_count()))

        P_addr = dae.get_address("Bus", "AlgebEqn", "P_balance", bus_int)
        Q_addr = dae.get_address("Bus", "AlgebEqn", "Q_balance", bus_int)

        self.addresses.update({
            "AlgebEqn": {
                "P_balance": P_addr,
                "Q_balance": Q_addr,
            }
        })

        Va_addr = dae.get_address("Bus", "AlgebVar", "Va", bus_int)
        Vm_addr = dae.get_address("Bus", "AlgebVar", "Vm", bus_int)

        self.addresses.update({
            "AlgebVar": {"Va": Va_addr,
                         "Vm": Vm_addr,}
        })

    def fetch_values(self, dae):
        """
        Fetch values for branches
        """
        va_addr = self.addresses["AlgebVar"]["Va"]
        vm_addr = self.addresses["AlgebVar"]["Vm"]

        self.values.update({
            "AlgebVar": {
                "Va": dae.get_var_values("AlgebVar", va_addr),
                "Vm": dae.get_var_values("AlgebVar", vm_addr),
            }
        })

    def calc_g(self, system):
        """
        Calculate contributions to the residual vector 'g'.
        """
        Va = self.values["AlgebVar"]["Va"]
        Vm = self.values["AlgebVar"]["Vm"]

        Ybus = system.Ybus

        Vc = Vm * np.exp(1j*Va)
        S = np.diag(Vc) @ np.conj(Ybus @ Vc)

        self.values.update({
            "AlgebEqn": {
                "P_balance": -np.real(S),
                "Q_balance": -np.imag(S),
            }
        })

    def merge_g(self, dae):
        """
        Merge the residual contributions to the global 'dae.g' array
        """

        address = self.addresses["AlgebEqn"]
        value = self.values["AlgebEqn"]

        dae.g[address["P_balance"]] += value["P_balance"]
        dae.g[address["Q_balance"]] += value["Q_balance"]
         

    