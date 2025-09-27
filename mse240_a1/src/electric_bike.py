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

    def __init_(
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
        self.price: float = float(price)
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
                self._selected_color = selected_color

        # Active is derived from the stock initially
        self._is_active: bool = self._stock > 0

    # --- Required accessors ---
    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        """Base price before any discount."""
        return self._price

    # --- Additional accessors/mutators ---
    def set_price(self, price: float) -> None:
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("price must be a non-negative number")
        self._price = float(price)

    def get_current_price(self) -> float:
        """Computed price after discount, rounded to cents."""
        return round(self._price * (1.0 - self._discount_percent), 2)

    def set_discount_percent(self, pct: float) -> None:
        if not isinstance(pct, (int, float)) or not (0.0 <= pct < 1.0):
            raise ValueError("discount_percent must be in [0.0, 1.0)")
        self._discount_percent = float(pct)

    def is_on_sale(self) -> bool:
        return self._discount_percent > 0.0

    def get_stock(self) -> int:
        return self._stock

    def set_stock(self, qty: int) -> None:
        if not isinstance(qty, int) or qty < 0:
            raise ValueError("stock must be a non-negative int")
        self._stock = qty
        if self._stock == 0:
            self._is_active = False
        else:
            # If stock was replenished and was previously inactive *only due to stock*,
            # default to making it active again.
            self._is_active = True

    def is_active(self) -> bool:
        return self._is_active

    def set_active(self, active: bool) -> None:
        if not isinstance(active, bool):
            raise TypeError("active must be a bool")
        if active and self._stock == 0:
            raise ValueError("cannot activate item with zero stock")
        self._is_active = active

    def get_weight_kg(self) -> float:
        return self._weight_kg

    def get_weight_lb(self) -> float:
        return round(self._weight_kg * 2.2046226218, 3)

    def get_available_colors(self) -> List[str]:
        return list(self._available_colors)  # defensive copy

    def add_color(self, color: str) -> None:
        if not isinstance(color, str) or not color.strip():
            raise TypeError("color must be a non-empty string")
        if color in self._available_colors:
            return
        self._available_colors.append(color)

    def remove_color(self, color: str) -> None:
        if color not in self._available_colors:
            raise ValueError("color not in available_colors")
        if color == self._selected_color:
            raise ValueError("cannot remove the currently selected color")
        self._available_colors.remove(color)

    def get_selected_color(self) -> str:
        return self._selected_color

    def set_selected_color(self, color: str) -> None:
        if color not in self._available_colors:
            raise ValueError("selected_color must exist in available_colors")
        self._selected_color = color

    def get_features(self) -> Dict[str, bool]:
        return dict(self._features)  # defensive copy

    def set_feature(self, feature: str, enabled: bool) -> None:
        if not isinstance(feature, str) or not feature.strip():
            raise TypeError("feature must be a non-empty string")
        if not isinstance(enabled, bool):
            raise TypeError("enabled must be bool")
        self._features[feature] = enabled

    def get_battery_wh(self) -> int:
        return self._battery_wh

    def set_battery_wh(self, wh: int) -> None:
        if not isinstance(wh, int) or wh <= 0:
            raise ValueError("battery_wh must be a positive int")
        self._battery_wh = wh

    def get_assist_level(self) -> int:
        return self._assist_level

    def set_assist_level(self, level: int) -> None:
        if not isinstance(level, int) or not (1 <= level <= 5):
            raise ValueError("assist_level must be an int in [1..5]")
        self._assist_level = level

    def get_estimated_range_km(self, rider_weight_kg: float = 75.0) -> float:
        """Very rough range estimate.

        Model: base_efficiency = 0.16 km/Wh at assist level 3 and rider 75 kg.
        Efficiency scales inversely with assist level and rider weight.
        This is for demonstration/testing only.
        """
        if not isinstance(rider_weight_kg, (int, float)) or rider_weight_kg <= 0:
            raise ValueError("rider_weight_kg must be positive")
        base_eff_km_per_Wh = 0.16
        assist_factor = 3.0 / self._assist_level
        weight_factor = 75.0 / float(rider_weight_kg)
        eff = base_eff_km_per_Wh * assist_factor * weight_factor
        return round(self._battery_wh * eff, 2)

    # --- Size accounting (empirical) ---
    def __sizeof__(self) -> int:
        """Return an approximate size based on members. For empirical comparisons."""
        total = sys.getsizeof(self.__dict__)
        for v in self.__dict__.values():
            try:
                total += sys.getsizeof(v)
            except Exception:
                pass
            if isinstance(v, dict):
                for k2, v2 in v.items():
                    total += sys.getsizeof(k2) + sys.getsizeof(v2)
            elif isinstance(v, (list, tuple, set)):
                for it in v:
                    total += sys.getsizeof(it)
        return total
