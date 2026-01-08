import math
from .. import utilities as u, levelling as l
from stats.api_functions.main.rank import get_rank


def get_stats(player_api):
    """Extract and calculate all general stats from a player API."""
    player = player_api["player"]
    stats = {}

    # ==================================================================================
    # MAIN
    # ==================================================================================

    # General
    stats_needed = [
        "karma",
        "firstLogin",
        "lastLogin",
        "totalDailyRewards",
        "rewardStreak",
        "rewardHighScore",
    ]
    for stat in stats_needed:
        stats[u.camel_to_snake(stat)] = player.get(stat, 0)

    # Network Level
    stats["network_experience"] = int(player.get("networkExp", 0))

    stats["network_level"] = l.network_xp_to_level(stats["network_experience"])

    xp = stats["network_experience"]
    level = stats["network_level"]

    # Next network level
    current_level_xp = l.network_level_to_xp(math.floor(level))

    stats["next_level_progress"] = {
        "text": f"Level {'{:,}'.format(math.floor(level))} to {'{:,}'.format(math.floor(level) + 1)}",
        "current": {"progress": int(xp - current_level_xp)},
        "next": {
            "needed": int(l.network_level_to_xp(math.ceil(level)) - current_level_xp)
        },
    }

    # Next network level milestone
    if xp < 79680000:  # Experience needed for level 250
        prev = 0
        next = 250
    else:  # Calculate experience needed for next 100 level milestone
        prev = math.floor(level / 100) * 100 if level >= 300 else 250
        next = math.ceil(level / 100) * 100

    prev_milestone_xp = l.network_level_to_xp(prev)

    stats["next_milestone_progress"] = {
        "text": f"Level {'{:,}'.format(prev)} to {'{:,}'.format(next)}",
        "current": {"progress": int(xp - prev_milestone_xp)},
        "next": {"needed": int(l.network_level_to_xp(next) - prev_milestone_xp)},
    }

    # Coin Multiplier
    player_rank = get_rank(player_api)
    multipliers = {
        0: 1,
        5: 1.5,
        10: 2,
        15: 2.5,
        20: 3,
        25: 3.5,
        30: 4,
        40: 4.5,
        50: 5,
        100: 5.5,
        125: 6,
        150: 6.5,
        200: 7,
        250: 8,
    }

    if stats["network_level"] >= 250:
        multiplier = "8x"
    elif player_rank == "YOUTUBER":
        multiplier = "7x (YT)"
    else:
        multiplier = "1x"  # Default multiplier
        for req, value in multipliers.items():
            if level > req:
                multiplier = f"{value}x"

    stats["coin_multiplier"] = multiplier

    # Votes
    stats["total_votes"] = player.get("voting", {}).get("total", 0)

    # Gifts
    gift_stats = player.get("giftingMeta", {})
    gift_stats_needed = ["bundlesGiven", "bundlesReceived", "ranksGiven"]

    for stat in gift_stats_needed:
        stats[u.camel_to_snake(stat)] = gift_stats.get(stat, 0)

    # ==================================================================================
    # QUESTS ========================================================================================#
    # ==================================================================================

    stats["quests"] = {"completed": 0, "completions": {}}

    quests_object = player.get("quests", {})

    # Determine individual and overall completions
    for quest in quests_object:
        completions = len(quests_object[quest].get("completions", []))
        stats["quests"]["completions"][quest] = completions
        stats["quests"]["completed"] += completions

    # ==================================================================================
    # ACHIEVEMENTS
    # ==================================================================================

    stats["achievements"] = {
        "points": player.get("achievementPoints", 0),
        "achievements": player.get("achievements", {}),
        "achievements_one_time": player.get("achievementsOneTime", []),
    }

    # ==================================================================================
    # CHALLENGES
    # ==================================================================================

    stats["challenges"] = {
        "completed": stats["achievements"]["achievements"].get("general_challenger", 0),
        "completions": {},
    }

    challenges_object = player.get("challenges", {}).get("all_time", {})

    # Determine individual completions
    for challenge in challenges_object:
        stats["challenges"]["completions"][challenge] = challenges_object[challenge]

    # ==================================================================================
    # PARKOUR
    # ==================================================================================

    parkour_times = player.get("parkourCompletions", {})
    # Sort by descending start time
    stats["parkour_times"] = dict(
        sorted(
            parkour_times.items(),
            key=lambda item: item[1][0]["timeStart"],
            reverse=True,
        )
    )

    stats["parkour_checkpoints"] = player.get("parkourCheckpointBests", {})

    # ==================================================================================
    # PETS
    # ==================================================================================

    stats["pet_items"] = player.get("petConsumables", {})
    stats["pet_items"]["total"] = sum(stats["pet_items"].values())

    stats["pets"] = player.get("petStats", {})
    for info in stats["pets"].values():
        info["level"] = l.pet_xp_to_level(info.get("experience", 0))

    # ==================================================================================
    # HISTORY
    # ==================================================================================

    rank_history = ["VIP", "VIP_PLUS", "MVP", "MVP_PLUS"]

    stats["rank_history"] = {}

    for r in rank_history:
        stats["rank_history"][r] = player.get(f"levelUp_{r}", "Unknown")

    # ==================================================================================
    # SOCIALS
    # ==================================================================================

    stats["social_media"] = player.get("socialMedia", {}).get("links", {})

    return stats
