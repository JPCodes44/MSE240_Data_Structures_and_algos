import unittest
from src.electric_bike import ElectricBike


class TestElectricBike(unittest.TestCase):
    def test_basic_getters(self):
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99, stock=5)
        self.assertEqual(eb.get_name(), "MEC Midtown 2 Bicycle")
