System Architecture Overview
This document describes the internal architecture of the Blu‑ray Catalog Manager, including backend components, data flow, JSON schema, REST API, and Home Assistant integration.
It is intended for developers or advanced users who want to understand how the system works behind the scenes.
---
1. High‑Level Architecture
The system consists of four major layers:
+--------------------------------------------------+
| 1. Data Source (Blu-ray.com CSV)                 |
+--------------------------------------------------+
            |
            v
+--------------------------------------------------+
| 2. Data Pipeline (Python scripts)                |
|    - CSV parser (movies_alpha.py)                |
|    - TMDB resolver (tmdb_resolver.py)            |
+--------------------------------------------------+
            |
            v
+--------------------------------------------------+
| 3. Backend (Flask app)                           |
|    - REST API                                    |
|    - Catalog Manager Web UI                      |
+--------------------------------------------------+
            |
            v
+--------------------------------------------------+
| 4. Home Assistant Integration                    |
|    - REST sensors                                |
|    - Lovelace dashboard                          |
+--------------------------------------------------+

Each layer is independent, modular, and replaceable.
2. Data Source: Blu‑ray.com CSV
The system begins with the CSV export from Blu‑ray.com, which contains:
	•	Title
	•	Format
	•	UPC/EAN
	•	Studio
	•	Release year
	•	Edition notes
This CSV is placed in:
data/movies_raw.csv

It is parsed and normalized by the pipeline.
---
3. Data Pipeline (Python)
The pipeline consists of two main scripts:
---
3.1 `movies_alpha.py` — CSV Parser
Responsibilities:
	•	Read Blu‑ray.com CSV
	•	Normalize titles
	•	Extract EAN/UPC
	•	Clean edition markers
	•	Handle commas/quotes
	•	Remove duplicates
	•	Produce a clean JSON file:
data/movies_master.json

This file contains the base structure for each movie.
---
3.2 `tmdb_resolver.py` — Metadata Enrichment
Responsibilities:
	•	Query TMDB using title + year
	•	Fetch:
	◦	Poster
	◦	Backdrop
	◦	Runtime
	◦	Overview
	◦	Release year
	◦	Genres
	•	Merge TMDB data with movies_master.json
	•	Produce the final master catalog:
data/locations.json

This is the file used by the backend and Home Assistant.
---
4. Master Catalog (JSON Schema)
The master catalog is stored in:
data/locations.json
Each movie entry follows this schema:
{
  "ean": "string",
  "title": "string",
  "location": "string",
  "dv": true,
  "atmos": false,
  "duration": 120,
  "poster": "url",
  "backdrop": "url",
  "year": 2021,
  "overview": "string"
}
Notes:
	•	location, dv, atmos, and duration are editable via the web app.
	•	TMDB fields are updated via the resolver script.
	•	Additional fields can be added without breaking the system.
---
5. Backend Architecture (Flask)
The backend lives in:
app/app.py

It provides:
5.1 REST API
Endpoints:
GET /api/movies
Returns the full catalog (locations.json).
POST /api/update
Updates a single field (inline editing).
POST /api/add
Adds a new movie.
POST /api/delete
Removes a movie.
All changes are written directly to locations.json.
---
5.2 Catalog Manager Web UI
Located in:
app/templates/index.html

Features:
	•	Inline editing
	•	Add/delete movies
	•	CSV import
	•	Excel export
	•	Sorting by title
	•	Filtering by 4K
	•	Duration support
	•	DV/Atmos toggles
The UI communicates with the backend via AJAX calls to /api/update.
---
6. Home Assistant Integration
Home Assistant consumes the backend via REST.
---
6.1 REST Sensor
Example:
sensor:
  - platform: rest
    resource: http://<your-pi-ip>:5000/api/movies
    name: bluray_movies
    scan_interval: 60
This sensor loads the entire catalog into HA.
---
6.2 Input Helpers
Used for filtering and sorting:
input_boolean:
  filter_4k:
  filter_dv:
  filter_atmos:
  sort_duration:

input_text:
  bluray_search:

6.3 Lovelace Dashboard
Located in:
dashboard/bluray_dashboard.yaml

Features:
	•	Search
	•	Filters (4K, DV, Atmos)
	•	Sorting (Title, Duration, Recent)
	•	Posters and backdrops
	•	Physical shelf mapping
	•	Responsive grid layout
The dashboard reads the REST sensor and applies filters client‑side.
---
7. Data Flow Diagram
Blu-ray.com CSV
      |
      v
movies_alpha.py
      |
      v
tmdb_resolver.py
      |
      v
locations.json (master catalog)
      |
      v
Flask Backend (REST API + Web UI)
      |
      v
Home Assistant (REST sensor)
      |
      v
Lovelace Dashboard
 8. Updating the Catalog
There are three ways to update the catalog:
1. Web UI (recommended)
	•	Edit DV/Atmos
	•	Edit location
	•	Edit duration
	•	Add/delete movies
2. TMDB resolver
Refresh metadata:
python3 scripts/tmdb_resolver.py

3. CSV re‑import
If you update your Blu‑ray.com collection:
python3 scripts/movies_alpha.py
python3 scripts/tmdb_resolver.py



