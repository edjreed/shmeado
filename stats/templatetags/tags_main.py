from django.template.defaulttags import register
from django.utils.safestring import mark_safe
import re
import datetime
from stats.constants import get_constants


@register.filter
def get_item(dictionary, key):
    """Return the item from the dictionary at the given key."""
    return dictionary.get(key)


@register.filter
def get_index(array, index):
    """Return the item from the array at the given index."""
    return array[index]


@register.filter
def get_range(value):
    """Return a range object from 0 to the given value."""
    return range(value)


@register.filter
def format_timestamp(value):
    """Format a timestamp value into a human-readable string."""
    if value == 0:
        return "Unknown"
    try:
        # Return DD/MM/YY HH:MM assuming the integer represents milliseconds
        return datetime.datetime.fromtimestamp(int(value) / 1000).strftime("%d/%m/%y %H:%M")
    except (ValueError, TypeError):
        # Return N/A if the value is not an integer or cannot be converted
        return "N/A"
    

@register.filter
def time_since_timestamp(value):
    """Format the time since a timestamp into a human-readable string."""
    if value == 0:
        return "N/A"
    try:
        # Determine the difference between timestamp and current time
        event_time = datetime.datetime.fromtimestamp(int(value) / 1000)
        current_time = datetime.datetime.now()
        delta = current_time - event_time

        # Break down the difference
        seconds = delta.seconds
        
        time_units = {
            "d": delta.days,
            "h": seconds // 3600,
            "m": (seconds % 3600) // 60,
            "s": seconds % 60
        }

        # Filter out the zero values and format the non-zero time units
        time_parts = [f"{value:,}{label}" for label, value in time_units.items() if value > 0]

        # Return only the top 2 non-zero time measures
        return " ".join(time_parts[:2]) if time_parts else "0s"
    except (ValueError, TypeError):
        # Return N/A if the value is not an integer or cannot be converted
        return "N/A"


@register.filter
def format_duration(seconds, trimmed=False, noDays=False):
    """Format a duration in seconds into a human-readable string.
    
    Keyword arguments:
        trimmed: Boolean indicating whether to trim leading zero units.
        noDays: Boolean indicating whether to exclude days from the output.
    """
    days = seconds // (24 * 3600)  # Calculate days
    seconds = seconds % (24 * 3600)  # Remaining seconds after extracting days

    hours = seconds // 3600  # Calculate hours
    seconds = seconds % 3600  # Remaining seconds after extracting hours

    minutes = seconds // 60  # Calculate minutes
    seconds = seconds % 60  # Remaining seconds are the seconds

    # Format the output
    if noDays:
        hours += days * 24
        return f"{'{:,}'.format(hours)}h {minutes}m {seconds}s"
    if not trimmed:
        return f"{days}d {hours:02}h {minutes:02}m {seconds:02}s"
    else:
        string = ""
        if days > 0:
            string += f"{days}d "
        if hours > 0:
            string += f"{hours}h "
        if minutes > 0:
            string += f"{minutes}m "
        return string + f"{seconds}s"
    
    
@register.filter
def format_duration_ms(ms):
    """Format a duration in milliseconds into a human-readable string."""
    minutes = ms // 60000
    ms = ms % 60000
    
    seconds = ms // 1000
    ms = ms % 1000
    
    string = ""
    if minutes > 0:
        string += f"{minutes}m "
        
    return string + f"{seconds}.{ms:03}s"


@register.filter
def subtract(value, amount):
    """Subtract amount from value."""
    return int(value) - int(amount)


@register.filter
def multiply(value, amount):
    """Multiply value by amount."""
    return int(value) * int(amount)


@register.filter
def divide(value, amount):
    """Divide value by amount."""
    return int(int(value) / int(amount))


@register.filter
def percent(target, current):
    """Current as a percentage of target."""
    if current >= target:
        return 100
    elif current < 0:
        return 0
    else:
        return round(int(current) / int(target) * 100, 2)
    
    
@register.filter
def ratio(first, second):
    """First as a decimal of second."""
    if second == 0:
        return first
    else:
        return round(int(first) / int(second), 3)
    
    
@register.filter
def romanize(num):
    """Convert an integer to its Roman numeral representation."""
    num = int(num)
    if num == 0:
        return '0'
    
    val_map = [
        (1000, 'M'), (900, 'CM'),
        (500, 'D'),  (400, 'CD'),
        (100, 'C'),  (90, 'XC'),
        (50, 'L'),   (40, 'XL'),
        (10, 'X'),   (9, 'IX'),
        (5, 'V'),    (4, 'IV'),
        (1, 'I')
    ]

    roman = ''
    for value, numeral in val_map:
        while num >= value:
            roman += numeral
            num -= value
    return roman


@register.filter
def loop_counter(value):
    """Return a range object from 1 to the given value."""
    return range(1, int(value) + 1)


@register.filter
def round_down(value):
    """Round down the given value to the nearest integer."""
    return int(value)


