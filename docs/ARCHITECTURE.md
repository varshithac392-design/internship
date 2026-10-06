# Architecture

Sensor → Raw measurement → Calibration → Filtering → Validation → Engineering value → CAN → Master ESP32 → Raspberry Pi → Backend → Dashboard

This starter does not invent CAN IDs or hardware capabilities. The calibration layer supports:

`corrected = raw * gain + offset`

A new test resets test-session state but keeps the active calibration profile.
