from pydantic import BaseModel, Field
from typing import Literal, Optional

DataSource = Literal["LIVE_SENSOR", "DATASET", "DERIVED", "UNAVAILABLE"]

class StartTestRequest(BaseModel):
    operator: str = "unknown"

class MeasurementRequest(BaseModel):
    parameter: str
    raw_value: float
    unit: Optional[str] = None
    source: DataSource = "LIVE_SENSOR"

class Measurement(BaseModel):
    parameter: str
    raw_value: float
    corrected_value: Optional[float]
    unit: Optional[str]
    test_session_id: str
    calibration_id: str
    source: DataSource
    status: str = "VALID"
    record_index: int
