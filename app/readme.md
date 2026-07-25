# Data Folder

This folder contains the data files used by the Blu-ray Catalog Manager.  
For privacy and security reasons, **only example files are included in the public repository**.

Your real collection data should **never** be committed to GitHub.

---

## Files Included in This Folder

### `locations.json`
A safe example of the master catalog file used by the backend and Home Assistant.

This file demonstrates the JSON structure expected by the system:

- EAN / UPC
- Title #JUST IN APP TO SHOW IN HTML, THIS FIEL MUST NOT BE INCLUDED IN BACKED LOCATIONS.JSON THAT IS AUTOMATICALLY CREATED BY THE APP
- Location (shelf mapping)
- Dolby Vision flag
- Dolby Atmos flag
- Duration (runtime)

Replace this file with your real `locations.json` when running the system locally.

---

### `collection.csv`
A minimal example of the CSV exported from Blu-ray.com.

This file shows the expected column structure:


Replace this file with your real `movies_raw.csv` when running the pipeline.

---

## Files You Should NOT Upload

Do **not** commit any of the following:

- `locations.json` (your real catalog)
- `collection.csv` (your real Blu-ray.com export)
- Any file containing:
  - Real EANs
  - Real shelf locations
  - Personal notes
  - Sensitive metadata

These files contain personal collection information and should remain private.

---

## How to Use Your Real Data Locally

1. Export your collection from Blu-ray.com as CSV.
2. Place it in this folder as:

