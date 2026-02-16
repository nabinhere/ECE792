import sys
import os
import pytest
from pathlib import Path
import numpy as np
from pslib.system import PowerSystem
from pslib.parsers.excel import read_from_excel
from pslib.parsers import create_system_from_data

@pytest.fixture
def sample_system():
    """3 bus system from lecture 3"""
    current_dir = Path(__file__).parent
    data_file_path = current_dir.parent/"data"/"case3.xlsx"
    data = read_from_excel(data_file_path)

    sample_system = create_system_from_data(data)
    sample_system.bus.make_int_map()
    return sample_system

def test_ybus_creation(sample_system):
    sample_system.makeYbus()
    # ybus = sample_system.Ybus.todense()
    ybus = sample_system.Ybus

    # Test diagonal elements (self admittance)
    np.testing.assert_almost_equal(ybus[0, 0], 1.21133795-13.09457417j, decimal=3)
    np.testing.assert_almost_equal(ybus[1, 1], 1.21133795-13.09457417j, decimal=3)
    np.testing.assert_almost_equal(ybus[2, 2], 1.98019802-19.7019802j, decimal=3)

    # Test off-diagonal element (branch admittance between bus 1-2)
    np.testing.assert_almost_equal(ybus[1,2], -0.99009901+9.9009901j, decimal=3)

    # additional sanity checks
    assert  ybus.shape == (3,3), "Ybus should be 3x3 for 3-bus system"

