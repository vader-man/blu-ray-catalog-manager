# blu-ray-catalog-manager
Blu‑ray Catalog Manager — Full Home Assistant integration for physical Blu‑ray / 4K UHD collections. Flask backend, TMDB metadata pipeline, Lovelace dashboard, and complete documentation.
# Blu-ray Catalog Manager
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-green.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Integration-41BDF5.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Stable-success.svg)
![GitHub stars](https://img.shields.io/github/stars/vader-man/blu-ray-catalog-manager.svg)
![GitHub forks](https://img.shields.io/github/forks/vader-man/blu-ray-catalog-manager.svg)
![GitHub issues](https://img.shields.io/github/issues/vader-man/blu-ray-catalog-manager.svg)
![Last commit](https://img.shields.io/github/last-commit/vader-man/blu-ray-catalog-manager.svg)

A complete system for managing physical **Blu-ray / 4K UHD collections** with full **Home Assistant integration**.  
Includes a Flask backend, TMDB metadata pipeline, REST API, and a Lovelace dashboard with search, filters, sorting, and dynamic visuals.

---

## Features

- **Flask backend** with REST API  
- **Web app** for editing your catalog (DV, Atmos, runtime, location…)  
- **TMDB metadata pipeline** (posters, backdrops, overview, year)  
- **CSV import** from Blu-ray.com  
- **JSON master catalog** (`locations.json`)  
- **Home Assistant integration** via REST sensors  
- **Lovelace dashboard** with:
  - Search
  - Filters (4K, DV, Atmos)
  - Sorting (title, duration, recently added)
  - Responsive grid layout
  - Posters + backdrops
- **Systemd service example**  
- **Complete documentation**  
- **Safe example files** (no personal data)

---

## Project Structure

app/            → Flask backend + web app
scripts/        → CSV parser + TMDB resolver + utilities
data/           → Example data files (safe for GitHub)
dashboard/      → Lovelace dashboard (example)
systemd/        → Example service file
docs/           → Full documentation
screenshots/    → Optional screenshots


---

## Documentation

Toda la documentación está en la carpeta `docs/`:

- [INSTALL.md](docs/install.md) — instalación paso a paso  
- [CONFIG.md](docs/configuration.md) — configuración del backend y HA  
- [ARCHITECTURE.md](docs/architecture.md) — arquitectura del sistema  
- [CONTRIBUTING.md](docs/contributing.md) — cómo colaborar  
- [CHANGELOG.md](docs/changelog.md) — historial de cambios  

---

## Installation (Quick Start)

1. Clone the repository:
git clone https://github.com/YOUR-USER/blu-ray-catalog-manager (github.com in Bing)


2. Install dependencies:
pip install -r requirements.txt


3. Run the backend:
python3 app/app.py


4. Import your Blu-ray.com CSV:
python3 scripts/movies_alpha.py
python3 scripts/tmdb_resolver.py


5. Start using the web app:
http://YOUR-SERVER:5000


6. Integrate with Home Assistant using the example dashboard.

---

## Privacy & Safety

This repository contains **only example data**:

- No real IPs  
- No real TMDB keys  
- No real catalog  
- No personal system paths  

Your real data stays local.

---

## Screenshots

Screenshots are optional and can be placed in:
docs/screenshots/


Placeholders are included.

---

## License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome.  
Please read the [CONTRIBUTING.md](docs/contributing.md) file before submitting pull requests.

---

## Status

The project is stable and actively maintained.


