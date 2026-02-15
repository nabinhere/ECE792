import numpy as np
class PowerSystem:
    def __init__(self, bus, branch, gen):
        self.bus = bus
        self.branch = branch
        self.gen = gen

    def makeYbus(self):
        fbus = self.bus.ext2int(self.branch.fbus)
        tbus = self.bus.ext2int(self.branch.tbus)

        branches = [fbus, tbus, self.branch.r, self.branch.x, self.branch.b]

        n_bus = len(self.bus.getcount())     # number of branches
        # initialize the Y bus matrix
        Ybus = np.zeros((n_bus, n_bus))

        for branch in branches:
            f, t, r, x, b = branch

            z = r + 1j*x
            y = 1/z

            # off-diagonal elements
            Ybus[f][t] = -y
            Ybus[t][f] = -y

            # diagonal elements
            Ybus[f][f] += y + 1j*b/2
            Ybus[t][t] += y + 1j*b/2

        self.Ybus = Ybus

        