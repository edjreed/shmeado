from .. import utilities as u
from stats.constants import get_constants


DIVISIONS = get_constants("stats")["duels"]["divisions"]


def get_duels_division(wins, mode=False, next=False):
    """Get the division name based on number of wins and mode type.

    Keyword arguments:
        wins: Integer representing the number of wins
        mode: Boolean to indicate whether the mode is a specific mode
              (halves win requirements) (default False)
        next: Boolean to indicate whether to inlcude the win
              requirementfor the next division (default False)

    If next is False, returns the current division as HTML.
    If next is True, returns a dictionary with the next division as
    HTML and the win requirement as an integer.
    """
    d_prev = {"win_req": 0, "division": DIVISIONS["0"]}

    for win_req_str, d in DIVISIONS.items():
        win_req = int(win_req_str)
        if mode:
            win_req = int(win_req / 2)

        if wins >= d_prev["win_req"] and wins < win_req:
            if next:
                return {
                    "win_req": win_req,
                    "division": f"<b class='{d['color']}'>{d['name']} {d['value']}</b>",
                }
            else:
                d_prev_d = d_prev["division"]
                return f"<b class='{d_prev_d['color']}'>{d_prev_d['name']} {d_prev_d['value']}</b>"
        d_prev = {"win_req": win_req, "division": d}


