from environ import Env
from stats.api_functions.main import api


def ga_id(request):
    """Context processor to continually serve Google Analytics ID."""
    env = Env()
    Env.read_env()
    ga_id = env("GA_ID", default=None)
    return {"GA_ID": ga_id}


def api_status(request):
    """Context processor to continually serve API status info."""
    status = api.get_api_status()
    return {"api_status": status}
