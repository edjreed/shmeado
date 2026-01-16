import os
import json
import time
import urllib.request
from ratelimit import limits


# ======================================================================================
# API STATUS
# ======================================================================================

api_status = {
    "status": 4,  # Default to unknown
    "time": None,
}


def timed_api_response(url):
    """Update api_status based on request response time.

    Calculated by measuring the difference between the start and end
    times of a request. Updates api_status to a dictionary of the form:
    {
        "status": <integer representing numerical status code>,
        "time": <float representing the response time in seconds>
    }

    Status codes (where t is the response time in seconds):
        0: 0 < t <= 1
        1: 1 < t <= 2.5
        2: t > 2.5
        3: Unresponsive (request failed even with a valid UUID)
        4: Unknown (no request conducted since server startup)

    Keyword argument:
        url: string containing the URL to request
    """

    # Start the timer
    start = time.perf_counter()

    # Make the request
    try:
        response = url_to_json(url)
        end = time.perf_counter()  # End the timer
        response_time = end - start  # Calculate the response time
    except urllib.request.http.client.InvalidURL:
        return None  # Invalid UUID was given
    except urllib.error.URLError:
        response_time = -1

    # Determine the status code based on the response time
    if response_time == -1:
        status_code = 3
    elif response_time <= 1:
        status_code = 0
    elif response_time <= 2.5:
        status_code = 1
    else:
        status_code = 2

    # Update the API status
    api_status["status"] = status_code
    api_status["time"] = response_time
    return response


def get_api_status():
    """Return the latest API status."""
    return api_status


# ======================================================================================
# API FUNCTIONS
# ======================================================================================

API_KEY = os.getenv("API_KEY")
RATE_LIMIT = int(os.getenv("RATE_LIMIT"))
PER_MINUTE = 60


@limits(calls=RATE_LIMIT, period=PER_MINUTE)
def get_api_key():
    """Return the API key under rate limit restrictions."""
    return API_KEY


def url_to_json(url):
    """Return the JSON response given by a URL."""
    return json.loads(urllib.request.urlopen(url).read())


def get_uuid(name):
    """Return the UUID for a player."""
    # Check if it's already a UUID
    if len(name) in [32, 36]:
        return name
    # Otherwise try to get the UUID
    try:
        return url_to_json(
            f"https://api.minecraftservices.com/users/profiles/minecraft/{name}"
        ).get("id", "Invalid Name")
    # Return as invalid if the UUID cannot be found for that name
    except (urllib.error.URLError, json.JSONDecodeError):
        return "Invalid Name"


def get_api(uuid):
    """Return a player's Hypixel stats API."""
    return timed_api_response(
        f"https://api.hypixel.net/v2/player?key={get_api_key()}&uuid={uuid}"
    )


def get_online_status(uuid):
    """Return a player's Hypixel online status API."""
    return url_to_json(
        f"https://api.hypixel.net/v2/status?key={get_api_key()}&uuid={uuid}"
    )


def get_recent_games(uuid):
    """Return a player's Hypixel recent games API."""
    return url_to_json(
        f"https://api.hypixel.net/v2/recentgames?key={get_api_key()}&uuid={uuid}"
    )


def get_guild_information(uuid):
    """Return a player's Hypixel guild information API."""
    return url_to_json(
        f"https://api.hypixel.net/v2/guild?key={get_api_key()}&player={uuid}"
    )
