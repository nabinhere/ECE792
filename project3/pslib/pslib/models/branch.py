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

        self.eqn_address = {}
        self.eqn_residuals = {}
        
    def get_count(self):
        return len(self.fbus)
    
    def register_equations(self, dae):
        pass
    
    def fetch_eqn_address(self, dae, system):
        """
        Fetch DAE equation addresses for the given system
        """
        fbus_int = system.bus.ext2int(self.fbus)
        tbus_int = system.bus.ext2int(self.tbus)

        P_address_fbus  = dae.get_eqn_address("Bus", "Algeb", "P_balance", fbus_int)
        P_address_tbus  = dae.get_eqn_address("Bus", "Algeb", "P_balance", tbus_int)
        Q_address_tbus  = dae.get_eqn_address("Bus", "Algeb", "Q_balance", tbus_int)
        Q_address_fbus  = dae.get_eqn_address("Bus", "Algeb", "Q_balance", fbus_int)
        self.eqn_address = {"P_balance_fbus": P_address_fbus,
                            "P_balance_tbus": P_address_tbus,
                            "Q_balance_fbus": Q_address_fbus,
                            "Q_balance_tbus": Q_address_tbus} 
        return self.eqn_address