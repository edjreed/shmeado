import logging
from django.shortcuts import render
from django.http import JsonResponse

from stats.constants import get_constants

from stats.api_functions.main import api
from stats.api_functions.main.rank import get_rank

from stats.api_functions.stats import main as stats_main

from .models import Supporter

# ======================================================================================
# PAGES
# ======================================================================================

logger = logging.getLogger(__name__)


def home(request):
    """Home page."""
    context = {
        "header": "Player Stats",
        "sidebar": "stats",
        "description": "Advanced player stats tool for the Hypixel Network.",
        "constants": get_constants("home"),
        "tab": "Stats",  # Default tab
    }

    return render(request, "stats/pages/home.html", context)


def stats(request, name, game=None, tab=None):
    """Player stats page."""
    try:
        uuid = api.get_uuid(name)
        player_api = api.get_api(uuid)
        name = player_api["player"]["displayname"]

        constants = get_constants("stats")

        tabs = dict(constants["main"]["tabs"])
        games = list(tabs.keys())
        constants["main"]["games"] = games

        # Check if game and tab are valid
        game = game if game in games else None
        tab = tab if any(tab in tab_list for tab_list in tabs.values()) else None

        # Check if player is a supporter
        supporter = Supporter.objects.filter(uuid=uuid).first()

        context = {
            "header": f"{name}'s Stats",
            "sidebar": "stats",
            "description": f"{name}'s Hypixel Stats",
            "player": {
                "name": name,
                "uuid": uuid,
                "rank": get_rank(player_api),
                "stats": stats_main.get_stats(player_api),
            },
            "supporter": supporter if supporter else None,
            "constants": constants,
            "game": game if game is not None else games[0],
            "tab": tab if tab is not None else tabs[games[0]][0],
        }

        return render(request, "stats/pages/stats/main.html", context)

    except Exception as e:  # noqa: E722 - no exception type is given as site must continue to function
        logger.error(f"name: '{name}' - {e}")

        context = {
            "header": "Player Stats",
            "sidebar": "stats",
            "description": "Advanced player stats tool for the Hypixel Network.",
            "constants": get_constants("home"),
            "tab": "Stats",
            "error": name,
        }

        return render(request, "stats/pages/home.html", context)


def about(request):
    """About page."""
    context = {
        "header": "About",
        "sidebar": "about",
        "description": "About and FAQs.",
        "constants": get_constants("about"),
    }

    return render(request, "stats/pages/about.html", context)


# ======================================================================================
# INTERNAL APIS
# ======================================================================================


def online(request, uuid):
    """Online status API."""
    return JsonResponse(api.get_online_status(uuid))


def recent(request, uuid):
    """Recent games API."""
    return JsonResponse(api.get_recent_games(uuid))


def guild(request, uuid):
    """Guild information API."""
    return JsonResponse(api.get_guild_information(uuid))
