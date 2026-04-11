import numpy as np
from typing import Dict, Union, List, Optional


class DAE:
    def __init__(self):

        # model -> type -> name -> array of addresses
        self.addresses: Dict[str, Dict[str, Dict[str, List[int]]]] = {}
        self.next_addresses: Dict[str, int] = {}

        self.g = np.array([])
        self.y = np.array([])

    def register_address(self, model_name: str, type_name: str, var_dict: Dict[str, int]) -> None:
        """
        Register addresses for any type.

        Parameters
        ----------
        model_name : str
            Name of the model (e.g., "Bus")
        type_name : str
            Full type name (e.g., "AlgebEqn", "StateVar", "Observed")
        var_dict : dict
            Dictionary of variable names and their sizes
        """
        if model_name not in self.addresses:
            self.addresses[model_name] = {}
        if type_name not in self.addresses[model_name]:
            self.addresses[model_name][type_name] = {}

        # Initialize next_address for this type if not exists
        if type_name not in self.next_addresses:
            self.next_addresses[type_name] = 0

        for name, size in var_dict.items():
            # Store continuous array of addresses using type-specific counter
            self.addresses[model_name][type_name][name] = np.arange(
                self.next_addresses[type_name],
                self.next_addresses[type_name] + size
            )
            self.next_addresses[type_name] += size

    def get_address(self, model_name: str, type_name: str, name: str,
                   index: Optional[Union[int, List[int], range, np.ndarray]] = None) -> Union[np.ndarray, int, List[int]]:
        """
        Get the address of a type (equation, variable, etc.)

        Parameters
        ----------
        model_name : str
            Name of the model (e.g., "Bus")
        type_name : str
            Name of the type (e.g., "AlgebEqn", "AlgebVar")
        name : str
            Name of the variable (e.g., "P_balance", "Q_balance")
        index : int, list, range, or numpy array
            0-based index of the variable. If None, all addresses are returned.

        Returns
        -------
        addr_array : numpy array
            Array of addresses
        """

        addr_array = self.addresses[model_name][type_name][name]

        if index is None:
            return addr_array

        if isinstance(index, (int, np.integer, list, range, np.ndarray)):
            return addr_array[index]

        raise ValueError(f"Index must be an integer, list, range, or numpy array. Got {type(index)}")

    def initialize_arrays(self):
        """
        Initialize the arrays for the DAE.
        """
        # Check if the number of algebraic variables equal equations
        if self.next_addresses["AlgebEqn"] != self.next_addresses["AlgebVar"]:
            raise ValueError("# of algeb. eqn. != # of algeb. vars.")

        self.g = np.zeros(self.next_addresses["AlgebEqn"])
        self.y = np.zeros(self.next_addresses["AlgebVar"])

    def get_var_values(self, type_name: str, index: np.ndarray) -> np.ndarray:
        """
        Get the values of a type (equation, variable, etc.)
        """
        if type_name == "AlgebVar":
            return self.y[index]
        else:
            raise ValueError(f"Invalid type name: {type_name}")
