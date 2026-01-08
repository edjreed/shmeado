"""Provides heavily-used general/game-specific levelling functions."""

import math
from stats.constants import get_constants


CONSTANTS = get_constants("stats")


# ======================================================================================
# GENERAL
# ======================================================================================


def network_xp_to_level(xp):
    """Convert Hypixel network XP to network level."""
    return round((math.sqrt((2 * xp) + 30625) / 50) - 2.5, 2)


def network_level_to_xp(level):
    """Convert Hypixel network level to network XP."""
    return ((((level + 2.5) * 50) ** 2) - 30625) / 2


def pet_xp_to_level(xp):
    """Convert pet XP to level."""
    level = 0
    levels = CONSTANTS["general"]["petLevels"]
    for i, req in enumerate(levels.values()):
        if level == 100:
            return 100
        if xp - req >= 0:
            xp -= req
            level += 1
        else:
            return round(level + (xp / req), 2)


# ======================================================================================
# BEDWARS
# ======================================================================================

BEDWARS_EASY_LEVELS = 4
BEDWARS_EASY_LEVELS_XP = 7000
BEDWARS_XP_PER_PRESTIGE = (96 * 5000) + BEDWARS_EASY_LEVELS_XP
BEDWARS_LEVELS_PER_PRESTIGE = 100
BEDWARS_HIGHEST_PRESTIGE = 10


def bedwars_xp_per_level(level):
    """Return the XP required to reach the specified BedWars level."""
    if level == 0:
        return 0

    if level > BEDWARS_HIGHEST_PRESTIGE * BEDWARS_LEVELS_PER_PRESTIGE:
        respectedLevel = level - BEDWARS_HIGHEST_PRESTIGE * BEDWARS_LEVELS_PER_PRESTIGE
    else:
        respectedLevel = level % BEDWARS_LEVELS_PER_PRESTIGE

    if respectedLevel > BEDWARS_EASY_LEVELS:
        return 5000

    if respectedLevel == 1:
        return 500
    if respectedLevel == 2:
        return 1000
    if respectedLevel == 3:
        return 2000
    if respectedLevel == 4:
        return 3500
    else:
        return 5000


def bedwars_xp_to_level(xp):
    """Convert BedWars XP to level."""
    prestiges = math.floor(xp / BEDWARS_XP_PER_PRESTIGE)
    level = prestiges * BEDWARS_LEVELS_PER_PRESTIGE
    expWithoutPrestiges = xp - (prestiges * BEDWARS_XP_PER_PRESTIGE)

    i = 1
    while i <= BEDWARS_EASY_LEVELS:
        expForEasyLevel = bedwars_xp_per_level(i)
        i = i + 1
        if expWithoutPrestiges < expForEasyLevel:
            break
        level = level + 1
        expWithoutPrestiges = expWithoutPrestiges - expForEasyLevel
    level = level + (expWithoutPrestiges / 5000)
    return round(level, 4)


def bedwars_next_prestige(level):
    """Return the starting level of the next BedWars prestige."""
    return level + 100 - (level % 100)


def bedwars_prev_prestige(level):
    """Return the starting level of the current BedWars prestige."""
    return int(level - (level % 100))


def bedwars_format_prestige(level):
    """Return a formatted HTML element for a BedWars level."""
    level = int(level)

    prestiges = CONSTANTS["bedwars"]["prestiges"]
    emblems = CONSTANTS["bedwars"]["emblems"]

    emblem = None
    for req, e in emblems.items():
        if level >= int(req):
            emblem = e

    info = prestiges[str(bedwars_prev_prestige(level))]
    scheme = info.get("scheme", info["color"])

    if isinstance(scheme, str):
        return f"<span class='{scheme}'>[{level}{emblem}]</span>"
    else:
        unformatted = f"[{level}{emblem}]"
        formatted = ""
        for i, char in enumerate(unformatted):
            formatted += f"<span class='{scheme[i]}'>{char}</span>"
        return formatted


