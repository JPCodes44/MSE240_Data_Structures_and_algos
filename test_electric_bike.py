import sys
import gc
import unittest
from mse240_a1.src.electric_bike import ElectricBike


def _gc_header_bytes() -> int:
    """
    Unit: helper.gc_header_bytes
    Category: infrastructure
    Input: create a trivial GC-tracked object
    Output: integer size of per-object GC header on this CPython build
    """

    class _Tmp:
        pass

    t = _Tmp()
    assert gc.is_tracked(t)
    return sys.getsizeof(t) - object.__sizeof__(t)


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
        Output: 1299.99 (float)
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
        Output: 22.046 (rounded to 3 decimals)
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
        self.assertEqual(eb.get_available_colors(), color_list)

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
        self.assertEqual(eb.get_features(), {"5 gears": True})

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
        Input: assist_level=3 (valid range 1..5)
        Output: 3
        """
        eb = ElectricBike(name="MEC Midtown 2 Bicycle", price=1299.99, assist_level=3)
        self.assertEqual(eb.get_assist_level(), 3)

    def test_estimated_range_km_typical(self):
        """
        Unit: ElectricBike.get_estimated_range_km
        Category: typical
        Input: rider_weight_kg=34, bike battery_wh=4, assist_level=3
        Output: computed km using base 0.16 km/Wh, rounded to 2 decimals
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

    # -- Setter function tests --

    def test_set_price_typical(self):
        """
        Unit: ElectricBike.set_price
        Category: typical
        Input: initial price=1000.0, then set_price(799.95)
        Output: get_price() -> 799.95
        """
        eb = ElectricBike("Bike", 1000.0, stock=1)
        eb.set_price(799.95)
        self.assertEqual(eb.get_price(), 799.95)

    def test_set_price_rejects_negative(self):
        """
        Unit: ElectricBike.set_price
        Category: error
        Input: set_price(-0.01)
        Output: raises ValueError; price unchanged
        """
        eb = ElectricBike("Bike", 1000.0, stock=1)
        before = eb.get_price()
        with self.assertRaises(ValueError):
            eb.set_price(-0.01)
        self.assertEqual(eb.get_price(), before)

    def test_set_discount_percent_updates_current_price(self):
        """
        Unit: ElectricBike.set_discount_percent + get_current_price
        Category: typical
        Input: price=2000.0; set_discount_percent(0.25)
        Output: get_current_price() -> 1500.0
        """
        eb = ElectricBike("Bike", 2000.0, stock=1)
        eb.set_discount_percent(0.25)
        self.assertAlmostEqual(eb.get_current_price(), 1500.0, places=2)

    def test_set_discount_percent_bounds(self):
        """
        Unit: ElectricBike.set_discount_percent
        Category: bounds/error
        Input: pct in {-0.1, 1.0, 2, "0.2"}
        Output: raises ValueError or TypeError
        """
        eb = ElectricBike("Bike", 1000.0, stock=1)
        for bad in (-0.1, 1.0, 2, "0.2"):
            with self.subTest(bad=bad):
                with self.assertRaises((ValueError, TypeError)):
                    eb.set_discount_percent(bad)  # type: ignore[arg-type]

    def test_set_stock_toggles_active(self):
        """
        Unit: ElectricBike.set_stock + is_active
        Category: state/typical
        Input: start stock=2 -> True; set_stock(0) -> False; set_stock(5) -> True
        Output: is_active reflects stock>0
        """
        eb = ElectricBike("Bike", 1000.0, stock=2)
        self.assertTrue(eb.is_active())
        eb.set_stock(0)
        self.assertFalse(eb.is_active())
        eb.set_stock(5)
        self.assertTrue(eb.is_active())

    def test_set_stock_rejects_negative(self):
        """
        Unit: ElectricBike.set_stock
        Category: error
        Input: set_stock(-3)
        Output: raises ValueError; stock and is_active unchanged
        """
        eb = ElectricBike("Bike", 1000.0, stock=2)
        before = eb.get_stock()
        with self.assertRaises(ValueError):
            eb.set_stock(-3)
        self.assertEqual(eb.get_stock(), before)
        self.assertTrue(eb.is_active())

    def test_set_active_guarded_by_stock(self):
        """
        Unit: ElectricBike.set_active
        Category: guard/error
        Input: stock=0; set_active(True) -> ValueError; then stock=1; set_active(True) -> True
        Output: cannot activate with zero stock
        """
        eb = ElectricBike("Bike", 1000.0, stock=0)
        self.assertFalse(eb.is_active())
        with self.assertRaises(ValueError):
            eb.set_active(True)
        eb.set_stock(1)
        eb.set_active(True)
        self.assertTrue(eb.is_active())

    def test_set_active_type_check(self):
        """
        Unit: ElectricBike.set_active
        Category: type error
        Input: set_active("yes")
        Output: raises TypeError
        """
        eb = ElectricBike("Bike", 1000.0, stock=1)
        with self.assertRaises(TypeError):
            eb.set_active("yes")  # type: ignore

    def test_set_selected_color_valid(self):
        """
        Unit: ElectricBike.set_selected_color
        Category: typical
        Input: available_colors=["black","blue"]; set_selected_color("blue")
        Output: get_selected_color() -> "blue"
        """
        eb = ElectricBike("Bike", 1000.0, stock=1, available_colors=["black", "blue"])
        eb.set_selected_color("blue")
        self.assertEqual(eb.get_selected_color(), "blue")

    def test_set_selected_color_invalid(self):
        """
        Unit: ElectricBike.set_selected_color
        Category: error
        Input: available_colors=["black"]; set_selected_color("green")
        Output: raises ValueError
        """
        eb = ElectricBike("Bike", 1000.0, stock=1, available_colors=["black"])
        with self.assertRaises(ValueError):
            eb.set_selected_color("green")

    def test_add_color_typical_and_idempotent(self):
        """
        Unit: ElectricBike.add_color
        Category: typical/idempotent
        Input: start ["black"]; add_color("red") twice
        Output: "red" appears once; selection unchanged ("black")
        """
        eb = ElectricBike("Bike", 1000.0, stock=1, available_colors=["black"])
        eb.add_color("red")
        self.assertIn("red", eb.get_available_colors())
        eb.add_color("red")
        self.assertEqual(eb.get_available_colors().count("red"), 1)
        self.assertEqual(eb.get_selected_color(), "black")

    def test_add_color_type_check(self):
        """
        Unit: ElectricBike.add_color
        Category: type error
        Input: add_color("   ")  (empty-ish)
        Output: raises TypeError
        """
        eb = ElectricBike("Bike", 1000.0, stock=1)
        with self.assertRaises(TypeError):
            eb.add_color("   ")

    def test_remove_color_rules(self):
        """
        Unit: ElectricBike.remove_color
        Category: rules/guard
        Input: remove non-existent -> ValueError; remove current selection -> ValueError; then remove other color
        Output: errors as specified; remaining colors exclude removed entry
        """
        eb = ElectricBike(
            "Bike",
            1000.0,
            stock=1,
            available_colors=["black", "blue"],
            selected_color="black",
        )
        with self.assertRaises(ValueError):
            eb.remove_color("chartreuse")
        with self.assertRaises(ValueError):
            eb.remove_color("black")
        eb.set_selected_color("blue")
        eb.remove_color("black")
        self.assertNotIn("black", eb.get_available_colors())

    def test_set_feature_typical(self):
        """
        Unit: ElectricBike.set_feature
        Category: typical
        Input: features={"has_lights": False}; set_feature("has_lights", True)
        Output: features["has_lights"] is True
        """
        eb = ElectricBike("Bike", 1000.0, stock=1, features={"has_lights": False})
        eb.set_feature("has_lights", True)
        self.assertTrue(eb.get_features()["has_lights"])

    def test_set_feature_type_checks(self):
        """
        Unit: ElectricBike.set_feature
        Category: type error
        Input: set_feature("", True) and set_feature("has_rack", "yes")
        Output: raises TypeError for both
        """
        eb = ElectricBike("Bike", 1000.0, stock=1)
        with self.assertRaises(TypeError):
            eb.set_feature("", True)
        with self.assertRaises(TypeError):
            eb.set_feature("has_rack", "yes")  # type: ignore

    def test_set_battery_wh_typical(self):
        """
        Unit: ElectricBike.set_battery_wh
        Category: typical
        Input: set_battery_wh(600)
        Output: get_battery_wh() -> 600
        """
        eb = ElectricBike("Bike", 1000.0, stock=1)
        eb.set_battery_wh(600)
        self.assertEqual(eb.get_battery_wh(), 600)

    def test_set_battery_wh_rejects_nonpositive(self):
        """
        Unit: ElectricBike.set_battery_wh
        Category: error
        Input: set_battery_wh(0) and set_battery_wh(-10)
        Output: raises ValueError for each
        """
        eb = ElectricBike("Bike", 1000.0, stock=1)
        for bad in (0, -10):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    eb.set_battery_wh(bad)

    def test_set_assist_level_bounds(self):
        """
        Unit: ElectricBike.set_assist_level
        Category: bounds
        Input: valid {1,3,5} (accept), invalid {0,6,-2} (reject)
        Output: values set for valids; ValueError for invalids
        """
        eb = ElectricBike("Bike", 1000.0, stock=1)
        for ok in (1, 3, 5):
            with self.subTest(ok=ok):
                eb.set_assist_level(ok)
                self.assertEqual(eb.get_assist_level(), ok)
        for bad in (0, 6, -2):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    eb.set_assist_level(bad)

    def test_discount_then_price_changes_current_price(self):
        """
        Unit: ElectricBike.set_discount_percent + set_price
        Category: derived price
        Input: start price=2000; discount 10% -> 1800; then set_price(2500) -> 2250
        Output: get_current_price() follows discount and updated base price
        """
        eb = ElectricBike("Bike", 2000.0, stock=1)
        eb.set_discount_percent(0.10)
        self.assertAlmostEqual(eb.get_current_price(), 1800.0, places=2)
        eb.set_price(2500.0)
        self.assertAlmostEqual(eb.get_current_price(), 2250.0, places=2)

    def test_is_on_sale(self):
        """
        Unit: ElectricBike.is_on_sale
        Category: typical
        Input: discount_percent=0.1
        Output: True
        """
        eb = ElectricBike("Bike", 2000.0, discount_percent=0.1)
        self.assertTrue(eb.is_on_sale())

    def test_is_active(self):
        """
        Unit: ElectricBike.is_active
        Category: typical
        Input: stock=2
        Output: True
        """
        eb = ElectricBike("Bike", 2000.0, stock=2)
        self.assertTrue(eb.is_active())

    # -- Mutator function tests --

    def test_add_color_typical(self):
        """
        Unit: ElectricBike.add_color
        Category: typical
        Input: available_colors=["black"]; add_color("blue")
        Output: "blue" in available colors; selected color unchanged ("black")
        """
        eb = ElectricBike("Bike", 2000.0, stock=1, available_colors=["black"])
        eb.add_color("blue")
        self.assertIn("blue", eb.get_available_colors())
        self.assertEqual(eb.get_selected_color(), "black")

    def test_remove_color_typical(self):
        """
        Unit: ElectricBike.remove_color
        Category: typical
        Input: available_colors=["black","blue"]; remove_color("blue")
        Output: remaining colors ["black"]
        """
        eb = ElectricBike("Bike", 2000.0, stock=1, available_colors=["black", "blue"])
        eb.remove_color("blue")
        self.assertEqual(eb._available_colors, ["black"])

    def test_sizeof_typical_strict(self):
        """
        Unit: ElectricBike.__sizeof__
        Category: strict (CPython)
        Input: regular instance with small features dict
        Output: sys.getsizeof(eb) == eb.__sizeof__() + GC_HEADER (if tracked)
        """
        eb = ElectricBike(
            "Bike", 2000.0, stock=1, features={"grippers": True, "heated seats": True}
        )
        deep_no_gc = eb.__sizeof__()
        maybe_gc = _gc_header_bytes() if gc.is_tracked(eb) else 0
        self.assertEqual(sys.getsizeof(eb), deep_no_gc + maybe_gc)