def get_stats(player_api):
    """Extract and calculate all duels stats from a player API."""
    stats = {}

    # If player has not played duels, prepare empty dict
    try:
        duels = player_api["player"]["stats"].get("Duels", {})
    except LookupError:
        duels = {}

    # ==================================================================================
    # GENERAL
    # ==================================================================================

    stats_needed = [
        # Main
        "wins",
        "losses",
        "kills",
        "deaths",
        "coins",
        "duels_chests",
        # More
        "melee_swings",
        "melee_hits",
        "bow_shots",
        "bow_hits",
        "damage_dealt",
        "health_regenerated",
        "games_played_duels",
        "rounds_played",
        "blocks_placed",
        "golden_apples_eaten",
        "Duels_openedChests",
        "Duels_openedCommons",
        "Duels_openedRares",
        "Duels_openedEpics",
        "Duels_openedLegendaries",
    ]

    # Collect all initial stats
    for stat in stats_needed:
        stats[stat] = duels.get(stat, 0)

    stats["melee_misses"] = stats["melee_swings"] - stats["melee_hits"]
    stats["bow_misses"] = stats["bow_shots"] - stats["bow_hits"]
    stats["draws"] = abs(stats["losses"] - stats["deaths"])
    stats["division"] = get_duels_division(stats["wins"])

    # Calculate ratios
    stats = u.get_ratios(
        stats,
        {
            "win_loss": ["wins", "losses"],
            "kill_death": ["kills", "deaths"],
            "melee_hit_miss": ["melee_hits", "melee_misses"],
            "bow_hit_miss": ["bow_hits", "bow_misses"],
        },
    )

    # ==================================================================================
    # TABLE
    # ==================================================================================

    head = [
        "Mode",
        "Division",
        "Wins",
        "Losses",
        "W/L",
        "Kills",
        "Deaths",
        "K/D",
        "Melee H/M",
        "Arrow H/M",
    ]
    modes = {
        "Overall": {"": "Overall"},
        "UHC": {
            "uhc_duel_": "UHC 1v1",
            "uhc_doubles_": "UHC 2v2",
            "uhc_four_": "UHC 4v4",
            "uhc_meetup_": "UHC Deathmatch",
        },
        "OP": {
            "op_duel_": "OP 1v1",
            "op_doubles_": "OP 2v2",
        },
        "SkyWars": {
            "sw_duel_": "SkyWars 1v1",
            "sw_doubles_": "SkyWars 2v2",
        },
        "MegaWalls": {
            "mw_duel_": "MegaWalls 1v1",
            "mw_doubles_": "MegaWalls 2v2",
        },
        "Bow": {
            "bow_duel_": "Bow 1v1",
        },
        "Blitz": {
            "blitz_duel_": "Blitz 1v1",
        },
        "Sumo": {
            "sumo_duel_": "Sumo 1v1",
        },
        "Bowspleef": {
            "bowspleef_duel_": "Bowspleef 1v1",
        },
        "Classic": {
            "classic_duel_": "Classic 1v1",
        },
        "NoDebuff": {
            "potion_duel_": "NoDebuff 1v1",
        },
        "Combo": {
            "combo_duel_": "Combo 1v1",
        },
        "Boxing": {
            "boxing_duel_": "Boxing 1v1",
        },
        "Parkour": {
            "parkour_eight_": "Parkour",
        },
        "Duel Arena": {
            "duel_arena_": "Duel Arena",
        },
        "Tournament": {
            "uhc_tournament_": "UHC Tournament",
            "sw_tournament_": "SkyWars Tournament",
            "sumo_tournament_": "Sumo Tournament",
        },
    }

    rows = []
    for division, group in modes.items():
        # Tournaments do not have divisions
        tournament = False
        if division == "Tournament":
            tournament = True

        division_wins = 0
        for mode in group:
            division_wins += duels.get(f"{mode}wins", 0)

        for mode in group:
            row = {}
            for col in [
                "wins",
                "losses",
                "kills",
                "deaths",
                "melee_swings",
                "melee_hits",
                "bow_shots",
                "bow_hits",
            ]:
                row[col] = duels.get(f"{mode}{col}", 0)

            rows.append(
                [
                    group[mode],
                    get_duels_division(division_wins, False if mode == "" else True)
                    if not tournament
                    else "N/A",
                    row["wins"],
                    row["losses"],
                    u.get_ratio(row["wins"], row["losses"]),
                    row["kills"],
                    row["deaths"],
                    u.get_ratio(row["kills"], row["deaths"]),
                    u.get_ratio(
                        row["melee_hits"], row["melee_swings"] - row["melee_hits"]
                    ),
                    u.get_ratio(row["bow_hits"], row["bow_shots"] - row["bow_hits"]),
                ]
            )

    stats["table"] = {
        "id": "tableDuels",
        "head": head,
        "rows": rows,
        "green": {4: 10, 7: 10},
        "boldRows": [1],
        "percent": [4],
        "decimal": [7, 8, 9],
        "buttons": {
            "Division": [0, 1],
            "W/L": [0, 2, 3, 4],
            "K/D": [0, 5, 6, 7],
            "H/M": [0, 8, 9],
        },
    }

    # ==================================================================================
    # TITLES
    # ==================================================================================

    division_titles = []

    bridge_modes = {
        "bridge_duel_": "1v1",
        "bridge_doubles_": "2v2",
        "bridge_threes_": "3v3",
        "bridge_four_": "4v4",
        "bridge_2v2v2v2_": "2v2v2v2",
        "bridge_3v3v3v3_": "3v3v3v3",
        "capture_threes_": "Capture 3v3",
        "bridge_tournament_": "Tournament",
    }

    modes["Bridge"] = bridge_modes

    for division, group in modes.items():
        # Tournaments do not have divisions
        if division == "Tournament":
            continue

        status = {"mode": division}

        division_wins = 0
        for mode in group:
            if mode == "bridge_tournament":
                continue
            else:
                division_wins += duels.get(f"{mode}wins", 0)

        status["division_current"] = get_duels_division(
            division_wins, False if mode == "" else True
        )
        status["progress_current"] = division_wins

        next_division = get_duels_division(
            division_wins, False if mode == "" else True, True
        )
        status["division_next"] = next_division["division"]
        status["progress_next"] = next_division["win_req"]
        status["wins_needed"] = next_division["win_req"] - division_wins + 1

        division_titles.append(status)

    stats["division_titles"] = division_titles

    stats["custom_titles"] = duels.get("custom_titles", [])
    stats["current_custom_title"] = duels.get("equipped_custom_titles", "None")

    # ==================================================================================
    # BRIDGE
    # ==================================================================================

    head = [
        "Mode",
        "Wins",
        "Losses",
        "W/L",
        "Kills",
        "Deaths",
        "K/D",
        "Melee H/M",
        "Arrow H/M",
        "Goals",
    ]
    cols = [
        "wins",
        "losses",
        "kills",
        "deaths",
        "melee_swings",
        "melee_hits",
        "bow_shots",
        "bow_hits",
        "rounds_played",
        "goals",
    ]
    rows = []

    # Track overall stats for overall row
    overall_row = {}
    for col in cols:
        overall_row[col] = 0

    for mode in bridge_modes:
        row = {}
        for col in cols:
            if col in ["kills", "deaths"]:
                row[col] = duels.get(f"{mode}bridge_{col}", 0)
            else:
                row[col] = duels.get(f"{mode}{col}", 0)
            if col in overall_row.keys():
                overall_row[col] += row[col]

        rows.append(
            [
                bridge_modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                u.get_ratio(row["melee_hits"], row["melee_swings"] - row["melee_hits"]),
                u.get_ratio(row["bow_hits"], row["bow_shots"] - row["bow_hits"]),
                row["goals"],
            ]
        )

    rows.insert(
        0,
        [
            "Overall",
            overall_row["wins"],
            overall_row["losses"],
            u.get_ratio(overall_row["wins"], overall_row["losses"]),
            overall_row["kills"],
            overall_row["deaths"],
            u.get_ratio(overall_row["kills"], overall_row["deaths"]),
            u.get_ratio(
                overall_row["melee_hits"],
                overall_row["melee_swings"] - overall_row["melee_hits"],
            ),
            u.get_ratio(
                overall_row["bow_hits"],
                overall_row["bow_shots"] - overall_row["bow_hits"],
            ),
            overall_row["goals"],
        ],
    )

    stats["table_bridge"] = {
        "id": "tableBridgeDuels",
        "head": head,
        "rows": rows,
        "green": {3: 10, 6: 10},
        "boldRows": [1],
        "percent": [3],
        "decimal": [6, 7, 8],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
            "H/M": [0, 7, 8],
            "Goals": [0, 9],
        },
    }

    stats["division_bridge"] = get_duels_division(overall_row["wins"], True)

    # ==================================================================================
    # CARRIES
    # ==================================================================================

    head = ["Mode", "Carries", "Wins", "% of Wins"]
    modes = {
        "uhc_doubles_": "UHC 2v2",
        "uhc_four_": "UHC 4v4",
        "op_doubles_": "OP 2v2",
        "sw_doubles_": "SkyWars 2v2",
        "mw_doubles_": "MegaWalls 2v2",
    }

    rows = []
    for mode in modes:
        row = {}
        for col in ["wins", "losses", "deaths"]:
            row[col] = duels.get(f"{mode}{col}", 0)

        carries = abs(row["deaths"] - row["losses"])

        rows.append(
            [
                modes[mode],
                carries,
                row["wins"],
                f"{u.get_percentage(carries, row['wins'], 2)}%",
            ]
        )

    stats["table_carries"] = {
        "id": "tableCarriesDuels",
        "head": head,
        "rows": rows,
        "boldRows": [1],
        "width": 520,
    }

    total_carries = 0
    for row in rows:
        total_carries += row[1]

    rows.insert(
        0,
        [
            "Overall",
            total_carries,
            stats["wins"],
            f"{u.get_percentage(total_carries, stats['wins'])}%",
        ],
    )

    stats["carries"] = total_carries

    return stats
