from .. import utilities as u, levelling as l
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate all BedWars stats from a player API."""
    stats = {}

    # If player has not played BedWars, prepare empty dict
    try:
        bedwars = player_api["player"]["stats"].get("Bedwars", {})
    except LookupError:
        bedwars = {}

    # ==================================================================================
    # GENERAL
    # ==================================================================================

    stats_needed = [
        # Main
        "wins_bedwars",
        "losses_bedwars",
        "final_kills_bedwars",
        "final_deaths_bedwars",
        "kills_bedwars",
        "deaths_bedwars",
        "winstreak",
        "Experience",
        # More
        "beds_broken_bedwars",
        "beds_lost_bedwars",
        "items_purchased_bedwars",
        "void_final_kills_bedwars",
        "entity_attack_final_kills_bedwars",
        "void_final_deaths_bedwars",
        "entity_attack_final_deaths_bedwars",
        "eight_one_winstreak",
        "eight_two_winstreak",
        "four_three_winstreak",
        "four_four_winstreak",
        "bedwars_boxes",
        "bedwars_christmas_boxes",
        "bedwars_halloween_boxes",
        "bedwars_easter_boxes",
        "bedwars_lunar_boxes",
        "coins",
        "iron_resources_collected_bedwars",
        "gold_resources_collected_bedwars",
        "diamond_resources_collected_bedwars",
        "emerald_resources_collected_bedwars",
    ]

    # Collect all initial stats
    for stat in stats_needed:
        stats[stat] = bedwars.get(stat, 0)

    stats["games_played"] = stats["wins_bedwars"] + stats["losses_bedwars"]

    # Levelling and prestige
    stats["level"] = l.bedwars_xp_to_level(stats["Experience"])
    stats["prestige_formatted"] = l.bedwars_format_prestige(stats["level"])

    # Calculate ratios
    stats = u.get_ratios(
        stats,
        {
            "win_loss": ["wins_bedwars", "losses_bedwars"],
            "kill_death": ["kills_bedwars", "deaths_bedwars"],
            "final_kill_death": ["final_kills_bedwars", "final_deaths_bedwars"],
            "beds_broken_lost": ["beds_broken_bedwars", "beds_lost_bedwars"],
            "beds_win": ["beds_broken_bedwars", "wins_bedwars"],
            "beds_game": ["beds_broken_bedwars", "games_played"],
            "final_kills_win": ["final_kills_bedwars", "wins_bedwars"],
            "final_kills_game": ["final_kills_bedwars", "games_played"],
            "experience_win": ["Experience", "wins_bedwars"],
            "experience_game": ["Experience", "games_played"],
        },
    )

    # Total boxes
    stats["total_boxes"] = 0
    for box in [
        "bedwars_boxes",
        "bedwars_christmas_boxes",
        "bedwars_halloween_boxes",
        "bedwars_easter_boxes",
        "bedwars_lunar_boxes",
    ]:
        stats["total_boxes"] += stats[box]

    # ==================================================================================
    # PRESTIGE
    # ==================================================================================

    level = stats["level"]
    prestiges = get_constants("stats")["bedwars"]["prestiges"]

    prev_pres = str(l.bedwars_prev_prestige(int(level)))
    next_pres = str(l.bedwars_next_prestige(int(level)))

    progress = int(stats["Experience"] % l.BEDWARS_XP_PER_PRESTIGE)
    remaining = l.BEDWARS_XP_PER_PRESTIGE - progress

    stats["prestige"] = {
        "previous": {
            "level": prev_pres,
            "name": prestiges[prev_pres]["name"],
            "color": prestiges[prev_pres]["color"],
            "formatted": l.bedwars_format_prestige(int(prev_pres)),
        },
        "next": {
            "level": next_pres,
            "name": prestiges[next_pres]["name"],
            "color": prestiges[next_pres]["color"],
            "formatted": l.bedwars_format_prestige(int(next_pres)),
        },
        "progress": {
            "current": {"color": prestiges[prev_pres]["color"], "progress": progress},
            "next": {
                "color": prestiges[next_pres]["color"],
                "needed": l.BEDWARS_XP_PER_PRESTIGE,
            },
        },
        "remaining": remaining,
        "percent": u.get_percentage(progress, l.BEDWARS_XP_PER_PRESTIGE),
    }

    # Calculate estimated stats at next prestige
    proceed = True  # Flag to prevent zero division error
    relevant = ["wins", "final_kills", "beds_broken"]
    for stat in relevant:
        if stats[f"{stat}_bedwars"] == 0:
            proceed = False

    wins_estimated = (
        remaining / (stats["Experience"] / stats["wins_bedwars"]) if proceed else None
    )

    for stat in ["final_kills", "beds_broken"]:
        if proceed:
            value = int(
                stats[f"{stat}_bedwars"] / stats["wins_bedwars"] * wins_estimated
            )
        else:
            value = "Unknown"
        stats["prestige"][f"{stat}_estimated"] = value

    stats["prestige"]["wins_estimated"] = int(wins_estimated) if proceed else "Unknown"

    for stat in relevant:
        if proceed:
            value = stats[f"{stat}_bedwars"] + stats["prestige"][f"{stat}_estimated"]
        else:
            value = "Unknown"
        stats["prestige"][f"{stat}_at"] = value

    # ==================================================================================
    # TABLE
    # ==================================================================================

    head = [
        "Mode",
        "Wins",
        "Losses",
        "W/L",
        "Final Kills",
        "Final Deaths",
        "Final K/D",
        "Kills",
        "Deaths",
        "K/D",
        "Beds Broken",
    ]
    modes = {
        "": "Overall",
        "two_four_": "4v4",
        "eight_one_": "Solo",
        "eight_two_": "Doubles",
        "four_three_": "3v3v3v3",
        "four_four_": "4v4v4v4",
    }

    rows = []
    for mode in modes:
        row = {}
        for col in [
            "wins",
            "losses",
            "final_kills",
            "final_deaths",
            "kills",
            "deaths",
            "beds_broken",
        ]:
            row[col] = bedwars.get(f"{mode}{col}_bedwars", 0)

        rows.append(
            [
                modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["final_kills"],
                row["final_deaths"],
                u.get_ratio(row["final_kills"], row["final_deaths"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["beds_broken"],
            ]
        )

    stats["table"] = {
        "id": "tableBedWars",
        "head": head,
        "rows": rows,
        "green": {3: 10, 6: 30},
        "boldRows": [1],
        "percent": [3],
        "decimal": [6, 9],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "FK/D": [0, 4, 5, 6],
            "K/D": [0, 7, 8, 9],
            "Beds": [0, 10],
        },
    }

    # ==================================================================================
    # BEDS
    # ==================================================================================

    head = [
        "Mode",
        "Beds Broken",
        "Beds Lost",
        "Beds Broken/Beds Lost",
        "Beds Broken/Win",
        "Beds Broken/Game",
    ]
    modes = {
        "": "Overall",
        "two_four_": "4v4",
        "eight_one_": "Solo",
        "eight_two_": "Doubles",
        "four_three_": "3v3v3v3",
        "four_four_": "4v4v4v4",
    }

    rows = []
    for mode in modes:
        row = {}
        for col in ["wins", "losses", "beds_broken", "beds_lost"]:
            row[col] = bedwars.get(f"{mode}{col}_bedwars", 0)

        rows.append(
            [
                modes[mode],
                row["beds_broken"],
                row["beds_lost"],
                u.get_ratio(row["beds_broken"], row["beds_lost"]),
                u.get_ratio(row["beds_broken"], row["wins"]),
                u.get_ratio(row["beds_broken"], row["wins"] + row["losses"]),
            ]
        )

    stats["table_beds"] = {
        "id": "tableBedsBedWars",
        "head": head,
        "rows": rows,
        "boldRows": [1],
        "decimal": [3, 4, 5],
        "buttons": {
            "Broken": [0, 1],
            "Lost": [0, 2],
            "BB/BL": [0, 3],
            "BB/W": [0, 4],
            "BB/G": [0, 5],
        },
    }

    # ==================================================================================
    # CARRIES
    # ==================================================================================

    head = ["Mode", "Carries", "Wins", "% of Wins"]
    modes = {
        "": "Overall",
        "two_four_": "4v4",
        "eight_two_": "Doubles",
        "four_three_": "3v3v3v3",
        "four_four_": "4v4v4v4",
    }

    rows = []
    for mode in modes:
        row = {}
        for col in ["wins", "losses", "final_deaths"]:
            row[col] = bedwars.get(f"{mode}{col}_bedwars", 0)

        carries = abs(row["final_deaths"] - row["losses"])

        rows.append(
            [
                modes[mode],
                carries,
                row["wins"],
                f"{u.get_percentage(carries, row['wins'], 2)}%",
            ]
        )

    stats["table_carries"] = {
        "id": "tableCarriesBedWars",
        "head": head,
        "rows": rows,
        "boldRows": [1],
        "width": 520,
    }

    total_carries = 0
    for row in rows[1:]:
        total_carries += row[1]
    rows[0][1] = total_carries
    stats["carries_bedwars"] = total_carries

    # ==================================================================================
    # DREAM
    # ==================================================================================

    head = [
        "Mode",
        "Wins",
        "Losses",
        "W/L",
        "Final Kills",
        "Final Deaths",
        "Final K/D",
        "Kills",
        "Deaths",
        "K/D",
        "Beds Broken",
    ]
    modes = {
        "castle": "Castle",
        "eight_one_rush": "Rush Solo",
        "eight_two_rush": "Rush Doubles",
        "four_four_rush": "Rush 4v4v4v4",
        "eight_one_ultimate": "Ultimate Solo",
        "eight_two_ultimate": "Ultimate Doubles",
        "four_four_ultimate": "Ultimate 4v4v4v4",
        "eight_two_lucky": "Lucky Doubles",
        "four_four_lucky": "Lucky 4v4v4v4",
        "eight_two_armed": "Armed Doubles",
        "four_four_armed": "Armed 4v4v4v4",
    }

    rows = []
    for mode in modes:
        row = {}
        for col in [
            "wins",
            "losses",
            "final_kills",
            "final_deaths",
            "kills",
            "deaths",
            "beds_broken",
        ]:
            row[col] = bedwars.get(f"{mode}_{col}_bedwars", 0)

        rows.append(
            [
                modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["final_kills"],
                row["final_deaths"],
                u.get_ratio(row["final_kills"], row["final_deaths"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["beds_broken"],
            ]
        )

    # Overalls
    overalls = {
        "Rush": {"index": 1, "rows": [1, 2, 3]},
        "Ultimate": {"index": 5, "rows": [5, 6, 7]},
        "Lucky": {"index": 9, "rows": [9, 10]},
        "Armed": {"index": 12, "rows": [12, 13]},
    }

    for overall in overalls:
        row = {}
        cols = {
            "wins": 1,
            "losses": 2,
            "final_kills": 4,
            "final_deaths": 5,
            "kills": 7,
            "deaths": 8,
            "beds_broken": 10,
        }

        for col in cols:
            value = 0
            for mode in overalls[overall]["rows"]:
                value += rows[mode][cols[col]]
            row[col] = value

        rows.insert(
            overalls[overall]["index"],
            [
                f"{overall} Overall",
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["final_kills"],
                row["final_deaths"],
                u.get_ratio(row["final_kills"], row["final_deaths"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["beds_broken"],
            ],
        )

    stats["table_dream"] = {
        "id": "tableDreamBedWars",
        "head": head,
        "rows": rows,
        "green": {3: 10, 6: 30},
        "boldRows": [2, 6, 10, 13],
        "percent": [3],
        "decimal": [6, 9],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "FK/D": [0, 4, 5, 6],
            "K/D": [0, 7, 8, 9],
            "Beds": [0, 10],
        },
    }

    # ==================================================================================
    # PRACTICE MODE
    # ==================================================================================

    practice_modes = ["bridging", "mlg", "fireball_jumping", "pearl_clutching", "bow"]
    practice_stats = ["blocks_placed", "successful_attempts", "failed_attempts"]

    practice = bedwars.get("practice", {})

    for mode in practice_modes:
        mode_dict = practice.get(mode, {})
        for stat in practice_stats:
            stats[f"{stat}_{mode}"] = mode_dict.get(stat, 0)
        stats[f"success_rate_{mode}"] = (
            str(
                u.get_percentage(
                    mode_dict.get("successful_attempts", 0),
                    mode_dict.get("successful_attempts", 0)
                    + mode_dict.get("failed_attempts", 0),
                )
            )
            + "%"
        )

    bridging_records = [
        ["straight_30", "bridging_distance_30:elevation_NONE:angle_STRAIGHT:"],
        ["incline_30", "bridging_distance_30:elevation_SLIGHT:angle_STRAIGHT:"],
        ["stairs_30", "bridging_distance_30:elevation_STAIRCASE:angle_STRAIGHT:"],
        ["straight_50", "bridging_distance_50:elevation_NONE:angle_STRAIGHT:"],
        ["incline_50", "bridging_distance_50:elevation_SLIGHT:angle_STRAIGHT:"],
        ["stairs_50", "bridging_distance_50:elevation_STAIRCASE:angle_STRAIGHT:"],
        ["straight_100", "bridging_distance_100:elevation_NONE:angle_STRAIGHT:"],
        ["incline_100", "bridging_distance_100:elevation_SLIGHT:angle_STRAIGHT:"],
        ["stairs_100", "bridging_distance_100:elevation_STAIRCASE:angle_STRAIGHT:"],
    ]

    practice_records = practice.get("records", {})
    for record in bridging_records:
        time = practice_records.get(record[1], "N/A")
        if time != "N/A":
            time = "{:.3f}s".format(time / 1000)
        stats[record[0]] = time

    return stats
