# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2026-07-25
### Added
- Initial public release of the Blu-ray Catalog Manager.
- Complete Flask backend with REST API.
- Catalog Manager Web App with inline editing.
- CSV import (Blu-ray.com format) and Excel export.
- TMDB metadata enrichment pipeline.
- Master catalog JSON structure (`locations.json`).
- Home Assistant REST integration.
- Full Lovelace dashboard with search, filters, sorting, and dynamic visuals.
- Example files:
  - `locations.example.json`
  - `movies_raw.example.csv`
  - `bluray.example.service`
  - `bluray_dashboard.example.yaml`
- Complete documentation:
  - `README.md`
  - `INSTALL.md`
  - `CONFIG.md`
  - `ARCHITECTURE.md`
  - `CONTRIBUTING.md`
- MIT License.

### Changed
- Cleaned all sensitive data (IP addresses, system paths, API keys).
- Replaced real catalog files with safe example files.
- Improved folder structure for clarity and maintainability.

### Removed
- Personal Home Assistant configuration details.
- Real Blu-ray collection data.
- TMDB API key.
- System-specific paths and user information.

---

## [Unreleased]
### Planned
- Optional Docker container for backend deployment.
- Statistics dashboard (total runtime, formats, DV/Atmos counts).
- Shelf visualization view.
- NFC/QR tagging support for physical discs.
- Multi-collection support (games, music, DVDs).
- Automatic TMDB refresh via scheduled tasks.
- Dashboard on othe formats or platforms...
- Who knows what else