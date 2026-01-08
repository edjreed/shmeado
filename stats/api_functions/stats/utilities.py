"""Provides common general stats functions."""

import re


def camel_to_snake(str):
    """Convert camelCase to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", str).lower()


def get_ratio(one, two, dp=3):
    """Return the ratio of one to two, rounded to dp decimal places."""
    if two == 0:
        return round(one, dp)
    else:
        return round((one / two), dp)


def get_ratios(dict, ratios):
    """Return a dictionary with the specified ratios calculated."""
    for ratio, keys in ratios.items():
        dict[ratio] = get_ratio(dict.get(keys[0], 0), dict.get(keys[1], 0))
    return dict


def get_percentage(one, two, dp=2):
    """Return one as a % of two, rounded to dp decimal places."""
    if one == 0:
        return 0
    elif two == 0:
        return 100
    else:
        return round(one / two * 100, dp)


def romanize(num):
    """Convert an integer to a Roman numeral."""
    num = int(num)
    if num == 0:
        return "0"

    val_map = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    roman = ""
    for value, numeral in val_map:
        while num >= value:
            roman += numeral
            num -= value
    return roman
