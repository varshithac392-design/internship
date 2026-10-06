# Drone Propulsion Test Rig — Calibration & Test Session

A starter implementation based on the uploaded calibration/error-correction guide.

## Core behavior
- Every new test session starts at record 0.
- The active calibration profile persists between tests.
- Raw sensor values are never overwritten.
- Corrected value = `raw * gain + offset`.
- Missing calibration defaults to gain 1.0 / offset 0.0 and is marked `UNCALIBRATED`.
- Dataset and live sensor data remain explicitly separated.

## Run

Requirements: Python 3.10+

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

## Test

```bash
pytest
```

## GitHub

```bash
git init
git add .
git commit -m "Initial drone propulsion calibration system"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Hardware/CAN communication is intentionally represented as an interface/stub. No CAN IDs, sensor coefficients, or hardware values are fabricated.
