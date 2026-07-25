Standard Configuration Guide
This document explains how to configure and customize the Blu‑ray Catalog Manager to match your environment, file paths, shelf layout, and Home Assistant setup.
It assumes you have already completed the installation steps described in INSTALL.md.

1. File Paths
The project uses a simple folder structure:
app/
data/
scripts/
dashboard/
You may place the project anywhere on your system.
If you change the location, update:
Systemd service file
ExecStart and WorkingDirectory must point to the correct paths:
ExecStart=/usr/bin/python3 /path/to/blu-ray-catalog-manager/app/app.py
WorkingDirectory=/path/to/blu-ray-catalog-manager/app
Scripts
If you run scripts manually, ensure you are inside the project root:
cd /path/to/blu-ray-catalog-manager
python3 scripts/movies_alpha.py
python3 scripts/tmdb_resolver.py
Home Assistant REST sensors
Update the API URL:
resource: http://<your-pi-ip>:5000/api/movies

2. TMDB API Key
Edit scripts/tmdb_resolver.py:
TMDB_API_KEY = "your_api_key_here"
You can obtain an API key from:
https://www.themoviedb.org/settings/api
---
3. Shelf Layout (Levels & Blocks)
The physical shelf layout is stored inside:
data/locations.json
Each movie entry contains:
{
  "ean": "1234567890123",
  "title": "Example Movie",
  "location": "LEVEL 2 (BLOCK 3)",
  "dv": true,
  "atmos": false,
  "duration": 120
}
You may define any structure you want:
Examples
	•	LEVEL 1 (BOTTOM)
	•	LEVEL 2 (BLOCK 0)
	•	LEVEL 3 (TOP)
	•	CABINET A / ROW 4
	•	SHELF 1 / SECTION B
The dashboard does not enforce any specific naming convention.
It simply displays whatever text you provide.

4. Dashboard Configuration
The Lovelace dashboard YAML is located in:
dashboard/bluray_dashboard.yaml
You may customize:
API URL
Search for:
http://<your-pi-ip>:5000/api/movies
Replace with your backend address.
Grid layout
Modify:
columns: 4

Button labels
For example:
	•	“4K”
	•	“BR”
	•	“DV”
	•	“AT”
	•	“Time”
Theme colors
Inside button-card styles:
background: "#9c27b0"

Search field
Uses:
input_text.bluray_search

5. Home Assistant Entities
The dashboard uses:
Input booleans

input_boolean:
  filter_4k:
  filter_dv:
  filter_atmos:
  sort_duration:
Input text
input_text:
  bluray_search:

REST sensor
sensor:
  - platform: rest
    resource: http://<your-pi-ip>:5000/api/movies
    name: bluray_movies
    scan_interval: 60
You may rename these entities, but you must update the dashboard YAML accordingly.
6. CSV Import Behavior
The CSV parser (movies_alpha.py) expects the Blu‑ray.com export format.
If your CSV differs, you may adjust:
Column names
Inside the parser, update:
row["Title"]
row["UPC"]
row["Format"]

Title cleaning rules
You may add or remove:
	•	Removing edition markers
	•	Normalizing spacing
	•	Handling quotes or commas
EAN handling
To avoid Excel corruption, the export uses:
="EAN"
You may disable this if you prefer raw CSV output.

7. JSON Schema (Master Catalog)
The master catalog is stored in:

data/locations.json

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

You may add new fields:
	•	studio
	•	region
	•	edition
	•	collection
	•	tags
	•	favorite: true
The Flask backend and dashboard will ignore unknown fields unless you explicitly add support.
---
8. Backend API Endpoints
The Flask app exposes:
GET /api/movies
Returns the full catalog.
POST /api/update
Updates a single field (inline editing).
POST /api/add
Adds a new movie.
POST /api/delete
Removes a movie.
You may add new endpoints if needed.
---
9. Customizing Sorting & Filtering
Sorting and filtering logic is inside:
app/templates/index.html

You may customize:
Sorting
.sort((a, b) => ...)

Filtering
if (filter4k && !title.includes("4K")) return;

--
You can add:
	•	UHD
	•	Ultra HD
	•	2160p
	•	HDR10
	•	Steelbook
	•	Criterion
	•	Arrow Video


10. Optional: Advanced Configuration
Reverse proxy (HTTPS)
Use Nginx or HA add‑on.
Cron jobs
Automate TMDB updates weekly.
Backups
Backup locations.json regularly.
Multiple collections
You may create:
	•	locations_movies.json
	•	locations_games.json
	•	locations_music.json
And expose multiple endpoints.
---
Configuration Complete
Your Blu‑ray Catalog Manager is now fully customizable and adaptable to any installation.