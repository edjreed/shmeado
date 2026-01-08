from ... import utilities as u


def get_stats(player_api):
    """Extract and calculate all arcade stats from a player API."""
    stats = {}

    # If player has not played arcade, prepare empty dict
    try:
        arcade = player_api["player"]["stats"]["Arcade"]
    except LookupError:
        arcade = {}

    stats_needed = [
        "coins",
        # Blocking Dead
        "wins_dayone",
        "kills_dayone",
        "headshots_dayone",
        # Bounty Hunters
        "wins_oneinthequiver",
        "kills_oneinthequiver",
        "deaths_oneinthequiver",
        "bounty_kills_oneinthequiver",
        "bow_kills_oneinthequiver",
        "sword_kills_oneinthequiver",
        # Creeper Attack
        "max_wave",
        # Dragon Wars
        "wins_dragonwars2",
        "kills_dragonwars2",
        # Easter Simulator
        "wins_easter_simulator",
        "eggs_found_easter_simulator",
        # Ender Spleef
        "wins_ender",
        "blocks_destroyed_ender",
        "powerup_activations_ender",
        "bigshot_powerup_activations_ender",
        "tripleshot_powerup_activations_ender",
        # Farm Hunt
        "wins_farm_hunt",
        "poop_collected",
        "taunts_used_farm_hunt",
        "risky_taunts_used_farm_hunt",
        # Football
        "wins_soccer",
        "goals_soccer",
        "kicks_soccer",
        "powerkicks_soccer",
        # Galaxy Wars
        "sw_game_wins",
        "sw_kills",
        "sw_deaths",
        "sw_rebel_kills",
        "sw_empire_kills",
        "sw_shots_fired",
        # Grinch Simulator v2
        "wins_grinch_simulator_v2",
        "gifts_grinch_simulator_v2",
        # Halloween Simulator
        "wins_halloween_simulator",
        "candy_found_halloween_simulator",
        # Hide and Seek
        "seeker_wins_hide_and_seek",
        "hider_wins_hide_and_seek",
        # Hole in the Wall
        "wins_hole_in_the_wall",
        "rounds_hole_in_the_wall",
        "hitw_record_q",
        "hitw_record_f",
        # Hypixel Says
        "wins_simon_says",
        "rounds_simon_says",
        # Party Games
        "wins_party",
        "wins_party_2",
        "wins_party_3",
        # Pixel Painters
        "wins_draw_their_thing",
        # Santa Says
        "wins_santa_says",
        "rounds_santa_says",
        # Santa Simulator
        "delivered_santa_simulator",
        "spotted_santa_simulator",
        # Scuba Simulator
        "wins_scuba_simulator",
        "items_found_scuba_simulator",
        "total_points_scuba_simulator",
        # Throw Out
        "wins_throw_out",
        "kills_throw_out",
        "deaths_throw_out",
        # Mini Walls
        "wins_mini_walls",
        "kills_mini_walls",
        "deaths_mini_walls",
        "final_kills_mini_walls",
        "wither_kills_mini_walls",
        "wither_damage_mini_walls",
        "arrows_shot_mini_walls",
        "arrows_hit_mini_walls",
        # Zombies
        "wins_zombies",
        "deaths_zombies",
        "total_rounds_survived_zombies",
        "best_round_zombies",
        "zombie_kills_zombies",
        "bullets_shot_zombies",
        "bullets_hit_zombies",
        "headshots_zombies",
        "players_revived_zombies",
        "times_knocked_down_zombies",
        "doors_opened_zombies",
        "windows_repaired_zombies",
    ]

    for stat in stats_needed:
        stats[stat] = arcade.get(stat, 0)

    # Blocking Dead
    stats["melee_weapon"] = arcade.get("melee_weapon", "None").replace("_", " ").title()

    # Bounty Hunters
    stats["kill_death_oneinthequiver"] = u.get_ratio(
        stats["kills_oneinthequiver"], stats["deaths_oneinthequiver"]
    )

    # Capture the Wool
    stats["ctw_kills"] = (
        player_api["player"].get("achievements", {}).get("arcade_ctw_slayer", 0)
    )
    stats["ctw_captures"] = (
        player_api["player"].get("achievements", {}).get("arcade_ctw_oh_sheep", 0)
    )

    # Dropper
    dropper = arcade.get("dropper", {})
    for stat in [
        "wins",
        "games_played",
        "maps_completed",
        "fastest_game",
        "games_finished",
        "flawless_games",
        "fails",
    ]:
        stats[f"{stat}_dropper"] = dropper.get(stat, 0)
    stats["losses_dropper"] = stats["games_played_dropper"] - stats["wins_dropper"]
    stats["win_loss_dropper"] = u.get_ratio(
        stats["wins_dropper"], stats["losses_dropper"]
    )
    stats["fastest_game_dropper"] = stats["fastest_game_dropper"] / 1000

    # Galaxy Wars
    stats["sw_kill_death"] = u.get_ratio(stats["sw_kills"], stats["sw_deaths"])

    # Party Games
    stats["wins_party_games"] = (
        stats["wins_party"] + stats["wins_party_2"] + stats["wins_party_3"]
    )

    # Pixel Party
    pixel_party = arcade.get("pixel_party", {})
    pixel_party_stats = [
        "games_played",
        "wins",
        "power_ups_collected",
        "highest_round",
        "rounds_completed",
    ]
    for stat in pixel_party_stats:
        stats[f"{stat}_pixel_party"] = pixel_party.get(stat, 0)

    stats["losses_pixel_party"] = (
        stats["games_played_pixel_party"] - stats["wins_pixel_party"]
    )
    stats["win_loss_pixel_party"] = u.get_ratio(
        stats["wins_pixel_party"], stats["losses_pixel_party"]
    )

    # Pixel Party Table
    pixel_party_head = ["Mode", "Wins", "Losses", "W/L", "Powerups", "Rounds"]
    pixel_party_modes = {
        "": "Overall",
        "_normal": "Normal",
        "_hyper": "Hyper",
    }

    pixel_party_rows = []
    for mode in pixel_party_modes:
        row = {}
        for col in pixel_party_stats:
            row[col] = pixel_party.get(col + mode, 0)

        row["losses"] = row["games_played"] - row["wins"]

        pixel_party_rows.append(
            [
                pixel_party_modes[mode],
                row["wins"],
                row["losses"],
                u.get_ratio(row["wins"], row["losses"]),
                row["power_ups_collected"],
                row["rounds_completed"],
            ]
        )

    stats["table_pixel_party"] = {
        "id": "tablePixelPartyArcade",
        "head": pixel_party_head,
        "rows": pixel_party_rows,
        "boldRows": [1],
        "percent": [3],
        "buttons": {
            "W/L": [0, 1, 2, 3],
            "Powerups": [0, 4],
            "Rounds": [0, 5],
        },
    }

    # Throw Out
    stats["kill_death_throw_out"] = u.get_ratio(
        stats["kills_throw_out"], stats["deaths_throw_out"]
    )

    # Mini Walls
    stats["miniwalls_activeKit"] = arcade.get("miniwalls_activeKit", "None")
    stats["kill_death_mini_walls"] = u.get_ratio(
        stats["kills_mini_walls"], stats["deaths_mini_walls"]
    )
    stats["arrow_hit_miss_mini_walls"] = u.get_ratio(
        stats["arrows_hit_mini_walls"],
        stats["arrows_shot_mini_walls"] - stats["arrows_hit_mini_walls"],
    )

    # Zombies
    stats["bullet_accuracy_zombies"] = u.get_percentage(
        stats["bullets_hit_zombies"], stats["bullets_shot_zombies"]
    )
    stats["headshot_accuracy_zombies"] = u.get_percentage(
        stats["headshots_zombies"], stats["bullets_shot_zombies"]
    )

    # Zombies Table
    zombies_stats = [
        "best_round",
        "wins",
        "deaths",
        "zombie_kills",
        "players_revived",
        "times_knocked_down",
        "doors_opened",
        "windows_repaired",
    ]
    zombies_head = [
        "Map",
        "Best Round",
        "Wins",
        "Deaths",
        "Zombie Kills",
        "Revivals",
        "Downs",
        "Doors",
        "Windows",
    ]
    zombies_maps = {
        "deadend": "<span class='gold'>Deadend</span>",
        "badblood": "<span class='red'>Badblood</span>",
        "alienarcadium": "<span class='darkGreen'>Alienarcadium</span>",
    }

    zombies_rows = []
    for map in zombies_maps:
        row = {}
        for col in zombies_stats:
            row[col] = arcade.get(f"{col}_zombies_{map}", 0)

        zombies_rows.append(
            [
                zombies_maps[map],
                row["best_round"],
                row["wins"],
                row["deaths"],
                row["zombie_kills"],
                row["players_revived"],
                row["times_knocked_down"],
                row["doors_opened"],
                row["windows_repaired"],
            ]
        )

    stats["table_zombies"] = {
        "id": "tableZombiesArcade",
        "head": zombies_head,
        "rows": zombies_rows,
        "boldCols": [0],
        "buttons": {
            "Core": [0, 1, 2, 3],
            "Kills": [0, 4],
            "Revivals/Downs": [0, 5, 6],
            "Doors/Windows": [0, 7, 8],
        },
    }

    # Zombies Types Table
    zombies_types_stats = [
        "basic",
        "blaze",
        "blob",
        "broodmother",
        "cave_spider",
        "charged_creeper",
        "chgluglu",
        "clown",
        "empowered",
        "ender",
        "endermite",
        "family_daughter",
        "fire",
        "ghast",
        "giant",
        "guardian",
        "herobrine_minion",
        "inferno",
        "invisible",
        "iron_golem",
        "magma",
        "magma_cube",
        "mega_magma",
        "mega_blob",
        "pig_zombie",
        "rainbow",
        "sentinel",
        "skelefish",
        "skeleton",
        "slime",
        "slime_zombie",
        "space_blaster",
        "space_grunt",
        "tnt",
        "tnt_baby",
        "werewolf",
        "witch",
        "wither",
        "wither_skeleton",
        "wither_zombie",
        "wolf",
        "wolf_pet",
        "worm",
        "worm_small",
    ]
    zombies_types_head = ["Zombie Type", "Kills", "% of Kills"]
    zombies_types_rows = []

    zombies_formatting = {"tnt": "TNT", "tnt_baby": "TNT Baby"}

    for zombie in zombies_types_stats:
        zombies = arcade.get(f"{zombie}_zombie_kills_zombies", 0)
        zombies_types_rows.append(
            [
                zombies_formatting.get(zombie, zombie.replace("_", " ").title()),
                zombies,
                f"{u.get_percentage(zombies, stats['zombie_kills_zombies'])}%",
            ]
        )

    stats["table_zombies_types"] = {
        "id": "tableZombiesTypesArcade",
        "head": zombies_types_head,
        "rows": zombies_types_rows,
        "boldCols": [0],
    }

    return stats
