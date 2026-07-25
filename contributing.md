# Contributing to Blu-ray Catalog Manager

Thank you for your interest in contributing to the **Blu-ray Catalog Manager** project!  
This document explains how to report issues, request features, and submit pull requests.

The goal of this project is to provide a clean, modular, and extensible system for managing physical Blu-ray / 4K UHD collections integrated with Home Assistant.

---

## Before You Start

Please make sure you have:

- Read the main documentation (`docs/README.md`)
- Reviewed the installation guide (`docs/INSTALL.md`)
- Understood the architecture (`docs/ARCHITECTURE.md`)
- Checked existing issues to avoid duplicates

---

## Reporting Issues

If you encounter a bug, please include:

1. A clear description of the problem  
2. Steps to reproduce the issue  
3. Expected behavior  
4. Actual behavior  
5. Relevant logs (if any)  
6. Your environment:
   - OS / hardware (e.g., Raspberry Pi 4)
   - Python version
   - Home Assistant version
   - Browser (for the web app)

Please **do not** include:

- Your real IP address  
- Your TMDB API key  
- Your real `locations.json`  
- Sensitive personal data  

---

## Requesting Features

Feature requests are welcome!

When submitting a feature request, please include:

- A clear explanation of the feature  
- Why it would be useful  
- How it might work  
- Any examples or mockups  
- Whether it affects:
  - The backend
  - The dashboard
  - The data pipeline
  - The JSON schema

---

## Submitting Pull Requests

Pull requests are appreciated.  
To keep the project clean and maintainable, please follow these guidelines:

### 1. Fork the repository  
Create your own fork and work in a feature branch.

### 2. Use clear branch names  
Examples:

- `feature/add-runtime-sort`
- `fix/csv-parser-commas`
- `enhancement/dashboard-layout`

### 3. Follow the project structure  
Place files in the correct folders:

app/          → Flask backend
scripts/      → Data pipeline
data/         → Example data only
dashboard/    → Home Assistant UI
docs/         → Documentation
systemd/      → Service examples


### 4. Do not commit sensitive data  
Never include:

- Real IPs  
- Real TMDB keys  
- Real catalog data  
- Personal system paths  

### 5. Write clear commit messages  
Examples:

- `Fix EAN parsing for long numeric values`
- `Add DV/Atmos icons to dashboard`
- `Improve TMDB resolver error handling`

### 6. Ensure code quality  
- Use consistent formatting  
- Avoid hardcoded paths  
- Add comments where needed  
- Test your changes locally  

### 7. Submit the PR  
Include:

- A description of the change  
- Why it’s needed  
- Any breaking changes  
- Screenshots (if UI-related)

---

## Coding Style

### Python
- Follow PEP8 where possible  
- Use descriptive variable names  
- Avoid global state  
- Prefer modular functions  

### JavaScript (Web App)
- Keep logic inside `static/js/`  
- Avoid inline scripts when possible  
- Use clear function names  
- Comment complex logic  

### YAML (Dashboard)
- Keep indentation consistent  
- Avoid hardcoded IPs  
- Use variables where possible  

---

## Testing

Before submitting a PR, please test:

- CSV import  
- TMDB resolver  
- Web app editing  
- REST API endpoints  
- Dashboard filters and sorting  

If your change affects any of these, please mention it in the PR.

---

## Community Guidelines

- Be respectful  
- Be constructive  
- Keep discussions technical  
- Avoid sharing personal data  
- Help others when possible  

---

## Thank You

Your contributions help improve the project and make it more useful for collectors around the world.  
Whether you report a bug, request a feature, or submit code — **thank you!**

