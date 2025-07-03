from datetime import datetime

def format_timestamp(iso_str):
    """Convert ISO timestamp to '1st April 2021 - 9:30 PM UTC' format."""
    dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%-d %B %Y - %-I:%M %p UTC")
