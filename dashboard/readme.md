# Home Assistant Dashboard

This folder contains the Lovelace dashboard configuration used to display and interact with the Blu-ray Catalog Manager inside Home Assistant.

The dashboard provides:

- Search by title  
- Filters (4K, Dolby Vision, Dolby Atmos)  
- Sorting (Title, Duration, Recently Added)  
- Dynamic posters and backdrops  
- Responsive grid layout  
- Shelf location display  
- Integration with the Flask backend via REST  

Only **example files** are included in the public repository to avoid exposing personal IP addresses or Home Assistant configuration details.

---

## Files Included

### `bluray_dashboard.example.yaml`
A safe example of the Lovelace dashboard configuration.

This file demonstrates:

- How to load data from the REST sensor  
- How to bind filters and sorting to input booleans  
- How to display posters, backdrops, and metadata  
- How to structure the grid layout  
- How to reference the backend API using a placeholder URL

Replace the placeholder API URL:

```yaml
api_url: "http://YOUR-API-URL/api/movies"

with your actual backend address when running locally.
---
`assets/`
Optional folder for dashboard assets:
• Custom icons
• Background images
• Logos
• Theme elements
This folder is empty by default.
You may add your own assets if you want to customize the dashboard visually.
---
Requirements in Home Assistant
To use the dashboard, you need:
1. REST Sensor
Add this to your Home Assistant configuration:

sensor:
  - platform: rest
    resource: http://YOUR-API-URL/api/movies
    name: bluray_movies
    scan_interval: 60

2. Input Helpers
Used for filtering and sorting:

input_boolean:
  filter_4k:
  filter_dv:
  filter_atmos:
  sort_duration:

input_text:
  bluray_search:

3. Custom Cards (recommended)
The dashboard uses:
• button-card
• card-mod (optional)
Install them via HACS if needed.
---
Importing the Dashboard
There are two ways to import the dashboard:
Option A — As a standalone dashboard #RECOMMENDED
1. Go to Settings → Dashboards
2. Click Add Dashboard
3. Choose YAML mode
4. Paste the contents of bluray_dashboard.example.yaml
5. Update the API URL
6. Save and reload

Another way to Force YAML mode by including in configuration.yaml:

lovelace:
  dashboards:
    bluray-dashboard:
      mode: yaml
      title: Blu-ray Library
      icon: mdi:movie-open
      show_in_sidebar: true
      filename: lovelace-bluray.yaml

Option B — As a view inside an existing dashboard
1. Open your dashboard
2. Click Edit
3. Add a new view
4. Switch to YAML editor
5. Paste the YAML
6. Update the API URL
7. Save
---
Customization
You can customize:
Grid Layout

columns: 4

Colors and Themes
Inside button-card styles:

background: "#9c27b0"

Icons
Replace or add icons in:

dashboard/assets/icons/


Backdrops
You may add custom backgrounds in:

dashboard/assets/backgrounds/

Filters
Modify logic for:
• 4K
• DV
• Atmos
• Duration
Sorting
Adjust sorting functions in the dashboard YAML.
---
Privacy Notes
The example dashboard file:
• Does not contain your IP
• Does not contain your Home Assistant entity names
• Does not contain your real catalog
• Is safe to publish publicly
When using your real dashboard locally:
• Do not commit your real YAML
• Do not commit your real IP
• Do not commit your real entity names
• Do not commit your real catalog data
---
✔ Summary
This folder contains:
• A safe example Lovelace dashboard
• Optional assets for customization
• Instructions for importing and configuring the dashboard
• Privacy guidelines
• Customization tips
Use the example file as a template and replace placeholders with your real configuration when running the system locally.




