from datetime import datetime

def format_timestamp(iso_str):

    dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%#d %B %Y - %#I:%M %p UTC")

