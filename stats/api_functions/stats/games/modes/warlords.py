from ... import utilities as u
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate all warlords stats from a player API."""
    stats = {}

    # If player has not played warlords, prepare empty dict
    try:
        warlords = player_api["player"]["stats"]["Battleground"]
    except LookupError:
        warlords = {}

    # Main Stats
    stats_needed = [
        "wins",
        "losses",
        "kills",
        "deaths",
        "coins",
        "void_shards",
        "magic_dust",
        "assists",
        "flag_conquer_self",
        "flag_returns",
    ]

    for stat in stats_needed:
        stats[stat] = warlords.get(stat, 0)

    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])

    # Main Table
    wl_head = ["Mode", "Wins", "Kills"]
    wl_cols = ["wins", "kills"]
    wl_modes = {
        "capturetheflag": "Capture the Flag",
        "domination": "Domination",
        "teamdeathmatch": "Team Deathmatch",
    }

    wl_rows = []
    for mode in wl_modes:
        row = {}
        for col in wl_cols:
            row[col] = int(warlords.get(f"{col}_{mode}", 0))

        wl_rows.append(
            [
                wl_modes[mode],
                row["wins"],
                row["kills"],
            ]
        )

    stats["table"] = {
        "id": "tableWarlords",
        "head": wl_head,
        "rows": wl_rows,
        "boldCols": [0],
    }

    # Weapons
    stats["repaired"] = warlords.get("repaired", 0)
    for weapon in ["common", "rare", "epic", "legendary"]:
        stats[f"repaired_{weapon}"] = warlords.get(f"repaired_{weapon}", 0)

    stats["weapon_inv"] = warlords.get("weapon_inventory", [])
    WEAPON_SCORES = get_constants("stats")["modes"]["warlords"]["weaponScores"]

    for weapon in stats["weapon_inv"]:
        for attr in weapon:
            if type(weapon[attr]) is bool:
                weapon[attr] = str(weapon[attr])

        score = 0
        score += weapon["damage"] * (1 + weapon["upgradeTimes"] * 0.075)
        score += weapon["chance"]
        score += weapon["multiplier"]
        score += weapon["ability"] * (1 + weapon["upgradeTimes"] * 0.075)
        score += weapon["health"] * (1 + weapon["upgradeTimes"] * 0.25)
        score += weapon["energy"] * (1 + weapon["upgradeTimes"] * 0.1)
        score += weapon["cooldown"] * (1 + weapon["upgradeTimes"] * 0.075)
        score += weapon["movement"] * (1 + weapon["upgradeTimes"] * 0.075)

        for prefix in WEAPON_SCORES[weapon["category"]]:
            if score >= prefix["score"]:
                weapon["prefix"] = prefix["prefix"]

    # Classes Table
    wl_classes_head = [
        "Class",
        "Wins",
        "Losses",
        "W/L",
        "Damage",
        "Damage Prevented",
        "Healing",
    ]
    wl_classes_cols = ["wins", "losses", "damage", "damage_prevented", "heal"]
    wl_classes = {
        "": "Overall",
        "_mage": "Mage",
        "_warrior": "Warrior",
        "_paladin": "Paladin",
        "_shaman": "Shaman",
    }
    wl_classes_upgrades = [
        "cooldown",
        "critchance",
        "critmultiplier",
        "energy",
        "health",
        "skill1",
        "skill2",
        "skill3",
        "skill4",
        "skill5",
    ]

    wl_classes_rows = []
    for wl_class in wl_classes:
        row = {}
        for col in wl_classes_cols:
            row[col] = int(warlords.get(f"{col}{wl_class}", 0))

        if wl_class != "":
            row["level"] = 0
            for upgrade in wl_classes_upgrades:
                row["level"] += warlords.get(
                    f"{wl_class.replace('_', '')}_{upgrade}", 0
                )

        wl_classes_rows.append(
            [
                f"<span class='gray'>[Lv{row['level']}] </span><span class='gold'>{wl_classes[wl_class]}</span>"
                if wl_class != ""
                else wl_classes[wl_class],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["damage"],
                row["damage_prevented"],
                row["heal"],
            ]
        )

    stats["table_classes"] = {
        "id": "tableWarlordsClasses",
        "head": wl_classes_head,
        "rows": wl_classes_rows,
        "boldRows": [1],
        "boldCols": [0],
        "percent": [3],
        "buttons": {"W/L": [0, 1, 2, 3], "Damage": [0, 4, 5], "Healing": [0, 6]},
    }

    return stats
