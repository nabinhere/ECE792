from scipy.sparse import csc_matrix, coo_matrix
import numpy as np

class PowerSystem:
    def __init__(self, bus, branch, gen):
        self.bus = bus
        self.branch = branch
        self.gen = gen

        self.baseMVA = 100
    
    def makeYbus(self):
        """
        Make the Ybus matrix.
        """

        # convert the external bus numbers to internal bus numbers
        fbus = self.bus.ext2int(self.branch.fbus)
        tbus = self.bus.ext2int(self.branch.tbus)

        # get the number of buses
        n_buses = self.bus.get_count()

        # create the vector of series admittances
        y_series = 1 /(self.branch.r + 1j*self.branch.x)
        # create the vector of shunt admittances
        y_shunt = 1j* self.branch.b

        # create the row and column indices
        row = np.hstack([fbus, tbus, fbus, tbus])
        col = np.hstack([fbus, tbus, tbus, fbus])

        # create the data vector
        data = np.hstack([y_series+ y_shunt/2,
                          y_series + y_shunt/2,
                          -y_series,
                          -y_series])

        # create the admittance matrix in COO format
        Y = coo_matrix((data, (row, col)), shape = (n_buses, n_buses))
        
        # convert the admittance matrix to a sparse matrix in CSC format
        self.Ybus = Y.tocsc()