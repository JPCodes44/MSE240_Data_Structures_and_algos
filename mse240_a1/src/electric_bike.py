"""
ElectricBike: Online-store item class for an e-bike.

Author: Justin Mak
Assignment: MSE 240 - Assignment 1
Date: 2025-09-27

Description:
  Represents an electric bicycle being sold in an online store. Satisfies assignment
  constraints: string name, floar price, boolean(s), integer(s), list/dict attrivutes,
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
