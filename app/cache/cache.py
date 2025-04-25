from datetime import datetime, timedelta

cache = {}


def is_cache_valid(user_id: int, minutes: int = 5) -> bool:
    if user_id not in cache:
        return False
    last_fetched = cache[user_id]["timestamp"]
    return datetime.utcnow() - last_fetched < timedelta(minutes=minutes)
