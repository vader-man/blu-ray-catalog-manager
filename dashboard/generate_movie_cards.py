# generate_movie_cards.py

base_sensor = "sensor.movies_alpha"

state_obj = hass.states.get(base_sensor)
if not state_obj:
    logger.error(f"{base_sensor} not found")
else:
    movies = state_obj.attributes.get("movies", [])

    if not movies:
        logger.error("generate_movie_cards: there are no movies y movies_alpha")
    else:
        cards = []

        for movie in movies:
            slug = movie.get("slug")
            if not slug:
                continue

            safe_slug = slug.replace("-", "_")
            entity_id = f"sensor.movie_{safe_slug}"

            cards.append({
                "entity": entity_id,
                "title": movie.get("title"),
                "poster_url": movie.get("poster_url"),
                "backdrop_url": movie.get("backdrop_url"),
                "logo_url": movie.get("logo_url"),
                "movie_year": movie.get("movie_year"),
                "format_icon": movie.get("format_icon"),
                "dv": movie.get("dv"),
                "atmos": movie.get("atmos"),
                "runtime": movie.get("runtime"),
                "tmdb_rating": movie.get("tmdb_rating"),
                "cabinet_level": movie.get("cabinet_level"),
                "date_added": movie.get("date_added"),
                "duration": movie.get("duration", ""),
                "slug": slug,
            })

        hass.states.set(
            "sensor.movies_cards",
            len(cards),
            {
                "cards": cards
            }
        )

        logger.error("generate_movie_cards: sensor.movies_cards correctly created")
