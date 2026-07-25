#!/usr/bin/env python3
import json
import re
import os
import sys
from datetime import datetime
from tmdb_resolver import get_poster

BASE_DIR = "/home/<YOUR_PATH>/bluray"
CSV_PATH = os.path.join(BASE_DIR, "collection.csv")
LOCATIONS_PATH = os.path.join(BASE_DIR, "locations.json")

COLUMN_MAP = {
    "title": "title",
    "studio": "studio",
    "country code": "country",
    "upc": "upc",
    "ean": "ean",
    "asin": "asin",
    "release date": "release_date",
    "slipcover": "slipcover",
    "casing": "casing",
    "memorabilia": "memorabilia",
    "blu-ray discs": "bluray_discs",
    "dvd discs": "dvd_discs",
    "digital copy": "digital_copy",
    "date added": "date_added",
    "retailer": "retailer",
    "price": "price",
}

def log(msg):
    print(msg, file=sys.stderr)

def normalize(s):
    return s.replace("\ufeff", "").strip().lower()

def clean_line(line):
    line = line.replace('"""', '"')
    line = line.replace('""', '"')
    return line

CSV_REGEX = re.compile(r'''
    (?:^|,)
    (
      "(?:[^"]*)"
      |
      [^,]*
    )
''', re.VERBOSE)

def parse_csv_line(line):
    line = clean_line(line).strip()
    fields = CSV_REGEX.findall(line)
    return [f.strip().strip('"') for f in fields]

def detect_format(row):
    bd = row.get("bluray_discs", "")
    dvd = row.get("dvd_discs", "")
    digital = row.get("digital_copy", "")

    if bd and bd != "0":
        return "Blu-ray"
    if dvd and dvd != "0":
        return "DVD"
    if digital.lower() in ("yes", "true", "1"):
        return "Digital"
    return "Unknown"

def extract_year(date):
    date = (date or "").strip()
    m = re.search(r'(\d{4})$', date)
    return m.group(1) if m else ""

def load_locations():
    if not os.path.exists(LOCATIONS_PATH):
        return {}
    with open(LOCATIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_collection():
    items = []

    with open(CSV_PATH, encoding="utf-8") as f:
        lines = f.readlines()

    headers = [normalize(h) for h in parse_csv_line(lines[0])]

    for line in lines[1:]:
        row_values = parse_csv_line(line)
        clean = {}

        for i, value in enumerate(row_values):
            if i < len(headers):
                key = headers[i]
                if key in COLUMN_MAP:
                    clean[COLUMN_MAP[key]] = value.strip()

        items.append({
            "title": clean.get("title", ""),
            "year": extract_year(clean.get("release_date", "")),
            "format": detect_format(clean),
            "upc": clean.get("upc", ""),
            "ean": clean.get("ean", ""),
            "asin": clean.get("asin", ""),
            "studio": clean.get("studio", ""),
            "country": clean.get("country", ""),
            "date_added": clean.get("date_added", ""),
            "slipcover": clean.get("slipcover", ""),
            "casing": clean.get("casing", ""),
            "memorabilia": clean.get("memorabilia", ""),
            "retailer": clean.get("retailer", ""),
            "price": clean.get("price", ""),
        })

    return items

def build_format_icons(item):
    icons = []

    title = item["title"].upper()
    casing = item["casing"].lower()
    slip = item["slipcover"]

    if "4K" in title:
        icons.append("4k")
    if "steelbook" in casing:
        icons.append("steelbook")
    if slip == "1":
        icons.append("slipcover")

    return icons

# ---------------------------------------------------------
# 1) TITLE OVERRIDES (TMDB) If a title shows wrong, correct it here
# ---------------------------------------------------------
TITLE_OVERRIDES = {
    # EXAMPLE
    "Up": {"title": "Up", "year": "2009"},
    "WALL•E": {"title": "WALL-E", "year": "2008"},
}

# ---------------------------------------------------------
# 2) POSTER OVERRIDES (manual) If a poster is wrong, correct it here
# ---------------------------------------------------------
POSTER_OVERRIDES = {
    # EXAMPLE
    "up": "https://www.themoviedb.org/t/p/w1280/mFvoEwSfLqbcWwFsDjQebn9bzFe.jpg",
    "wall\u2022e-4k": "https://image.tmdb.org/t/p/w1280/2Wjn5vxvJmomJQkLuUwyX2hBaif.jpg",
}

# ---------------------------------------------------------
# 3) INTELLIGENT DEDUPE (keep BR + 4K)
# ---------------------------------------------------------
def dedupe(items):
    grouped = {}
    result = []

    for item in items:
        title = item["title"].strip()
        base = title.replace("4K", "").strip().lower()

        if base not in grouped:
            grouped[base] = {"br": None, "4k": None}

        if "4K" in title.upper():
            if grouped[base]["4k"] is None:
                grouped[base]["4k"] = item
        else:
            if grouped[base]["br"] is None:
                grouped[base]["br"] = item

    for base, editions in grouped.items():
        if editions["br"]:
            result.append(editions["br"])
        if editions["4k"]:
            result.append(editions["4k"])

    return result

# ---------------------------------------------------------
# 4) ENRICH ITEMS
# ---------------------------------------------------------
def enrich_items(items, locations):
    enriched = []
    total = len(items)

    log(f"Starting enrichment for {total} titles...")

    for index, item in enumerate(items, start=1):
        title = item["title"]
        year = item["year"]
        ean = item["ean"]

        override = TITLE_OVERRIDES.get(title)
        if override:
            title = override.get("title", title)
            year = override.get("year", year)

        log(f"[{index}/{total}] Fetching metadata for: {title} ({year})")

        meta = get_poster(ean, title, year)

        # generar slug antes del override de poster
        slug = (
            item["title"]
            .lower()
            .replace(":", "")
            .replace(" ", "-")
            .replace("(", "")
            .replace(")", "")
            .replace(".", "")
            .replace(",", "")
        )
        item["slug"] = slug

        # override manual de poster
        override_poster = POSTER_OVERRIDES.get(slug)
        if override_poster:
            item["poster_url"] = override_poster
        else:
            item["poster_url"] = meta.get("poster_url", "")

        item["backdrop_url"] = meta.get("backdrop_url", "")
        item["logo_url"] = meta.get("logo_url", "")
        item["genres"] = meta.get("genres", [])
        item["overview"] = meta.get("overview", "")
        item["runtime"] = meta.get("runtime", 0)
        item["tmdb_rating"] = meta.get("tmdb_rating", 0)
        item["collection_name"] = meta.get("collection_name", "")
        item["movie_year"] = meta.get("movie_year", "")

        item["format_icon"] = build_format_icons(item)

        loc = locations.get(ean, {})
        item["cabinet_level"] = loc.get("level")
        item["dv"] = loc.get("dv", False)
        item["atmos"] = loc.get("atmos", False)
        # NEW adds from locations.json
        item["duration"] = loc.get("duration", "")
        enriched.append(item)

    log("Enrichment completed.")
    return enriched

def sort_alpha(items):
    return sorted(items, key=lambda x: x["title"].lower())

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    items = load_collection()
    items = dedupe(items)
    locations = load_locations()

    enriched = enrich_items(items, locations)
    sorted_items = sort_alpha(enriched)
    catalog = { item["slug"]: item for item in sorted_items }

    output = {
        "count": len(sorted_items),
        "movies": sorted_items,
        "catalog": catalog
    }

    print(json.dumps(output))

if __name__ == "__main__":
    main()
