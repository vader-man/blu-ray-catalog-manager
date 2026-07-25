1. Requirements
Hardware
	•	Raspberry Pi (recommended)
	•	Any Linux machine running Python 3.9+
Software
	•	Python 3
	•	Flask
	•	Home Assistant
	•	TMDB API key
	•	Blu‑ray.com CSV export (your collection)
---
2. Clone the Repository
git clone https://github.com/yourname/blu-ray-catalog-manager.git
cd blu-ray-catalog-manager
3. Install Python Dependencies
Inside the app/ folder:
pip install -r requirements.txt
This installs:
	•	Flask
	•	Requests
	•	TMDB client libraries
	•	CSV/JSON utilities
---
4. Prepare Folder Structure
Your project should contain:
app/
data/
scripts/
dashboard/
docs/
Ensure the following files exist:
	•	data/movies_raw.csv → Blu‑ray.com export
	•	data/locations.json → master catalog (initially empty or example)
	•	scripts/movies_alpha.py → CSV parser
	•	scripts/tmdb_resolver.py → metadata enrichment
	•	app/app.py → Flask backend
5. Import Your Blu‑ray.com CSV
Place your exported CSV here:
data/movies_raw.csv
Run the parser:
python3 scripts/movies_alpha.py
This generates:
data/movies_master.json
6. Run TMDB Metadata Enrichment
Edit your TMDB API key inside tmdb_resolver.py.
Then run:
python3 scripts/tmdb_resolver.py
This enriches:
	•	Posters
	•	Backdrops
	•	Runtime
	•	Overview
	•	Release year
The result is written into:
data/locations.json
This file becomes the master catalog used by the backend and Home Assistant.
7. Start the Flask Backend (Development Mode)
cd app
python3 app.py
Default URL:
http://<your-pi-ip>:5000
You should now see the Catalog Manager Web App.
8. Install as a systemd Service (Production)
Create:
/etc/systemd/system/bluray.service
Contents:
[Unit]
Description=Blu-ray Catalog Manager
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/blu-ray-catalog-manager/app/app.py
WorkingDirectory=/home/pi/blu-ray-catalog-manager/app
Restart=always
User=pi

[Install]
WantedBy=multi-user.target

Enable and start:
sudo systemctl enable bluray.service
sudo systemctl start bluray.service

Backend is now running permanently.

9. Configure Home Assistant
Add REST sensors
Example:
sensor:
  - platform: rest
    resource: http://<your-pi-ip>:5000/api/movies
    name: bluray_movies
    scan_interval: 60
Add input booleans and input text
Used for filters and search:
input_boolean:
  sort_duration:
  filter_4k:
  filter_dv:
  filter_atmos:

input_text:
  bluray_search:

Import the Lovelace Dashboard
Place the YAML from /dashboard/bluray_dashboard.yaml into:
	•	A new dashboard
	•	Or a view inside your existing dashboard
Update the API URL inside the card:
http://<your-pi-ip>:5000/api/movies
10. Verify Everything Works
You should now be able to:
	•	Open the Catalog Manager web app
	•	Edit movies inline
	•	Add DV/Atmos/Duration
	•	Export to Excel
	•	See your collection in Home Assistant
	•	Filter by 4K, DV, Atmos
	•	Sort by title, duration, recent
	•	View posters and backdrops
	•	Navigate shelf levels and blocks
Your Blu‑ray catalog is now fully integrated with Home Assistant.

11. Optional (Recommended)
Enable HTTPS reverse proxy
Using Nginx or HA Add‑on.
Backup your JSON
locations.json is your master catalog.
Automate TMDB updates
Run the resolver weekly via cron.
---
Installation Complete
Your Blu‑ray Catalog Manager is now fully installed and operational.


