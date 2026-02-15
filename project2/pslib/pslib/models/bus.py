import numpy as np
from pslib.parsers import create_system_from_data
from pslib.parsers.excel import read_from_excel

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

        self._int_map = {}
    
    def get_count(self):
        return len(self.bus_i)
    
    def ext2int(self, ext_numbers):
        """
        Convert an array of external bus numbers to internal bus numbers.
        """
        return np.vectorize(self._int_map.get)(ext_numbers)
    
    def make_int_map(self):
        """
        Make the map from external bus number to internal bus number.

        This function should be called before adding all bus data
        """
        self._int_map = {}
        for i, ext_number in enumerate(self.ext_numbers):
            self._int_map[ext_number] = i