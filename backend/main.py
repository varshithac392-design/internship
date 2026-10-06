from fastapi import FastAPI
from .models import StartTestRequest, MeasurementRequest
from .store import load_profile, save_profile
from .calibration import CalibrationProfile, CalibrationParameter

app = FastAPI(title="Drone Propulsion Test Rig API")

state = {
    "session_id": None,
    "operator": None,
    "record_index": 0,
    "running": False,
    "measurements": [],
}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/calibration")
def get_calibration():
    p = load_profile()
    return {
        "calibration_id": p.calibration_id,
        "status": p.status,
        "parameters": {
            k: {"gain": v.gain, "offset": v.offset}
            for k, v in p.parameters.items()
        },
    }

@app.post("/api/calibration")
def set_calibration(payload: dict):
    profile = CalibrationProfile(
        calibration_id=payload["calibration_id"],
        status=payload.get("status", "CALIBRATED"),
        parameters={
            k: CalibrationParameter(
                gain=float(v.get("gain", 1.0)),
                offset=float(v.get("offset", 0.0)),
            )
            for k, v in payload.get("parameters", {}).items()
        },
    )
    save_profile(profile)
    return get_calibration()

@app.post("/api/test/start")
def start_test(req: StartTestRequest):
    # New test state is reset; calibration is deliberately NOT reset.
    state["session_id"] = f"TEST-{len(state['measurements']) + 1:03d}"
    state["operator"] = req.operator
    state["record_index"] = 0
    state["measurements"] = []
    state["running"] = True
    return {
        "test_session_id": state["session_id"],
        "record_index": 0,
        "calibration": get_calibration(),
    }

@app.post("/api/test/stop")
def stop_test():
    state["running"] = False
    return {
        "test_session_id": state["session_id"],
        "running": False,
        "measurements": state["measurements"],
    }

@app.post("/api/measurement")
def measurement(req: MeasurementRequest):
    if not state["running"]:
        return {"status": "REJECTED", "reason": "TEST_NOT_RUNNING"}

    profile = load_profile()
    corrected = None
    status = "VALID"

    if req.source != "UNAVAILABLE":
        corrected = profile.correct(req.parameter, req.raw_value)
        if profile.status != "CALIBRATED":
            status = "UNCALIBRATED"

    record = {
        "parameter": req.parameter,
        "raw_value": req.raw_value,
        "corrected_value": corrected,
        "unit": req.unit,
        "test_session_id": state["session_id"],
        "calibration_id": profile.calibration_id,
        "source": req.source,
        "status": status,
        "record_index": state["record_index"],
    }
    state["measurements"].append(record)
    state["record_index"] += 1
    return record

@app.get("/api/test")
def current_test():
    return {
        "test_session_id": state["session_id"],
        "operator": state["operator"],
        "record_index": state["record_index"],
        "running": state["running"],
        "measurements": state["measurements"],
    }

@app.get("/")
def dashboard():
    return {"message": "Drone Propulsion Test Rig API", "docs": "/docs"}
