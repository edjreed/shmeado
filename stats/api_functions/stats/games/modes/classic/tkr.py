import re
import json
from .... import utilities as u


def get_stats(player_api):
    """Extract and calculate all TKR stats from a player API."""
    stats = {}

    # If player has not played TKR, prepare empty dict
    try:
        tkr = player_api["player"]["stats"]["GingerBread"]
    except LookupError:
        tkr = {}

    tkr_stats = [
        "wins",
        "coins",
        "grand_prix_tokens",
        "gold_trophy",
        "silver_trophy",
        "bronze_trophy",
        "banana_hits_sent",
        "banana_hits_received",
        "laps_completed",
        "blue_torpedo_hit",
        "box_pickups",
        "coins_picked_up",
        "engine_active",
        "frame_active",
        "booster_active",
    ]
    for stat in tkr_stats:
        stats[stat] = tkr.get(stat, 0)

    stats["banana_sent_received"] = u.get_ratio(
        stats["banana_hits_sent"], stats["banana_hits_received"]
    )

    # Kart parts
    stats["kart_parts"] = []

    for part in ["engine", "frame", "booster"]:
        raw_info = tkr.get(
            f"{part}_active", "{}"
        )  # This is a malformed JSON as a string provided by Hypixel API
        add_key_quotes = re.sub(r"(\w+):", r'"\1":', raw_info)  # Add quotes around keys
        add_value_quotes = re.sub(
            r":([A-Z_]+)([,\}])", r':"\1"\2', add_key_quotes
        )  # Add quotes around values
        json_info = json.loads(add_value_quotes).get(
            "GingerbreadPart", {}
        )  # Final JSON

        if json_info != {}:
            quality = -1
            for attr in json_info.get("Attributes", []):
                quality += attr["Level"]

            json_info["Quality"] = quality
        else:
            json_info["PartType"] = part

        stats["kart_parts"].append(json_info)

    return stats