@register.filter
def skywars_kit_tier(xp, tiers):
    """Determine SkyWars kit tier information based on XP and tier requirements."""
    tierInfo = {}
    
    # Change dict format to iterable tuple
    sorted_tiers = sorted(tiers.items(), key=lambda x: x[1])
    
    for t, (tier, required_xp) in enumerate(sorted_tiers):
        # Non-max prestige info
        if xp < required_xp:
            tierInfo["next_prestige"] = tier
            tierInfo["next_xp"] = required_xp
            if t > 0:
                tierInfo["current_prestige"], tierInfo["current_xp"] = sorted_tiers[t - 1]
            else:
                tierInfo["current_prestige"] = 0
                tierInfo["current_xp"] = 0
            break
        # Max prestige info
        else:
            tierInfo["current_prestige"], tierInfo["current_xp"] = sorted_tiers[-1]
            tierInfo["next_prestige"] = None
            tierInfo["next_xp"] = sorted_tiers[-1][1]
    
    return tierInfo
            

@register.filter
def untrim_uuid(uuid):
    """Convert a trimmed UUID (without dashes) back to standard UUID format."""
    return f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
    
    
@register.filter
def remove_underscores(text):
    """Replace underscores in the text with spaces."""
    return text.replace('_', ' ')


@register.filter
def escape_slash(text):
    """Escape forward slashes in the text."""
    return text.replace('/', '\\/')


def snake_to_camel(s):
    """Convert snake_case string to camelCase."""
    return re.sub(r'_([a-z])', lambda match: match.group(1).upper(),s)


@register.filter
def replace_color_tags(s):
    """Replace color tags in the string with corresponding HTML span elements."""
    constants = get_constants("stats")["main"]
    
    formatted = ""
    current_color = ""

    # Tags identified with '§'
    if "§" in s:
        color_sections = constants["colorSections"]
        i = 0
        while i < len(s):
            if s[i] == "§" and i + 1 < len(s):
                color_code = s[i:i+2]  # e.g. "§a"
                current_color = color_sections.get(color_code, current_color)
                i += 2  # Skip color code
            else:
                formatted += f"<span class='{current_color}'>{s[i]}</span>"
                i += 1
                
    # Tags identified with '%%'
    elif "%%" in s:
        # Pattern to find color markers like %%color%%
        pattern = r'%%(.*?)%%'
        parts = re.split(pattern, s)

        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Text part
                if current_color:
                    formatted += f"<span class='{snake_to_camel(current_color)}'>{part}</span>"
                else:
                    formatted += part
            else:
                # Color part
                current_color = part.strip()

    else:
        return s

    return formatted


@register.simple_tag
def rank(rankInfo, name, improveVisbility=False):
    """Format a player's rank into an HTML string with appropriate colors and tags."""
    rank_name = rankInfo["rank"]
    rank_plus_color = snake_to_camel(rankInfo["rankPlusColor"].lower())
    monthly_rank_color = snake_to_camel(rankInfo["monthlyRankColor"].lower())
    
    default_color = "gray"
    vip_color = "makeGreenVisible" if improveVisbility else "green"
    mvp_color = "makeAquaVisible" if improveVisbility else "aqua"
    
    rank_formats = {
        "None": f"<span class='{default_color}'>{name}</span>",
        "VIP": f"<span class='{vip_color}'>[VIP] {name}</span>",
        "VIP_PLUS": f"<span class='{vip_color}'>[VIP</span><span class='#FFAA00'>+</span><span class='{vip_color}'>] {name}</span>",
        "MVP": f"<span class='{mvp_color}'>[MVP] {name}</span>",
        "MVP+": f"<span class='{mvp_color}'>[MVP</span><span class='{rank_plus_color}'>+</span><span class='{mvp_color}'>] {name}</span>",
        "MVP++": f"<span class='{mvp_color if monthly_rank_color == 'AQUA' else monthly_rank_color}'>[MVP</span><span class='{rank_plus_color}'>++</span><span class='{mvp_color if monthly_rank_color == 'AQUA' else monthly_rank_color}'>] {name}</span>",
        "YOUTUBER": f"<span class='red'>[</span><span class='white'>YOUTUBE</span><span class='red'>] {name}</span>",
        "HELPER": f"<span class='blue'>[HELPER] {name}</span>",
        "MODERATOR": f"<span class='darkGreen'>[MOD] {name}</span>",
        "GAME_MASTER": f"<span class='darkGreen'>[GM] {name}</span>",
        "ADMIN": f"<span class='red'>[ADMIN] {name}</span>",
        "STAFF": f"<span class='red'>[</span><span class='gold'>ዞ</span><span class='red'>] {name}</span>",
        "OWNER": f"<span class='red'>[OWNER] {name}</span>",
    }
    
    # If not predefined, replace color tags and add name to final span element
    return mark_safe(rank_formats.get(rank_name, f"{replace_color_tags(rank_name)[:-7] + f' {name}</span>'}"))
