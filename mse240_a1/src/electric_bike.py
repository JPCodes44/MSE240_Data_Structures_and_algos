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
