# ElectricBike — MSE 240 Assignment 1

A small, typed Python class modeling an electric bicycle for an online storefront. It demonstrates invariants, validation, calculated accessors, and a shallow memory-size estimator.

> **Author:** Justin Mak
> **Date:** 2025-09-27

---

## Overview

`ElectricBike` represents a single e-bike item with:

* validated attributes (name, price, stock, battery Wh, assist level, etc.),
* guardrails for setters,
* derived values like discounted price, weight in pounds, and estimated range.

---

## Features

* **Validation & Invariants**

  * `price ≥ 0`, `stock ≥ 0`
  * `0 ≤ discount_percent < 1`
  * `assist_level ∈ {1..5}`
  * `selected_color ∈ available_colors`
  * `battery_wh > 0`, `weight_kg > 0`
* **Derived values**

  * `get_current_price()` (price after discount, rounded to cents)
  * `get_estimated_range_km()` (battery × efficiency × rider/assist factors)
  * `get_weight_lb()` (kg → lb)
* **Color & feature management**

  * `add_color`, `remove_color`, `set_selected_color`
  * `set_feature(feature: str, enabled: bool)`
* **Memory note**

  * `__sizeof__()` reports a shallow/deep-ish estimate by summing selected fields.

---

## Class Diagram (Mermaid)

```mermaid
classDiagram
class ElectricBike {
  - _name: str
  - _price: float
  - _stock: int
  - _is_active: bool
  - _weight_kg: float
  - _battery_wh: int
  - _assist_level: int
  - _discount_percent: float
  - _selected_color: str
  - _available_colors: List~str~
  - _features: Dict~str,bool~

  + ElectricBike(name: str, price: float, stock: int=0, weight_kg: float=22.5,
                 available_colors: List~str~=None, selected_color: str=None,
                 features: Dict~str,bool~=None, battery_wh: int=450,
                 assist_level: int=3, discount_percent: float=0.0)

  + get_current_price() float
  + get_estimated_range_km(rider_weight_kg: float=75.0) float
  + get_weight_lb() float
  + set_price(price: float) void
  + set_discount_percent(pct: float) void
  + set_stock(qty: int) void
  + set_active(active: bool) void
  + set_selected_color(color: str) void
  + add_color(color: str) void
  + remove_color(color: str) void
  + set_feature(feature: str, enabled: bool) void
  + set_battery_wh(wh: int) void
  + set_assist_level(level: int) void
  + is_on_sale() bool
  + is_active() bool
  + __sizeof__() int
}
```

---

## Getting Started

### Requirements

* Python **3.10+**
* Optional: `pytest` for tests

### Install (venv recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # if present
pip install pytest
```

---

## Usage

```python
from electric_bike import ElectricBike  # adjust path as needed

eb = ElectricBike(
    name="MEC Midtown 2 Bicycle",
    price=1299.99,
    stock=2,
    available_colors=["black", "blue", "red"],
    selected_color="black",
    battery_wh=500,
    assist_level=3,
)

print(eb.get_current_price())         # 1299.99 (no discount)
eb.set_discount_percent(0.10)
print(eb.get_current_price())         # 1169.99

print(eb.get_estimated_range_km(75))  # range estimate (km)
print(eb.get_weight_lb())             # kg -> lb

eb.add_color("silver")
eb.set_selected_color("silver")
eb.set_stock(0)
print(eb.is_active())                 # False
```

**Common errors raised intentionally**

* `ValueError`: negative price/stock, discount outside `[0,1)`, invalid assist level, color not in list, non-positive battery Wh, removing the currently selected color.
* `TypeError`: wrong argument types (non-string color, non-bool flags, non-int Wh, etc.).

---

## API (Quick Reference)

* **Queries**

  * `get_name() -> str`
  * `get_price() -> float`
  * `get_current_price() -> float`
  * `get_weight_kg() -> float`, `get_weight_lb() -> float`
  * `get_stock() -> int`
  * `get_available_colors() -> list[str]`
  * `get_features() -> dict[str, bool]`
  * `get_selected_color() -> str`
  * `get_battery_wh() -> int`
  * `get_assist_level() -> int`
  * `get_estimated_range_km(rider_weight_kg: float = 75.0) -> float`
  * `is_on_sale() -> bool`, `is_active() -> bool`

* **Commands**

  * `set_price(price: float) -> None`
  * `set_discount_percent(pct: float) -> None`
  * `set_stock(qty: int) -> None`
  * `set_active(active: bool) -> None`
  * `set_selected_color(color: str) -> None`
  * `add_color(color: str) -> None`
  * `remove_color(color: str) -> None`
  * `set_feature(feature: str, enabled: bool) -> None`
  * `set_battery_wh(wh: int) -> None`
  * `set_assist_level(level: int) -> None`
  * `__sizeof__() -> int`

---

## Testing

Run the test suite:

```bash
pytest -q
```

The tests cover typical cases, bounds, type errors, and rules/guards (e.g., `set_active(True)` is forbidden if `stock == 0`).

---

## Memory Footprint Notes

`__sizeof__()` estimates memory by summing:

* the instance shell (`object.__sizeof__(self)`),
* the attribute dict shell,
* shallow sizes of scalar fields,
* list/dict shells **plus** shallow sizes of contained strings and feature keys/values.

> `sys.getsizeof("Bike")` showing **45 bytes** is normal: CPython strings include header + payload (PEP 393). Values vary across Python versions and platforms.

---

## Project Structure (suggested)

```
.
├─ src/
│  └─ electric_bike.py
├─ test_electric_bike.py
│  
├─ docs/
│  ├─ report.tex
│  └─ images/
└─ README.md
```

---

## License

MIT (or update to your course’s required license).
