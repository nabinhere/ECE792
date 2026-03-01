import pytest
import numpy as np
from pslib.dae import DAE

@pytest.fixture
def dae():
    """Fixture to create DAE instance"""
    return DAE()

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

# def test_get_eqn_address_by_branch(dae):
#     """
#     Test retrieving equation address by the branch class for a three-bus system.
#     """

#     # Register equations for a bus model
#     dae.register_eqn("Bus", "Algeb", {"P_balance":3, "Q_balance":3})

#     # Test addresses for P_balance and Q_balance equations
#     assert dae.get_eqn_address("Bus", "Algeb", "P_balance", 0) == 0
#     assert np.testing.assert_array_equal(dae.get_eqn_address("Bus", "Algeb", "P_balance", [0, 1, 2]), [0, 1, 2]) 

#     assert dae.get_eqn_address("Bus", "Algeb", "Q_balance", 0) == 3
#     assert np.testing.assert_array_equal(dae.get_eqn_address("Bus", "Algeb", "Q_balance", [0, 1, 2]), [3, 4, 5])

# def test_multiple_equation_types(dae):
#     """
#     Test registering and retrieving multiple equation types (e.g., Algebraic and Differential)
#     """ 
#     # Register equations for Bus model
#     dae.register_eqn("Bus", "Algeb", {"P_balance": 3, "Q_balance": 3})
#     dae.register_eqn("Bus", "Differential", {"V_dot": 3})

# def test_invalid_equation_access(dae):
#     """
#     Test error handling when accessing invalid equation addresses
#     """

#     # Register equation for Bus model
#     dae.register_eqn("Bus", "Algeb", {"P_balance": 3})

#     # Test invalid equation access
#     with pytest.raises(KeyError):
#         dae.get_eqn_address("Bus", "Algeb", "Q_balance", 0)
#         # Q_balance registered

#     with pytest.raises(KeyError):
#         dae.get_eqn_address("Bus", "Differential", "V_dot", 0)
#         # Differential not registered

#     with pytest.raises(KeyError):
#         dae.get_eqn_address("Branch", "Algeb", "P_from", 0)
#         # branch nor registered

