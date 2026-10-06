from dataclasses import dataclass
from typing import Dict

@dataclass
class CalibrationParameter:
    gain: float = 1.0
    offset: float = 0.0

    def apply(self, raw: float) -> float:
        return raw * self.gain + self.offset

@dataclass
class CalibrationProfile:
    calibration_id: str
    status: str
    parameters: Dict[str, CalibrationParameter]

    def correct(self, parameter: str, raw: float) -> float:
        p = self.parameters.get(parameter, CalibrationParameter())
        return p.apply(raw)
