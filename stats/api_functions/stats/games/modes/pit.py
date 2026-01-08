from ... import utilities as u
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate all pit stats from a player API."""
    stats = {}

    # If player has not played pit, prepare empty dict
    try:
        pit = player_api["player"]["stats"]["Pit"]
    except LookupError:
        pit = {}

    # Main Stats
    pit_profile = pit.get("profile", {})

    stats["cash_during_current_prestige"] = pit_profile.get(
        "cash_during_prestige_" + str(len(pit_profile.get("prestiges", []))), 0
    )

    stats_profile = ["cash", "xp"]
    for stat in stats_profile:
        stats[stat] = pit_profile.get(stat, 0)

    stats["renown_unlocks"] = len(pit_profile.get("renown_unlocks", []))

    pit_stats = pit.get("pit_stats_ptl", {})
    stats_needed = [
        "playtime_minutes",
        "cash_earned",
        "contracts_completed",
        "king_quest_completion",
        "kills",
        "deaths",
        "assists",
        "enchanted_tier1",
        "enchanted_tier2",
        "enchanted_tier3",
        "damage_dealt",
        "damage_received",
        "max_streak",
        "melee_damage_dealt",
        "melee_damage_received",
        "left_clicks",
        "sword_hits",
        "bow_damage_dealt",
        "bow_damage_received",
        "arrows_fired",
        "arrow_hits",
        "jumped_into_pit",
        "launched_by_launchers",
        "lucky_diamond_pieces",
        "diamond_items_purchased",
        "soups_drank",
        "gapple_eaten",
        "ghead_eaten",
        "rage_potatoes_eaten",
        "blocks_broken",
        "blocks_placed",
        "fishing_rod_launched",
        "lava_bucket_emptied",
        "wheat_farmed",
        "fished_anything",
        "fishes_fished",
        "sewer_treasures_found",
    ]

    for stat in stats_needed:
        stats[stat] = pit_stats.get(stat, 0)

    hours = stats["playtime_minutes"] / 60
    stats["gold_hour"] = u.get_ratio(stats["cash_earned"], hours, 2)
    stats["xp_hour"] = u.get_ratio(stats["xp"], hours, 2)
    stats["playtime"] = (
        f"{'{:,}'.format(int(hours))}h {stats['playtime_minutes'] % 60}m"
    )

    # Progress Bars
    PIT_CONSTANTS = get_constants("stats")["modes"]["pit"]
    PIT_PRESTIGES = PIT_CONSTANTS["prestiges"]
    PIT_LEVELS = PIT_CONSTANTS["levels"]

    def get_pit_level():
        for count, prestige in enumerate(PIT_PRESTIGES):
            if stats["xp"] <= prestige["xpTotal"]:
                xp_over = stats["xp"] - (prestige["xpTotal"] - prestige["xp"])

                if xp_over == prestige["xp"]:
                    return {
                        "prestige": count,
                        "prestigeColor": prestige["color"],
                        "level": 120,
                        "levelColor": "aqua",
                    }

                level_xp_total = 0
                level_count = 0
                for level in PIT_LEVELS:
                    for i in range(1, 11):
                        level_xp_total += level["xp"] * prestige["multiplier"]
                        if level_xp_total <= xp_over:
                            level_count += 1
                        else:
                            return {
                                "prestige": count,
                                "prestigeColor": prestige["color"],
                                "level": level_count,
                                "levelColor": level["color"],
                            }

    stats["level"] = get_pit_level()

    prestige_info = PIT_PRESTIGES[stats["level"]["prestige"]]

    xp_over = stats["xp"] - (prestige_info["xpTotal"] - prestige_info["xp"])
    stats["prestige_xp_progress"] = {
        "text": "Prestige XP",
        "current": {"progress": xp_over},
        "next": {"needed": prestige_info["xp"]},
    }

    stats["prestige_gold_progress"] = {
        "text": "Prestige Gold",
        "current": {
            "color": "darkGray",
            "progress": int(stats["cash_during_current_prestige"]),
        },
        "next": {"color": "gold", "needed": prestige_info["goldReq"]},
    }

    stats["renown_progress"] = {
        "text": "Renown",
        "current": {"color": "darkPurple", "progress": stats["renown_unlocks"]},
        "next": {"color": "lightPurple", "needed": 114},
    }

    # Combat Stats
    stats["kill_death"] = u.get_ratio(stats["kills"], stats["deaths"])

    bounties = pit_profile.get("bounties", [])
    if len(bounties) == 0:
        stats["bounty"] = 0
    else:
        bounty_amount = 0
        for bounty in bounties:
            bounty_amount += bounty.get("amount", 0)
        stats["bounty"] = bounty_amount

    stats["kill_hour"] = u.get_ratio(stats["kills"], hours, 2)
    stats["kill_assist_death"] = u.get_ratio(
        stats["kills"] + stats["assists"], stats["deaths"]
    )
    stats["kill_assist_hour"] = u.get_ratio(stats["kills"] + stats["assists"], hours, 2)

    stats["damage_dealt_taken"] = u.get_ratio(
        stats["damage_dealt"], stats["damage_received"]
    )
    stats["melee_damage_dealt_taken"] = u.get_ratio(
        stats["melee_damage_dealt"], stats["melee_damage_received"]
    )
    stats["melee_accuracy"] = u.get_percentage(
        stats["sword_hits"], stats["left_clicks"]
    )

    stats["bow_damage_dealt_taken"] = u.get_ratio(
        stats["bow_damage_dealt"], stats["bow_damage_received"]
    )
    stats["bow_accuracy"] = u.get_percentage(stats["arrow_hits"], stats["arrows_fired"])

    return stats
