import unittest
from src.electric_bike import ElectricBike


class TestElectricBike(unittest.TestCase):
    """Unit tests for ElectricBike"""

    # -- Getter function tests --

    def test_get_name_typical(self):
        """
        Unit: ElectricBike.get_name
        Category: typical
        Input: ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99, stock=5)
        Output: "MEC Midtown 2 Bicycle"
        """
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99, stock=5)
        self.assertEqual(eb.get_name(), "MEC Midtown 2 Bicycle")

    def test_get_price_typical(self):
        """
        Unit: ElectricBike.get_price
        Category: typical
        Input: ElectricBike(..., price=1299.99)
        Output: 129.999e1 (1299.99) as float
        """
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99)
        self.assertEqual(eb.get_price(), 1299.99)

    def test_get_current_price_typical(self):
        """
        Unit: ElectricBike.get_current_price
        Category: typical
        Input: price=1299.99, then set_discount_percent(0.20)
        Output: 1039.99 (price after 20% discount), rounded to 2 decimals
        """
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99)
        eb.set_discount_percent(0.20)
        self.assertAlmostEqual(eb.get_current_price(), 1039.99, places=2)

    def test_get_weight_kg_typical(self):
        """
        Unit: ElectricBike.get_weight_kg
        Category: typical
        Input: weight_kg=10.1
        Output: 10.1
        """
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99, weight_kg=10.1)
        self.assertEqual(eb.get_weight_kg(), 10.1)

    def test_get_weight_lb_typical(self):
        """
        Unit: ElectricBike.get_weight_lb
        Category: typical
        Input: weight_kg=10.0
        Output: 22.046 lb (rounded to 3 decimals)
        """
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99, weight_kg=10.0)
        self.assertAlmostEqual(eb.get_weight_lb(), 22.046, places=3)

    def test_get_stock_typical(self):
        """
        Unit: ElectricBike.get_stock
        Category: typical
        Input: stock=3
        Output: 3
        """
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99, stock=3)
        self.assertEqual(eb.get_stock(), 3)

    def test_get_available_colors_typical(self):
        """
        Unit: ElectricBike.get_available_colors
        Category: typical
        Input: available_colors=["black","cyan","purple"]
        Output: ["black","cyan","purple"] (defensive copy; equal contents)
        """
        color_list = ["black", "cyan", "purple"]
        eb = ElectricBike(
            name="MEC Midtown 2 Bicycle", price=1299.99, available_colors=color_list
        )
        self.assertEqual(eb.get_available_colors(), color_list)  # NOTE: call the method

    def test_get_features_typical(self):
        """
        Unit: ElectricBike.get_features
        Category: typical
        Input: features={"5 gears": True}
        Output: {"5 gears": True} (defensive copy; equal contents)
        """
        eb = ElectricBike(
            name="MEC Midtown 2 Bicycle", price=1299.99, features={"5 gears": True}
        )
        self.assertEqual(eb.get_features(), {"5 gears": True})  # NOTE: call the method

    def test_get_selected_colors_typical(self):
        """
        Unit: ElectricBike.get_selected_color
        Category: typical
        Input: available_colors includes "green", selected_color="green"
        Output: "green"
        """
        eb = ElectricBike(
            name="MEC Midtown 2 Bicycle",
            price=1299.99,
            available_colors=["black", "green", "purple"],
            selected_color="green",
        )
        self.assertEqual(eb.get_selected_color(), "green")

    def test_get_battery_wh_typical(self):
        """
        Unit: ElectricBike.get_battery_wh
        Category: typical
        Input: battery_wh=10
        Output: 10
        """
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99, battery_wh=10)
        self.assertEqual(eb.get_battery_wh(), 10)

    def test_get_assist_level_typical(self):
        """
        Unit: ElectricBike.get_assist_level
        Category: typical
        Input: assist_level=3  (valid range 1..5)
        Output: 3
        """
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99, assist_level=3)
        self.assertEqual(eb.get_assist_level(), 3)

    def test_estimated_range_km_typical(self):
        """
        Unit: ElectricBike.get_estimated_range_km
        Category: typical
        Input: rider_weight_kg=34, bike with battery_wh=4, assist_level=3
        Output: numeric range in km (rounded to 2 decimals) using the documented formula
        """
        assist_level = 3
        battery_wh = 4
        rider_weight_kg = 34

        eb = ElectricBike(
            name="MEC Midtown 2 Bicycle",
            price=1299.99,
            battery_wh=battery_wh,
            assist_level=assist_level,
        )

        base_eff_km_per_Wh = 0.16
        assist_factor = 3.0 / assist_level
        weight_factor = 75.0 / float(rider_weight_kg)
        expected = round(
            battery_wh * base_eff_km_per_Wh * assist_factor * weight_factor, 2
        )

        self.assertEqual(
            eb.get_estimated_range_km(rider_weight_kg=rider_weight_kg), expected
        )
