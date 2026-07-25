#!/usr/bin/env python3
import json
import os
import re
import unicodedata
import requests
import sys

def log(msg):
    print(msg, file=sys.stderr)

BASE_DIR = "/home/<YOUR_PATH>/bluray"
CACHE_PATH = os.path.join(BASE_DIR, "posters.json")
TMDB_KEY_PATH = os.path.join(BASE_DIR, "tmdb_key.txt") #INSERT TMDB KEY IN THAT FILE

TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/original"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (RaspberryPi BluRay Library Script)"
}

# ---------------------------------------------------------
# OVERRIDES EAN 
# ---------------------------------------------------------
EAN_OVERRIDES = { 
    "7321970184693": {"poster_url": "...", "movie_year": "1982"},
    "5051893210019": {"poster_url": "...", "movie_year": "1982"},
}

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def load_api_key():
    if not os.path.exists(TMDB_KEY_PATH):
        log(f"TMDB key file not found: {TMDB_KEY_PATH}")
        return None
    with open(TMDB_KEY_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()

def load_cache():
    if not os.path.exists(CACHE_PATH):
        return {}
    try:
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)

def normalize_unicode(s):
    return unicodedata.normalize("NFKC", s or "")

def strip_disc_year_suffix(title):
    return re.sub(r"\(\d{4}\)\s*$", "", title).strip()

def remove_format_markers(t):
    if not t:
        return ""
    u = t.upper()

    markers = [
        "4K", "UHD", "ULTRA HD", "BLU-RAY", "BLURAY", "BD", "DVD", "3D",
        "DIGITAL", "STEELBOOK", "LIMITED EDITION", "COLLECTOR'S EDITION",
        "SPECIAL EDITION", "ANNIVERSARY EDITION", "REMASTERED",
        "DIRECTOR'S CUT", "EXTENDED CUT", "COMBO PACK",
        "3-MOVIE COLLECTION", "2-MOVIE", "4-MOVIE COLLECTION",
        "TRILOGY 4K", "TRILOGY",
        "THE COMPLETE SERIES", "SEASON", "GIFT SET"
    ]

    for m in markers:
        u = u.replace(m, "")

    u = u.replace("+", " ").replace("/", " ").replace("&", " ")
    u = " ".join(u.split())

    u = re.sub(r"\(4K.*?\)", "", u)
    u = re.sub(r"\(UHD.*?\)", "", u)

    return u.title().strip()

def extract_pack_base(title):
    t = normalize_unicode(title)

    if "+" in t:
        t = t.split("+", 1)[0].strip()
    if " / " in t:
        t = t.split(" / ", 1)[0].strip()
    if " & " in t:
        t = t.split(" & ", 1)[0].strip()

    if " - " in t:
        left, right = t.split(" - ", 1)
        if "colección" in right.lower() or "collection" in right.lower(): #overrides spanish title for collection
            t = left.strip()

    t = re.sub(r"\bTrilogy\b", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\bCollection\b", "", t, flags=re.IGNORECASE)

    t = strip_disc_year_suffix(t)
    t = remove_format_markers(t)

    return t.strip()

def extract_base_title(title):
    t = normalize_unicode(title)
    t = strip_disc_year_suffix(t)
    t = remove_format_markers(t)
    return t.strip()

# ---------------------------------------------------------
# TMDB API calls
# ---------------------------------------------------------
def tmdb_query_movie(title):
    api_key = load_api_key()
    if not api_key or not title:
        return None

    params = {"api_key": api_key, "query": title}

    try:
        r = requests.get(TMDB_SEARCH_URL, params=params, headers=HEADERS, timeout=10)
        data = r.json()
        results = data.get("results") or []
        if results:
            return results[0]
    except Exception as e:
        log(f"TMDB movie error: {e}")

    return None

def tmdb_movie_details(movie_id):
    api_key = load_api_key()
    if not api_key:
        return {}

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {"api_key": api_key, "append_to_response": "images"}

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        data = r.json()

        backdrop = None
        if data.get("backdrop_path"):
            backdrop = TMDB_IMAGE_BASE + data["backdrop_path"]

        images = data.get("images") or {}
        logos = images.get("logos") or []

        logo = None
        for img in logos:
            if img.get("iso_639_1") in ("en", None):
                logo = TMDB_IMAGE_BASE + img["file_path"]
                break

        return {
            "movie_year": data.get("release_date", "")[:4],
            "genres": [g["name"] for g in data.get("genres", [])],
            "overview": data.get("overview", ""),
            "runtime": data.get("runtime", 0),
            "tmdb_rating": data.get("vote_average", 0),
            "collection_name": data.get("belongs_to_collection", {}).get("name", ""),
            "backdrop_url": backdrop,
            "logo_url": logo
        }

    except Exception as e:
        log(f"TMDB details error: {e}")
        return {}

# ---------------------------------------------------------
# MAIN RESOLVER
# ---------------------------------------------------------
def get_poster(ean, title, year):

    if ean in EAN_OVERRIDES:
        log(f"Override aplicado para EAN {ean}")
        return EAN_OVERRIDES[ean]

    cache = load_cache()
    if ean in cache:
        return cache[ean]

    original = title or ""
    base = extract_base_title(original)
    pack_base = extract_pack_base(original)

    attempts = [
        base,
        pack_base,
        original,
        base.split()[0] if base else ""
    ]

    for q in attempts:
        if not q:
            continue

        result = tmdb_query_movie(q)
        if result:
            poster_path = result.get("poster_path")
            movie_id = result.get("id")

            if not poster_path:
                continue

            poster_url = TMDB_IMAGE_BASE + poster_path
            details = tmdb_movie_details(movie_id)

            final = {
                "poster_url": poster_url,
                **details
            }

            cache[ean] = final
            save_cache(cache)
            log(f"Found using: '{q}'")
            return final

    cache[ean] = {
        "poster_url": "",
        "movie_year": "",
        "genres": [],
        "overview": "",
        "runtime": 0,
        "tmdb_rating": 0,
        "collection_name": "",
        "backdrop_url": "",
        "logo_url": ""
    }

    save_cache(cache)
    log("No poster found (fallback applied)")
    return cache[ean]
