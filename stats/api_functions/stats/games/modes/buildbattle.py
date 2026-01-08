from ... import utilities as u
from stats.constants import get_constants


def get_stats(player_api):
    """Extract and calculate build battle stats from a player API."""
    stats = {}

    # If player has not played build battle, prepare empty dict
    try:
        buildbattle = player_api["player"]["stats"]["BuildBattle"]
    except LookupError:
        buildbattle = {}

    stats = {}

    stats_needed = [
        "score",
        "coins",
        "wins",
        "games_played",
        "total_votes",
        "wins_guess_the_build",
        "correct_guesses",
        "super_votes",
        "wins_solo_normal",
        "wins_teams_normal",
        "wins_solo_pro",
    ]

    for stat in stats_needed:
        stats[stat] = buildbattle.get(stat, 0)

    stats["losses"] = stats["games_played"] - stats["wins"]
    stats["win_loss"] = u.get_ratio(stats["wins"], stats["losses"])

    # Titles
    TITLES = get_constants("stats")["modes"]["buildBattle"]["titles"]

    for count, title in enumerate(TITLES):
        if stats["score"] < title["value"]:
            current = TITLES[count - 1]
            next = TITLES[count]

            stats["current_title"] = current
            stats["next_title"] = next

            if next["name"] == "N/A":  # If max title reached
                stats["title_progress"] = {
                    "text": current["name"],
                    "complete": 1,
                    "current": {"progress": current["value"]},
                    "next": {"color": current["color"], "needed": current["value"]},
                }
            else:
                stats["title_progress"] = {
                    "text": next["name"],
                    "current": {
                        "color": current["color"],
                        "progress": stats["score"] - current["value"],
                    },
                    "next": {
                        "color": next["color"],
                        "needed": next["value"] - current["value"],
                    },
                }
            break

    return stats
