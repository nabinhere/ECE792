class Generator:
    def __init__(self, bus, Pg, Qg, Qmax, Qmin, Vg, mBase, status, Pmax, Pmin, Pc1, Pc2,
                   Qc1min, Qc1max, Qc2min, Qc2max, ramp_agc, ramp_10, ramp_30, ramp_q, apf):
        self.bus = bus
        self.Pg = Pg
        self.Qg = Qg
        self.Qmax = Qmax
        self.Qmin = Qmin
        self.Vg = Vg
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

        self.eqn_address = {}
        self.residuals = {}

    def get_count(self):
        return len(self.bus)
    
    def register_eqn(self, dae):
        pass
    
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