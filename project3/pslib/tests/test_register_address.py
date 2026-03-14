import pytest
import numpy as np
import sys
import os
import pytest
from pathlib import Path
import numpy as np
from pslib.system import PowerSystem
from pslib.parsers.excel import read_from_excel
from pslib.parsers import create_system_from_file, create_system_from_data
from pslib.dae import DAE

@pytest.fixture
def dae():
    """Fixture to create DAE instance"""
    return DAE()

def test_register_eqn_for_case3(dae):
    """3 bus system from lecture 3"""
    current_dir = Path(__file__).parent
    data_file_path = current_dir.parent/"data"/"case3.xlsx"
    data = read_from_excel(data_file_path)

    three_bus_system = create_system_from_data(data)
    three_bus_system.bus.make_int_map()
    three_bus_system.bus.register_equations(dae)

    # check if equations are registered correctly
    assert "Bus" in dae.eqn_address
    assert "Algeb" in dae.eqn_address["Bus"]
    assert "P_balance" in dae.eqn_address["Bus"]["Algeb"]
    assert "Q_balance" in dae.eqn_address["Bus"]["Algeb"]
    assert len(dae.eqn_address["Bus"]["Algeb"]["P_balance"]) == 3
    assert len(dae.eqn_address["Bus"]["Algeb"]["Q_balance"]) == 3

def test_get_eqn_address_for_case3(dae):
    """3 bus system from lecture 3"""
    current_dir = Path(__file__).parent
    data_file_path = current_dir.parent/"data"/"case3.xlsx"
    data = read_from_excel(data_file_path)

    three_bus_system = create_system_from_data(data)
    three_bus_system.bus.make_int_map()
    three_bus_system.bus.register_equations(dae)

    # Test addresses for P_balance and Q_balance equations
    assert dae.get_eqn_address("Bus", "Algeb", "P_balance", [0]) == [0]
    assert dae.get_eqn_address("Bus", "Algeb", "Q_balance", [0]) == [3]
    np.testing.assert_array_equal(dae.get_eqn_address("Bus", "Algeb", "P_balance", [0, 1, 2]), [0,1,2])
    np.testing.assert_array_equal(dae.get_eqn_address("Bus", "Algeb", "Q_balance", [0, 1, 2]), [3, 4, 5])

    # Test fetch_eqn_address of generator
    np.testing.assert_array_equal(three_bus_system.gen.fetch_eqn_address(dae, three_bus_system)["P_balance"], [1])
    np.testing.assert_array_equal(three_bus_system.gen.fetch_eqn_address(dae, three_bus_system)["Q_balance"], [4])

    # Test fetch_eqn_address of network branches
    np.testing.assert_array_equal(three_bus_system.branch.fetch_eqn_address(dae, three_bus_system)["P_balance_fbus"], [0, 0, 1])
    np.testing.assert_array_equal(three_bus_system.branch.fetch_eqn_address(dae, three_bus_system)["P_balance_tbus"], [1, 2, 2])


def test_register_eqn_by_bus(dae):
    """
    Test registering equations by the Bus class for a three-bus system
    """

    # Register equations for Bus model
    dae.register_eqn("Bus", "Algeb", {"P_balance": 3, "Q_balance": 3}, [0, 1, 2])

    # check if equations are registered correctly
    assert "Bus" in dae.eqn_address
    assert "Algeb" in dae.eqn_address["Bus"]
    assert "P_balance" in dae.eqn_address["Bus"]["Algeb"]
    assert "Q_balance" in dae.eqn_address["Bus"]["Algeb"]
    assert len(dae.eqn_address["Bus"]["Algeb"]["P_balance"]) == 3
    assert len(dae.eqn_address["Bus"]["Algeb"]["Q_balance"]) == 3

def test_get_eqn_address_by_branch(dae):
    """
    Test retrieving equation address by the branch class for a three-bus system.
    """

    # Register equations for a bus model
    dae.register_eqn("Bus", "Algeb", {"P_balance":3, "Q_balance":3}, [0, 1, 2])

    # Test addresses for P_balance and Q_balance equations
    assert dae.get_eqn_address("Bus", "Algeb", "P_balance", [0]) == [0]
    assert dae.get_eqn_address("Bus", "Algeb", "Q_balance", [0]) == [3]
    np.testing.assert_array_equal(dae.get_eqn_address("Bus", "Algeb", "P_balance", [0, 1, 2]), [0,1,2])
    np.testing.assert_array_equal(dae.get_eqn_address("Bus", "Algeb", "Q_balance", [0, 1, 2]), [3, 4, 5])

def test_multiple_equation_types(dae):
    """
    Test registering and retrieving multiple equation types (e.g., Algebraic and Differential)
    """ 
    # Register equations for Bus model
    dae.register_eqn("Bus", "Algeb", {"P_balance": 3, "Q_balance": 3}, [0, 1, 2])
    dae.register_eqn("Bus", "Differential", {"V_dot": 3}, [0, 1, 2])
    # Test addresses for Algeb and Differential equations
    assert dae.get_eqn_address("Bus", "Algeb", "P_balance", [0]) == [0]
    assert dae.get_eqn_address("Bus", "Algeb", "Q_balance", [2]) == [5]
    assert dae.get_eqn_address("Bus", "Differential", "V_dot", [0]) == [6]

def test_invalid_equation_access(dae):
    """
    Test error handling when accessing invalid equation addresses
    """

    # Register equation for Bus model
    dae.register_eqn("Bus", "Algeb", {"P_balance": 3}, [0, 1, 2])

    # Test invalid equation access
    with pytest.raises(KeyError):
        dae.get_eqn_address("Bus", "Algeb", "Q_balance", [0])
        # Q_balance not registered

    with pytest.raises(KeyError):
        dae.get_eqn_address("Bus", "Differential", "V_dot", [0])
        # Differential not registered

    with pytest.raises(KeyError):
        dae.get_eqn_address("Branch", "Algeb", "P_from", [0])
        # branch nor registered