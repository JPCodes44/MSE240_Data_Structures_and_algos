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
