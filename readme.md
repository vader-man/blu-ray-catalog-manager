Blu‑ray Catalog Manager for Home Assistant
A complete physical media cataloging system integrated with Home Assistant, featuring a Flask backend, a web‑based catalog editor, TMDB metadata enrichment, and a fully interactive Lovelace dashboard.
This project is designed for collectors who want to manage their physical Blu‑ray / 4K UHD library with the same convenience and visual polish as digital media platforms.
---
Overview
This system provides:
	•	A Flask backend running on a Raspberry Pi (or any Linux machine)
	•	A web catalog editor with inline editing
	•	Automatic metadata enrichment using TMDB
	•	A JSON master file representing the entire collection
	•	A Home Assistant dashboard with search, filters, sorting, and dynamic visuals
	•	Full CSV import/export, including runtime (duration)
	•	Mapping of discs to physical shelf locations
	•	REST sensors in Home Assistant for real‑time updates
It is a complete ecosystem, not a single script or dashboard.
---
Key Features
Catalog Manager Web App
	•	Add, edit, and delete movies
	•	Inline editing for:
	◦	Title
	◦	Location
	◦	Dolby Vision
	◦	Dolby Atmos
	◦	Duration
	•	CSV import (Blu‑ray.com export)
	•	Excel export (EAN preserved as text)
	•	JSON export for Home Assistant
Metadata Enrichment
	•	TMDB resolver script:
	◦	Poster
	◦	Backdrop
	◦	Runtime
	◦	Release year
	◦	Genres
	◦	Overview
Home Assistant Dashboard
	•	Search by title
	•	Filters:
	◦	4K
	◦	Blu‑ray
	◦	Dolby Vision
	◦	Dolby Atmos
	•	Sorting:
	◦	Title
	◦	Duration
	◦	Recently added
	•	Dynamic badges (DV/AT icons)
	•	Backdrop background per movie
	•	Responsive grid layout
	•	Physical shelf mapping (Levels / Blocks)
Backend Architecture
	•	Flask app running as a systemd service
	•	JSON master file (locations.json)
	•	REST endpoints consumed by Home Assistant
	•	Python scripts for TMDB enrichment and CSV parsing
---
Data Source: Blu‑ray.com Collection Export
This project uses the Blu‑ray.com CSV export as the initial source of truth for the physical media collection.
Blu‑ray.com’s CSV includes:
	•	Title
	•	Format
	•	EAN / UPC
	•	Studio
	•	Release year
	•	Edition notes
However, it does not include:
	•	Dolby Vision
	•	Dolby Atmos
	•	Runtime
	•	Physical shelf location
These fields are added manually through the Catalog Manager app.
CSV Characteristics and Known Issues
The Blu‑ray.com CSV has several quirks:
	•	EANs longer than 15 digits may be misinterpreted by Excel
	•	Some titles contain commas or quotes
	•	Multi‑disc sets may share the same EAN
	•	Some releases have missing EANs
	•	Edition markers (e.g., “4K”, “Steelbook”) appear inside the title
The included parser and editor handle these issues automatically.
---
Architecture

+-----------------------+
| Blu-ray.com CSV       |
+-----------------------+
            |
            v
+-----------------------+
| movies_alpha.py       |  --> parses CSV, cleans data
+-----------------------+
            |
            v
+-----------------------+
| TMDB Resolver         |  --> enriches metadata
+-----------------------+
            |
            v
+-----------------------+
| locations.json        |  --> master catalog
+-----------------------+
            |
            v
+-----------------------+
| Flask Backend         |  --> REST API
+-----------------------+
            |
            v
+-----------------------+
| Home Assistant        |  --> REST sensors + dashboard
+-----------------------+

Requirements
Hardware
	•	Raspberry Pi (recommended)
	•	Any Linux machine works
Software
	•	Python 3
	•	Flask
	•	Home Assistant
	•	TMDB API key
	•	Custom Lovelace cards:
	◦	button-card
	◦	card-mod (optional)
---
Installation (Summary)
Full installation instructions are provided in INSTALL.md.
1. Clone the repository
git clone https://github.com/yourname/blu-ray-catalog-manager.git
2. Install Python dependencies
pip install -r requirements.txt
3. Configure systemd service for Flask
sudo systemctl enable bluray.service
sudo systemctl start bluray.service
4. Configure Home Assistant
	•	Add REST sensors
	•	Add input booleans and input text
	•	Import the Lovelace dashboard YAML
	•	Point the dashboard to your Flask API URL
---
Configuration
Full configuration details are provided in CONFIG.md.
You can customize:
	•	Shelf levels and blocks
	•	Dashboard layout
	•	API endpoints
	•	File paths
	•	TMDB API key
	•	CSV import behavior
---
Screenshots
(Add your images here)
	•	Dashboard
	•	Catalog Manager app
	•	Excel export
	•	Shelf mapping
---
FAQ
Can I use this without a Raspberry Pi?
Yes. Any Linux machine running Python 3 works.
Can I change the shelf layout?
Yes. Levels and blocks are fully configurable.
Can I add new metadata fields?
Yes. The JSON structure and editor can be extended easily.
Does this work with Plex/Kodi?
This project is designed for physical media, not digital libraries.
---
License
MIT License.
You are free to modify, distribute, and adapt the project.
---
Credits
	•	Blu‑ray.com for the CSV export
	•	TMDB for metadata
	•	Home Assistant community
	•	Project created by Jorge A.