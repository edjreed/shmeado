from .games import general, bedwars, skywars, duels
from .games.modes import (
    arcade,
    bsg,
    buildbattle,
    cvc,
    megawalls,
    murdermystery,
    pit,
    smash,
    speeduhc,
    tnt,
    uhc,
    warlords,
    wool,
)
from .games.modes.classic import arena, paintball, quakecraft, tkr, vampirez, walls
from .games.modes.legacy import crazywalls, skyclash


def get_stats(player_api):
    """Trigger stats extraction for all modes from a player API."""
    return {
        "general": general.get_stats(player_api),
        "bedwars": bedwars.get_stats(player_api),
        "skywars": skywars.get_stats(player_api),
        "duels": duels.get_stats(player_api),
        "modes": {
            "arcade": arcade.get_stats(player_api),
            "bsg": bsg.get_stats(player_api),
            "build_battle": buildbattle.get_stats(player_api),
            "cvc": cvc.get_stats(player_api),
            "megawalls": megawalls.get_stats(player_api),
            "murdermystery": murdermystery.get_stats(player_api),
            "pit": pit.get_stats(player_api),
            "smash": smash.get_stats(player_api),
            "speeduhc": speeduhc.get_stats(player_api),
            "tnt": tnt.get_stats(player_api),
            "uhc": uhc.get_stats(player_api),
            "warlords": warlords.get_stats(player_api),
            "wool": wool.get_stats(player_api),
            "classic": {
                "arena": arena.get_stats(player_api),
                "paintball": paintball.get_stats(player_api),
                "quakecraft": quakecraft.get_stats(player_api),
                "tkr": tkr.get_stats(player_api),
                "vampirez": vampirez.get_stats(player_api),
                "walls": walls.get_stats(player_api),
            },
            "legacy": {
                "crazywalls": crazywalls.get_stats(player_api),
                "skyclash": skyclash.get_stats(player_api),
            },
        },
    }
