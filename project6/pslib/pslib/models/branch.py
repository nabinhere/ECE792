import numpy as np
from pslib.models.basemodel import BaseModel


class Branch(BaseModel):
    def __init__(self, fbus, tbus, r, x, b, rateA, rateB, rateC,
                 ratio, angle, status, angmin, angmax):
            super().__init__()      # call the constructor of the base class
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

            self.eqn_residuals = {}

        
    def get_count(self):
        return len(self.fbus)
    
    def set_metadata(self):
         """
         Set the metadata for the branch

         self.reg_data is not required because branches use equations from the Bus model.
         No new equations created by branches
         """

         self.fetch_data = {
              "AlgebEqn": {
                   "P_balance": ("Bus", "P_balance", None),
                   "Q_balance": ("Bus", "Q_balance", None),
              },
              "AlgebVar": {
                   "Va": ("Bus", "Va", None),
                   "Vm": ("Bus", "Vm", None),
              }
         }
    
    

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
         

    