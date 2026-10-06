import json
from pathlib import Path
from .calibration import CalibrationProfile, CalibrationParameter

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PROFILE_FILE = DATA_DIR / "calibration.json"

def default_profile() -> CalibrationProfile:
    return CalibrationProfile(
        calibration_id="CAL-UNSET",
        status="UNCALIBRATED",
        parameters={}
    )

def load_profile() -> CalibrationProfile:
    if not PROFILE_FILE.exists():
        return default_profile()
    data = json.loads(PROFILE_FILE.read_text())
    params = {
        k: CalibrationParameter(**v)
        for k, v in data["parameters"].items()
    }
    return CalibrationProfile(
        calibration_id=data["calibration_id"],
        status=data["status"],
        parameters=params,
    )

def save_profile(profile: CalibrationProfile) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    payload = {
        "calibration_id": profile.calibration_id,
        "status": profile.status,
        "parameters": {
            k: {"gain": v.gain, "offset": v.offset}
            for k, v in profile.parameters.items()
        }
    }
    PROFILE_FILE.write_text(json.dumps(payload, indent=2))
