# 🌱 Track Your Plant

A simple Python app for tracking houseplants — when they were acquired, when they need water, and their progress over time.

Built for the General Assembly Python Fundamentals project.

## Features

- Add a new plant (name, location, date acquired, watering frequency, sunlight needs)
- Record care activities (watering, fertilizing, repotting, pruning)
- View which plants are due for watering
- Search plants by name or location
- View all plants
- Attach progress photos (file paths) to a plant

## Files

| File | What it is |
|---|---|
| `backend.py` | Core functions: add, search, care log, due check |
| `plant.py` | Command-line menu to run the app in a terminal |
| `Mohamed Kadhem.ipynb` | Same app, runnable in Jupyter Notebook |
| `app.py` | Web version of the app, built with Streamlit |

## How to Run

**Command line / Jupyter** — keep `backend.py` in the same folder, then either run:
```bash
python plant.py
```
or open `Mohamed Kadhem.ipynb` in Jupyter and run all cells.

**Web app (Streamlit)**
```bash
pip install streamlit pandas
streamlit run app.py
```

## Data

All data is saved to CSV files in the same folder:
- `plants.csv` — your plants
- `care_history.csv` — care/watering log
- `plant_photos.csv` — photo file paths

## Team

- Meqdad Muhana
- Hajar Marzooq
- Mohamed Kadhem
