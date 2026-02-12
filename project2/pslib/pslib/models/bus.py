class Bus:
    def __init__(self, bus_i, type, Pd, Qd, Gs, Bs,
                 area, Vm, Va, baseKV, zone, Vmax, Vmin):
        self.bus_i = bus_i
        self.type = type
        self.Pd = Pd
        self.Qd = Qd
        self.Gs = Gs
        self.Bs = Bs
        self.Vm = Vm
        self.Va = Va
        self.baseKV = baseKV
        self.zone = zone
        self.Vmax = Vmax
        self.Vmin = Vmin
    
    def get_count(self):
        return len(self.bus_i)