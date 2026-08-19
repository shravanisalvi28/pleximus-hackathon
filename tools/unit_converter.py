"""
Unit converter tool — local conversion logic, no external API.
Supports: Length (m, km, cm, miles, feet),
          Weight (kg, g, pounds),
          Temperature (Celsius, Fahrenheit, Kelvin).
"""


# ---------------------------------------------------------------------------
# Conversion tables — all values are relative to a base unit
# Length base: meter | Weight base: kilogram | Temperature: handled separately
# ---------------------------------------------------------------------------

LENGTH_TO_METER = {
    "meter": 1.0,
    "meters": 1.0,
    "m": 1.0,
    "kilometer": 1000.0,
    "kilometers": 1000.0,
    "km": 1000.0,
    "centimeter": 0.01,
    "centimeters": 0.01,
    "cm": 0.01,
    "mile": 1609.344,
    "miles": 1609.344,
    "mi": 1609.344,
    "foot": 0.3048,
    "feet": 0.3048,
    "ft": 0.3048,
}

WEIGHT_TO_KG = {
    "kilogram": 1.0,
    "kilograms": 1.0,
    "kg": 1.0,
    "gram": 0.001,
    "grams": 0.001,
    "g": 0.001,
    "pound": 0.453592,
    "pounds": 0.453592,
    "lb": 0.453592,
    "lbs": 0.453592,
}

TEMPERATURE_UNITS = {"celsius", "c", "fahrenheit", "f", "kelvin", "k"}


def _normalize_unit(unit: str) -> str:
    return unit.strip().lower()


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between temperature scales."""
    from_unit = from_unit.replace("°", "").strip()
    to_unit = to_unit.replace("°", "").strip()

    # Normalize to Celsius first
    if from_unit in ("celsius", "c"):
        celsius = value
    elif from_unit in ("fahrenheit", "f"):
        celsius = (value - 32) * 5 / 9
    elif from_unit in ("kelvin", "k"):
        celsius = value - 273.15
    else:
        raise ValueError(f"Unknown temperature unit: '{from_unit}'")

    # Convert from Celsius to target
    if to_unit in ("celsius", "c"):
        return celsius
    elif to_unit in ("fahrenheit", "f"):
        return celsius * 9 / 5 + 32
    elif to_unit in ("kelvin", "k"):
        return celsius + 273.15
    else:
        raise ValueError(f"Unknown temperature unit: '{to_unit}'")


def convert_unit(value: float, from_unit: str, to_unit: str) -> str:
    """
    Convert a numeric value from one unit to another.

    Args:
        value     : The numeric value to convert.
        from_unit : The source unit as a string (e.g., "km", "kg", "Fahrenheit").
        to_unit   : The target unit as a string (e.g., "meters", "pounds", "Celsius").

    Returns:
        A human-readable result string, or an error message.
    """
    from_norm = _normalize_unit(from_unit)
    to_norm = _normalize_unit(to_unit)

    # ---- Temperature ----
    if from_norm in TEMPERATURE_UNITS or to_norm in TEMPERATURE_UNITS:
        try:
            result = _convert_temperature(value, from_norm, to_norm)
        except ValueError as e:
            return str(e)
        return f"{value} {from_unit} = {round(result, 4)} {to_unit}"

    # ---- Length ----
    if from_norm in LENGTH_TO_METER and to_norm in LENGTH_TO_METER:
        meters = value * LENGTH_TO_METER[from_norm]
        result = meters / LENGTH_TO_METER[to_norm]
        return f"{value} {from_unit} = {round(result, 6)} {to_unit}"

    # ---- Weight ----
    if from_norm in WEIGHT_TO_KG and to_norm in WEIGHT_TO_KG:
        kg = value * WEIGHT_TO_KG[from_norm]
        result = kg / WEIGHT_TO_KG[to_norm]
        return f"{value} {from_unit} = {round(result, 6)} {to_unit}"

    # ---- Unsupported ----
    if from_norm not in {**LENGTH_TO_METER, **WEIGHT_TO_KG, **dict.fromkeys(TEMPERATURE_UNITS)}:
        return f"Unsupported source unit: '{from_unit}'."
    if to_norm not in {**LENGTH_TO_METER, **WEIGHT_TO_KG, **dict.fromkeys(TEMPERATURE_UNITS)}:
        return f"Unsupported target unit: '{to_unit}'."
    return (
        f"Cannot convert '{from_unit}' to '{to_unit}' — "
        "they belong to different measurement categories."
    )
