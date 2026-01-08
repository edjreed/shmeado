from .. import utilities as u, levelling as l
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate all SkyWars stats from a player API."""
    stats = {}

    # If player has not played SkyWars, prepare empty dict
    try:
        skywars = player_api["player"]["stats"].get("SkyWars", {})
    except LookupError:
        skywars = {}

    constants = get_constants("stats")["skywars"]

    # ==================================================================================
    # GENERAL
    # ==================================================================================

    # Selected prestige styles
    for active in ["emblem", "scheme"]:
        stats[f"active_{active}"] = skywars.get(f"active_{active}", "default")

    stats_needed = [
        # Main
        "wins",
        "losses",
        "kills",
        "deaths",
        "skywars_experience",
        "heads",
        "angel_of_death_level",
        "time_played",
        # More
        "coins",
        "cosmetic_tokens",
        "blocks_broken",
        "blocks_placed",
        "souls",
        "souls_gathered",
        "soul_well",
        "soul_well_rares",
        "soul_well_legendaries",
        "paid_souls",
        "arrows_shot",
        "arrows_hit",
        "enderpearls_thrown",
        "items_enchanted",
        "egg_thrown",
        "chests_opened",
        "assists",
        "survived_players",
        "angels_offering",
        "melee_kills",
        "void_kills",
        "mob_kills",
        "bow_kills",
        "bow_kills",
    ]

    # Collect all initial stats
    for stat in stats_needed:
        stats[stat] = skywars.get(stat, 0)

    stats["angel_of_death_level_raw"] = stats["angel_of_death_level"]

    stats["favor_of_the_angel"] = "false"
    if "favor_of_the_angel" in skywars.get("packages", []):
        stats["favor_of_the_angel"] = "true"
        stats["angel_of_death_level"] += 1

    stats["angels_offering"] = "false"
    if skywars.get("angels_offering", 0) == 1:
        stats["angels_offering"] = "true"
        stats["angel_of_death_level"] += 1

    stats["games_played"] = stats["wins"] + stats["losses"]
    stats["arrows_missed"] = stats["arrows_shot"] - stats["arrows_hit"]

    # Calculate ratios
    stats = u.get_ratios(
        stats,
        {
            "win_loss": ["wins", "losses"],
            "kill_death": ["kills", "deaths"],
            "kill_win": ["kills", "wins"],
            "kill_game": ["kills", "games_played"],
            "arrow_hit_miss": ["arrows_hit", "arrows_missed"],
        },
    )

    # Levelling and prestige
    stats["level"] = float(l.skywars_xp_to_level(stats["skywars_experience"]))
    stats["prestige_formatted"] = l.skywars_format_prestige(
        stats["level"], stats["active_emblem"], stats["active_scheme"]
    )
    stats["level_old"] = float(l.skywars_xp_to_level_old(stats["skywars_experience"]))

    # ==================================================================================
    # PRESTIGE
    # ==================================================================================

    level = stats["level"]
    prestiges = get_constants("stats")["skywars"]["prestiges"]

    prev_pres = str(l.skywars_prev_prestige(int(level)))
    next_pres = str(l.skywars_next_prestige(int(level)))

    prev_pres_info = prestiges[prev_pres]
    next_pres_info = prestiges[next_pres]

    needed = next_pres_info["endXP"] - next_pres_info["startXP"] + 1
    progress = round(stats["skywars_experience"] - prev_pres_info["startXP"])
    remaining = needed - progress

    stats["prestige"] = {
        "previous": {
            "level": prev_pres,
            "name": prev_pres_info["name"],
            "color": prestiges[prev_pres]["currentColor"],
            "formatted": l.skywars_format_prestige(
                int(prev_pres), stats["active_emblem"]
            ),
        },
        "next": {
            "level": next_pres,
            "name": next_pres_info["name"],
            "color": next_pres_info["currentColor"],
            "formatted": l.skywars_format_prestige(
                int(next_pres), stats["active_emblem"]
            ),
        },
        "progress": {
            "current": {"color": prev_pres_info["currentColor"], "progress": progress},
            "next": {"color": next_pres_info["currentColor"], "needed": needed},
        },
        "remaining": remaining,
        "percent": u.get_percentage(progress, needed),
    }

    # Calculate estimated stats at next prestige
    proceed = True  # Flag to prevent zero division error
    relevant = ["wins", "kills"]
    for stat in relevant:
        if stats[stat] == 0:
            proceed = False

    if proceed:
        xp_win = 11 if stats["favor_of_the_angel"] == "true" else 10
        kill_win = stats["kills"] / stats["wins"]
        wins_estimated = remaining / (xp_win + kill_win)

    stats["prestige"]["wins_estimated"] = int(wins_estimated) if proceed else "Unknown"
    stats["prestige"]["kills_estimated"] = (
        int(wins_estimated * kill_win) if proceed else "Unknown"
    )

    for stat in relevant:
        if proceed:
            value = stats[stat] + stats["prestige"][f"{stat}_estimated"]
        else:
            value = "Unknown"
        stats["prestige"][f"{stat}_at"] = value

    # ==================================================================================
    # TABLE
    # ==================================================================================

    head = ["Mode", "Wins", "Losses", "W/L", "Kills", "Deaths", "K/D"]
    modes = {
        "": "Overall",
        "_mini": "Mini",
        "_solo": "Solo Overall",
        "_solo_normal": "Solo Normal",
        "_solo_insane": "Solo Insane",
        "_team": "Team Overall",
        "_team_normal": "Team Normal",
        "_team_insane": "Team Insane",
    }

    rows = []
    for mode in modes:
        row = {}
        for col in ["wins", "losses", "kills", "deaths"]:
            row[col] = skywars.get(f"{col}{mode}", 0)

        if mode == "_mini":
            games = skywars.get("games_mini", 0)
            losses = games - row["wins"]
            row["losses"] = losses
            row["deaths"] = losses

        rows.append(
            [
                modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
            ]
        )

    stats["table"] = {
        "id": "tableSkyWars",
        "head": head,
        "rows": rows,
        "green": {3: 1, 6: 5},
        "boldRows": [1, 3, 6],
        "percent": [3],
        "decimal": [6],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
        },
    }

    # ==================================================================================
    # GRIM REAPER
    # ==================================================================================

    # Angel's Descent
    angels_descent_stats = ["shard_seeker", "grand_slam", "opals", "souls"]
    for stat in angels_descent_stats:
        stats[stat] = skywars.get(stat, 0)

    stats["harvesting_season"] = skywars.get("harvesting_season", -1) + 1
    stats["xezbeth_luck"] = skywars.get("xezbeth_luck", -1) + 1

    stats["opal_progress"] = {
        "current": {"progress": stats["souls"]},
        "next": {"needed": 1500},
    }

    angels_descent_info = constants["descentInfo"]

    opals_spent = 0
    opals_to_spend = 0
    for item in angels_descent_info:
        value = 0
        item_type = angels_descent_info[item]["type"]
        if item_type == "stat":
            value = skywars.get(item, 0)
        if item_type == "package":
            if item in skywars.get("packages", {}):
                value = 1
            else:
                value = 0
        if item_type == "vanity":
            try:
                if item in player_api["player"]["vanityMeta"]["packages"]:
                    value = 1
                else:
                    value = 0
            except LookupError:
                value = 0
        angels_descent_info[item]["value"] = value
        opals_spent += angels_descent_info[item]["cost"] * value
        opals_to_spend += (
            angels_descent_info[item]["cost"] * angels_descent_info[item]["tiers"]
        )

    stats["angels_descent_info"] = angels_descent_info
    stats["opals_spent"] = opals_spent
    stats["opals_to_spend"] = opals_to_spend

    # Heads
    heads = constants["heads"]
    head_stats = {}
    heads_xp = 0

    for color in heads:
        for head in color["heads"]:
            heads = skywars.get(f"heads_{head['name']}", 0)
            head_stats[head["name"]] = heads
            heads_xp += heads * head["xp"]

    head_stats["total_xp"] = heads_xp
    stats["head_stats"] = head_stats

    # Angel's Brewery
    stats["brewery_active"] = skywars.get("brewery_active", "none")
    stats["brewery"] = skywars.get("brewery", {})

    # ==================================================================================
    # PLAYTIME
    # ==================================================================================

    head = ["Mode", "Wins", "Wins/Hour", "Kills", "Kills/Hour", "Playtime"]
    modes = {
        "": "Overall",
        "_lab": "Lab",
        "_solo": "Solo",
        "_team": "Team",
        "_ranked": "Ranked",
        "_mega": "Mega Normal",
        "_mega_doubles": "Mega Doubles",
    }

    rows = []
    for mode in modes:
        row = {}
        for col in ["wins", "kills", "time_played"]:
            row[col] = skywars.get(f"{col}{mode}", 0)

        rows.append(
            [
                modes[mode],
                row["wins"],
                u.get_ratio(row["wins"], row["time_played"] / 3600),
                row["kills"],
                u.get_ratio(row["kills"], row["time_played"] / 3600),
                row["time_played"],
            ]
        )

    stats["table_playtime"] = {
        "id": "tablePlaytimeSkyWars",
        "head": head,
        "rows": rows,
        "boldRows": [1],
        "boldCols": [0, 5],
        "duration": [5],
        "decimal": [2, 4],
        "buttons": {
            "Playtime": [0, 5],
            "W/H": [0, 1, 2],
            "K/H": [0, 3, 4],
        },
    }

    # ==================================================================================
    # KITS
    # ==================================================================================

    kit_names = constants["kitNames"]
    for kit_type in kit_names:
        head = [
            "Kit",
            "Wins",
            "Losses",
            "W/L",
            "Kills",
            "Deaths",
            "K/D",
            "Playtime",
            "XP",
        ]
        modes = kit_names[kit_type]

        rows = []
        for mode in modes:
            row = {}
            for col in ["wins", "losses", "kills", "deaths", "time_played", "xp"]:
                row[col] = skywars.get(f"{col}_{mode}", 0)

            rows.append(
                [
                    modes[mode],
                    row["wins"],
                    row["losses"],
                    u.get_ratio(row["wins"], row["losses"]),
                    row["kills"],
                    row["deaths"],
                    u.get_ratio(row["kills"], row["deaths"]),
                    row["time_played"],
                    row["xp"],
                ]
            )

            sorted_rows = sorted(rows, key=lambda x: x[8], reverse=True)

        stats[f"table_kits_{kit_type}"] = {
            "id": f"tableKits{kit_type.title()}SkyWars",
            "head": head,
            "rows": sorted_rows,
            "boldCols": [0, 3, 6, 8],
            "percent": [3],
            "duration": [7],
            "decimal": [6],
            "green": {3: 1, 6: 5},
            "buttons": {
                "W/L": [0, 1, 2, 3],
                "K/D": [0, 4, 5, 6],
                "Playtime": [0, 7],
                "XP": [0, 8],
            },
        }

    # ==================================================================================
    # CARRIES
    # ==================================================================================

    head = ["Mode", "Carries", "Wins", "% of Wins"]
    modes = {
        "": "Overall",
        "_team": "Team Overall",
        "_team_normal": "Team Normal",
        "_team_insane": "Team Insane",
        "_mega": "Mega Normal",
        "_mega_doubles": "Mega Insane",
    }

    rows = []
    for mode in modes:
        row = {}
        for col in ["wins", "losses", "deaths"]:
            row[col] = skywars.get(f"{col}{mode}", 0)

        carries = abs(row["deaths"] - row["losses"])

        rows.append(
            [
                modes[mode],
                carries,
                row["wins"],
                f"{u.get_percentage(carries, row['wins'], 2)}%",
            ]
        )

    # Mega Overall
    mega_overall_carries = rows[-1][1] + rows[-2][1]
    mega_overall_wins = rows[-1][2] + rows[-2][2]
    mega_overall_percent = u.get_percentage(mega_overall_carries, mega_overall_wins, 2)
    rows.insert(
        4,
        [
            "Mega Overall",
            mega_overall_carries,
            mega_overall_wins,
            f"{mega_overall_percent}%",
        ],
    )

    stats["table_carries"] = {
        "id": "tableCarriesSkyWars",
        "head": head,
        "rows": rows,
        "boldRows": [1, 2, 5],
        "width": 520,
    }

    stats["carries"] = rows[1][1] + rows[4][1]

    # ==================================================================================
    # LEGACY
    # ==================================================================================

    # Ranked

    ranked = constants["ranked"]

    for stat in ["wins", "losses", "kills", "deaths"]:
        stats[f"{stat}_ranked"] = skywars.get(f"{stat}_ranked", 0)

    stats["win_loss_ranked"] = u.get_ratio(stats["wins_ranked"], stats["losses_ranked"])
    stats["kill_death_ranked"] = u.get_ratio(
        stats["kills_ranked"], stats["deaths_ranked"]
    )

    rewards = ranked["rewards"]
    reward_counts = {}
    for division in rewards:
        reward_counts[division] = 0
        for reward in rewards[division]:
            if reward["key"] in skywars.get("packages", {}):
                reward["has"] = 1
                reward_counts[division] += 1
            else:
                reward["has"] = 0

    stats["rewards_ranked"] = rewards
    stats["reward_counts_ranked"] = reward_counts

    def get_ranked_history_color(pos):
        if pos <= 10:
            return "darkGreen"  # Masters
        if pos <= 200:
            return "darkAqua"  # Diamond
        if pos <= 1500:
            return "gold"  # Gold
        return "gray"

    history = []

    masters_history = ranked["history"]
    for season in masters_history:
        number = season["number"]
        if number >= 24:
            break
        for position in season.get("leaderboard", {}):
            if position.get("uuid", "") == player_api["player"]["uuid"]:
                pos = position.get("position", 100000)
                history.append(
                    {
                        "season": number,
                        "rating": position.get("rating", 0),
                        "position": pos,
                        "color": get_ranked_history_color(pos),
                    }
                )

    season_numbers = ranked["seasons"]
    season_number = 24
    for season in season_numbers:
        try:
            position = skywars[f"SkyWars_skywars_rating{season}_position"] + 1
            history.append(
                {
                    "season": season_number,
                    "rating": int(skywars[f"SkyWars_skywars_rating{season}_rating"]),
                    "position": position,
                    "color": get_ranked_history_color(position),
                }
            )
        except LookupError:
            pass  # Player didn't rank this season
        season_number += 1

    stats["history_ranked"] = list(reversed(history))  # Order as descending
    stats["best_season_ranked"] = (
        min(history, key=lambda x: x["position"]) if len(history) != 0 else 0
    )

    # Mega

    head = ["Mode", "Wins", "Losses", "W/L", "Kills", "Deaths", "K/D"]
    cols = ["wins", "losses", "kills", "deaths"]
    modes = {"_mega": "Mega Normal", "_mega_doubles": "Mega Doubles"}

    for col in cols:
        stats[f"{col}_mega_overall"] = 0

    rows = []
    for mode in modes:
        row = {}
        for col in cols:
            value = skywars.get(f"{col}{mode}", 0)
            row[col] = value
            stats[f"{col}_mega_overall"] += value

        rows.append(
            [
                modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
            ]
        )

    rows.insert(
        0,
        [
            "Mega Overall",
            stats["wins_mega_overall"],
            stats["losses_mega_overall"],
            u.get_ratio(stats["wins_mega_overall"], stats["losses_mega_overall"]),
            stats["kills_mega_overall"],
            stats["deaths_mega_overall"],
            u.get_ratio(stats["kills_mega_overall"], stats["deaths_mega_overall"]),
        ],
    )

    stats["table_mega"] = {
        "id": "tableMegaSkyWars",
        "head": head,
        "rows": rows,
        "green": {3: 1, 6: 5},
        "boldRows": [1],
        "percent": [3],
        "decimal": [6],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "K/D": [0, 4, 5, 6],
        },
    }

    # Lab

    stats["assists_lab"] = skywars.get("assists_lab", 0)

    sub_modes = ["rush", "tnt_madness", "slime", "lucky_blocks", "hunters_vs_beasts"]
    for sub_mode in sub_modes:
        stats[f"wins_{sub_mode}_lab"] = skywars.get(f"lab_win_{sub_mode}_lab", 0)

    head = ["Mode", "Wins", "Losses", "W/L", "Kills", "Deaths", "K/D", "Playtime"]
    modes = {"": "Overall", "_solo": "Solo", "_team": "Team"}
    rows = []
    for mode in modes:
        row = {}
        for col in ["wins", "losses", "kills", "deaths", "time_played"]:
            row[col] = skywars.get(f"{col}_lab{mode}", 0)

        rows.append(
            [
                modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["kills"],
                row["deaths"],
                u.get_ratio(row["kills"], row["deaths"]),
                row["time_played"],
            ]
        )

    stats["table_lab"] = {
        "id": "tableLabSkyWars",
        "head": head,
        "rows": rows,
        "green": {3: 1, 6: 5},
        "boldRows": [1],
        "percent": [3],
        "duration": [7],
        "decimal": [6],
        "buttons": {"W/L": [0, 1, 2, 3], "K/D": [0, 4, 5, 6], "Playtime": [0, 7]},
    }

    return stats
