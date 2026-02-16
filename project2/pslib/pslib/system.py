import numpy as np

class PowerSystem:
    def __init__(self, bus, branch, gen):
        self.bus = bus
        self.branch = branch
        self.gen = gen

    def makeYbus(self):
        fbus = self.bus.ext2int(self.branch.fbus)
        tbus = self.bus.ext2int(self.branch.tbus)
        
        # convert to numpy arrays to enable vectorized operation
        r = np.array(self.branch.r)
        x = np.array(self.branch.x)
        b = np.array(self.branch.b)

        # branch impedance and admittance
        z = r + 1j*x
        y = 1 / z

        n_bus = self.bus.get_count()    #number of buses
        # initialize the Ybus matrix
        Ybus = np.zeros((n_bus, n_bus), dtype=complex)
        # off-diagonal elements
        Ybus[fbus, tbus] = -y
        Ybus[tbus, fbus] = -y
        # diagonal elements
        np.add.at(Ybus, (fbus, fbus), y + 1j*b/2)
        np.add.at(Ybus, (tbus, tbus), y + 1j*b/2)

        self.Ybus = Ybus

        return self.Ybus

        