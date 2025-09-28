"""
ElectricBike: Online-store item class for an e-bike.

Author: Justin Mak
Assignment: MSE 240 - Assignment 1
Date: 2025-09-27

Description:
  Represents an electric bicycle being sold in an online store. Satisfies assignment
  constraints: string name, float price, boolean(s), integer(s), list/dict attributes,
  mutually dependent attributes (stock <-> is_active, discount_percent -> current price),
  calculated accessors (weight in lb; estimated range), default values, and appropriate errors.

Input:
  Used via constructor parameters and method calls (no stdin).

Output:
  Accessor return values; raises ValueError/TypeError on invalid inputs.
"""

from __future__ import annotations
from typing import Dict, List
import sys


class ElectricBike:
    """
    ElectricBike item suitable for an online store cart/catalog.

    Invariants:
        - _name is non-empty string
        - _price >= 0.0
        - _stock >= 0
        - 0.0 <= _discount_percent < 1.0
        - _assist_level in [1..5]
        - _selected_color in _available_colors
        - _battery_wh > 0
        - _weight_kg > 0

      Mutually dependent attributes:
          - _stock (int) and _is_active (bool): stock == 0 forces is_active False.
          - _discount_percent (float) influences computed current price.
    """

    def __init__(
        self,
        name: str,
        price: float,
        *,
        stock: int = 0,
        weight_kg: float = 22.5,
        available_colors: List[str] | None = None,
        selected_color: str | None = None,
        features: Dict[str, bool] | None = None,
        battery_wh: int = 450,
        assist_level: int = 3,
        discount_percent: float = 0.0,
    ) -> None:
        # Basic validation
        if not isinstance(name, str) or not name.strip():
            raise TypeError("name must be a non-empty string")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a non-negative number")
        if not isinstance(stock, int) or stock < 0:
            raise ValueError("stock must be a non-negative int")
        if not isinstance(weight_kg, (int, float)) or weight_kg <= 0:
            raise ValueError("weight_kg must be a positive number")
        if not isinstance(battery_wh, int) or battery_wh <= 0:
            raise ValueError("battery_wh must be a positive int")
        if not isinstance(assist_level, int) or not (1 <= assist_level <= 5):
            raise ValueError("assist_level must be an int in [1..5]")
        if not isinstance(discount_percent, (int, float)) or not (
            0.0 <= discount_percent < 1.0
        ):
            raise ValueError("discount_percent must be in [0.0, 1.0)")

        self._name: str = name.strip()
        self._price: float = float(price)
        self._stock: int = stock
        self._weight_kg: float = float(weight_kg)
        self._available_colors: List[str] = list(
            available_colors or ["black", "silver", "red"]
        )
        self._features: Dict[str, bool] = dict(
            features or {"has_rack": True, "has_lights": True, "has_fenders": False}
        )
        self._battery_wh: int = battery_wh
        self._assist_level: int = assist_level
        self._discount_percent: float = float(discount_percent)

        # selected_color defaults to first available if not provided
        if selected_color is None:
            self._selected_color: str = self._available_colors[0]
        else:
            if selected_color not in self._available_colors:
                raise ValueError("selected_color must exist in available_colors")
            self._selected_color = selected_color

        # Active is derived from the stock initially
        self._is_active: bool = self._stock > 0

    # -- Getter functions --
    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        """Base price before any discount."""
        return self._price

    def get_current_price(self) -> float:
        """Computed price after discount, rounded to cents."""
        return round(self._price - (self._price * self._discount_percent), 2)

    def get_weight_kg(self) -> float:
        return self._weight_kg

    def get_weight_lb(self) -> float:
        KG_TO_LB = 2.20462262185
        return self._weight_kg * KG_TO_LB

    def get_stock(self) -> int:
        return self._stock

    def get_available_colors(self) -> List[str]:
        return self._available_colors

    def get_features(self) -> Dict[str, bool]:
        return self._features

    def get_selected_color(self) -> str:
        return self._selected_color

    def get_battery_wh(self) -> int:
        return self._battery_wh

    def get_assist_level(self) -> int:
        return self._assist_level

    def get_estimated_range_km(self, rider_weight_kg: float = 75.0) -> float:
        base_eff_km_per_Wh = 0.16
        assist_factor = 3.0 / self._assist_level
        weight_factor = 75.0 / float(rider_weight_kg)
        expected = round(
            self._battery_wh * base_eff_km_per_Wh * assist_factor * weight_factor, 2
        )
        return expected

    # -- Setter functions --
    def set_price(self, price: float) -> None:
        if price < 0:
            raise (ValueError("Price cannot be negative."))
        else:
            self._price = price

    def set_discount_percent(self, pct: float) -> None:
        if pct >= 1 or pct < 0:
            raise (
                ValueError(
                    "Cannot have a negative percentage or a discount of over 100%"
                )
            )
        self._discount_percent = pct

    def set_stock(self, qty: int) -> None:
        if qty < 0:
            raise (ValueError("Stock cannot be negative."))
        self._stock = qty

    def set_active(self, active: bool) -> None:
        if active == True and self._stock <= 0:
            raise (ValueError("Cannot activate stock if stock is less than 0"))
        if type(active) != bool:
            raise (TypeError("active is not a boolean"))
        self._is_active = active

    def set_selected_color(self, color: str) -> None:
        if color not in self._available_colors:
            raise (ValueError("Color is not in the list of available colors"))
        self._selected_color = color

    def set_feature(self, feature: str, enabled: bool) -> None:
        if type(feature) != str or type(enabled) != bool:
            raise (TypeError("Wrong types for feature or enabled"))

        if not feature.strip():
            raise (TypeError("Cant be a empty string"))
        self._features[feature] = enabled

    def set_battery_wh(self, wh: int) -> None:
        if wh <= 0:
            raise (ValueError("wh cannot be non-positive or 0"))
        self._battery_wh = wh

    def set_assist_level(self, level: int) -> None:
        if level <= 0 or level > 5:
            raise (
                ValueError(
                    "Level cannot be non-positive or 0 or above the current assist level"
                )
            )
        self._assist_level = level

    # -- Checker flag functions --
    def is_on_sale(self) -> bool:
        return self._discount_percent > 0

    def is_active(self) -> bool:
        return self._stock > 0

    # -- Mutator functions --
    def add_color(self, color: str) -> None:
        if not isinstance(color, str):
            raise TypeError("color must be a string")

        color = color.strip()

        if not color:
            raise TypeError("color must be a non-empty string")
        elif color not in self._available_colors:
            self._available_colors.append(color)

    def remove_color(self, color: str) -> None:
        if color not in self._available_colors:
            raise (ValueError("Color is not in the list of available colors"))
        elif self._selected_color == color:
            raise (ValueError("Removed color cannot be the same as the selected color"))
        else:
            self._available_colors.remove(color)

    # -- Status functions --
    def __sizeof__(self) -> int:
        import sys

        # start with the shallow size of the instance itself (avoid recursion)
        total = object.__sizeof__(self)

        # include the attribute dict (shallow)
        d = getattr(self, "__dict__", None)
        if d is not None:
            total += sys.getsizeof(d)

        # scalars/strings
        total += sys.getsizeof(self._name)
        total += sys.getsizeof(self._price)
        total += sys.getsizeof(self._stock)
        total += sys.getsizeof(self._is_active)
        total += sys.getsizeof(self._weight_kg)
        total += sys.getsizeof(self._battery_wh)
        total += sys.getsizeof(self._assist_level)
        total += sys.getsizeof(self._discount_percent)
        total += sys.getsizeof(self._selected_color)

        # list of colors: list shell + each string
        total += sys.getsizeof(self._available_colors)
        for c in self._available_colors:
            total += sys.getsizeof(c)

        # features dict: dict shell + each key and value
        total += sys.getsizeof(self._features)
        for k, v in self._features.items():
            total += sys.getsizeof(k) + sys.getsizeof(v)

        return total
