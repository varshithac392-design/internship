from backend.calibration import CalibrationParameter

def test_offset():
    p = CalibrationParameter(gain=1.0, offset=0.05)
    assert p.apply(1.65) == 1.70

def test_gain_offset():
    p = CalibrationParameter(gain=1.02, offset=0.10)
    assert round(p.apply(9.80), 3) == 10.096
