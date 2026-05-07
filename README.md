# Evo2Web

Evo2Web project codebase (frontend + backend) for sequence analysis/generation workflows.

## Repository scope

This repository publishes source code only.

Excluded from version control:
- Large genome datasets (e.g. `genome_data/`)
- Model parameters/checkpoints/weights
- Runtime caches, build artifacts, and local DB files
- Potentially sensitive local environment files

## Structure

- `Evo2Front/`: Vue 3 + Vite frontend
- `Evo2Back/`: Django backend

## Run (example)

Frontend:
```bash
cd Evo2Front
npm install
npm run dev
```

Backend:
```bash
cd Evo2Back
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```
