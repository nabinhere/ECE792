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
        
    def get_count(self):
        return len(self.fbus)