# ======================================================================================
# SKYWARS
# ======================================================================================


def skywars_xp_to_level(xp):
    """Convert SkyWars XP to level."""
    level_totals = [
        0, 10, 35, 85, 160, 260, 510, 1010, 1760, 2760, 4010, 5510, 7260, 9260, 11760,
        14760, 18260, 22260, 26760
    ]
    level_amounts = [
        10, 25, 50, 75, 100, 250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 
        3500, 4000, 4500, 5000
    ]
    if xp >= 26760:
        level = "{:.4f}".format(round(((xp - 26760) / 5000) + 19, 4))
    else:
        count = -1
        found = False
        while not found:
            count += 1
            if xp >= level_totals[count]:
                found = False
            else:
                found = True
                level = (
                    count + 1 + ((xp - level_totals[count]) / level_amounts[count - 1])
                )
                level = "{:.4f}".format(round((level * 5000) / 5000, 4))
    return level


def skywars_xp_to_level_old(xp):
    """Convert SkyWars XP to level as per the old levelling system."""
    level_totals = [0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
    level_amounts = [20, 50, 80, 100, 250, 500, 1000, 1500, 2500, 4000, 5000, 10000]
    if xp >= 15000:
        level = "{:.4f}".format(round(((xp - 15000) / 10000) + 12, 1))
    else:
        count = -1
        found = False
        while not found:
            count += 1
            if xp >= level_totals[count]:
                found = False
            else:
                found = True
                level = (
                    count + 1 + ((xp - level_totals[count]) / level_amounts[count - 1])
                )
                level = "{:.1f}".format(round((level * 10000) / 10000, 1))
    return level


def skywars_next_prestige(level):
    """Return the starting level of the next SkyWars prestige."""
    return 1000 if level >= 500 else int((level // 10) * 10) + 10


def skywars_prev_prestige(level):
    """Return the starting level of the current SkyWars prestige."""
    if level >= 1000:
        return 1000
    elif level >= 500:
        return 500
    else:
        return int((level // 10) * 10)


def skywars_format_prestige(level, emblem, scheme=False):
    """Return a formatted HTML element for a SkyWars level."""
    # Prepare input parameters for constants compatibility
    level = int(level)
    emblem = emblem.replace("emblem_", "")
    scheme = scheme.replace("scheme_", "") if scheme else False

    # Demigod is the only scheme with curly brackets
    brackets = ["{", "}"] if scheme == "demigod" else ["[", "]"]

    # Prepare constants
    prestiges = CONSTANTS["skywars"]["prestiges"]
    emblems = CONSTANTS["skywars"]["emblems"]
    schemes = CONSTANTS["skywars"]["schemes"]

    # Determine emblem and scheme
    emblem = emblems.get(emblem, emblems["default"])
    if scheme:
        # Use the given scheme
        scheme = schemes.get(scheme, schemes["default"])
    else:
        # Identify the scheme using the prestige name
        scheme_name = (
            prestiges[str(skywars_prev_prestige(level))]["name"]
            .lower()
            .replace(" ", "_")
            + "_prestige"
        )
        scheme = schemes.get(scheme_name, schemes["default"])

    # Uniform color scheme
    if isinstance(scheme, str):
        return f"<span class='{scheme}'>[{level}{emblem}]</span>"

    # Varied color scheme
    else:
        formatted = f"<span class='{scheme['brackets'][0]}'>{brackets[0]}</span>"
        for i, char in enumerate(str(level)):
            # Reset count as schemes only cover three-digit levels
            if level >= 1000 and i >= len(scheme["level"]):
                i = 0
            formatted += f"<span class='{scheme['level'][i]}'>{char}</span>"
        formatted += f"<span class='{scheme['emblem']}'>{emblem}</span>"
        formatted += f"<span class='{scheme['brackets'][1]}'>{brackets[1]}</span>"
        return formatted
