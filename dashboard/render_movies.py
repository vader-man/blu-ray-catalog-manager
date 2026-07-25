# render_movies.py

sensor = hass.states.get("sensor.movies_cards")
cards = sensor.attributes.get("cards") if sensor else []

rendered_entities = []

def safe(text):
    if not text:
        return "unknown"

    # Lowercase
    text = text.lower()

    # Replace accented characters manually
    accents = {
        "á": "a", "à": "a", "ä": "a", "â": "a",
        "é": "e", "è": "e", "ë": "e", "ê": "e",
        "í": "i", "ì": "i", "ï": "i", "î": "i",
        "ó": "o", "ò": "o", "ö": "o", "ô": "o",
        "ú": "u", "ù": "u", "ü": "u", "û": "u",
        "ñ": "n"
    }
    cleaned = ""
    for ch in text:
        cleaned += accents.get(ch, ch)

    text = cleaned

    # Replace & with "and"
    text = text.replace("&", "and")

    # Replace spaces and hyphens with underscore
    text = text.replace(" ", "_").replace("-", "_")

    # Remove invalid characters manually
    invalid = "!\"#$%&'()*+,/:;<=>?@[\\]^`{|}~"
    cleaned = ""
    for ch in text:
        if ch in invalid:
            continue
        if ch.isalnum() or ch == "_":
            cleaned += ch

    # Collapse multiple underscores
    final = ""
    prev = ""
    for ch in cleaned:
        if ch == "_" and prev == "_":
            continue
        final += ch
        prev = ch

    # Remove leading/trailing underscores
    final = final.strip("_")

    return final or "unknown"


for movie in cards:

    title = movie.get("title", "Unknown")
    poster = movie.get("poster_url", "")
    year = movie.get("movie_year", movie.get("year", "----"))
    runtime = movie.get("runtime", 0)
    rating = movie.get("tmdb_rating", 0)
    icons = movie.get("format_icon", []) or []
    dv = movie.get("dv", False)
    da = movie.get("atmos", False)
    cabinet = movie.get("cabinet_level", "Unknown")
    added = movie.get("date_added", "")
    duration = movie.get("duration", "")
    slug = movie.get("slug") or title

    safe_slug = safe(slug)
    entity_id = f"sensor.movie_{safe_slug}"

    hass.states.set(
        entity_id,
        "ok",
        {
            "title": title,
            "poster": poster,
            "year": year,
            "format": "4K" if "4k" in icons else "Blu-ray",
            "dv": dv,
            "da": da,
            "cabinet": cabinet,
            "added": added,
            "runtime": runtime,
            "rating": rating,
            "duration": duration,
        },
    )

    rendered_entities.append(entity_id)

hass.states.set(
    "sensor.movies_cards_rendered",
    "ok",
    {"entities": rendered_entities}
)
