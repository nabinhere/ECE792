import numpy as np


class Branch:
    def __init__(self, fbus, tbus, r, x, b, rateA, rateB, rateC,
                 ratio, angle, status, angmin, angmax):
        self.fbus = fbus
        self.tbus = tbus
        self.r = r
        self.x = x
        self.b = b
        self.rateA = rateA
        self.rateB = rateB
        self.rateC = rateC
        self.ratio = ratio
        self.angle = angle
        self.status = status
        self.angmin = angmin
        self.angmax=  angmax

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

    