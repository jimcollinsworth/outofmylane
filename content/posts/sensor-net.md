---
title: Sensor Net
slug: sensor-net
date: 2026-11-17
modified: 2026-11-17
tags: ai, mine, hardware
summary: Low-cost sensor network for Body Area Network (BAN) telemetry on Seeed Studio XIAO nRF52840 Sense and ESP32-C6 microcontrollers.
author: Jim Collinsworth, LLM-Argon
type: project
template: wip
url: sensor-net.html
save_as: sensor-net.html
status: published
---

`sensor-net` is a sensor network architecture for Body Area Network (BAN) and spatial telemetry applications targeting Seeed Studio XIAO nRF52840 Sense (CircuitPython) and ESP32-C6 (ESP-IDF v6.0.2) microcontrollers.

## Hardware Pin Mappings & Architecture

- **Battery Monitoring Network**: Uses board definitions `board.READ_BATT_ENABLE` and `board.VBATT` to toggle the power gate transistor, closing the circuit after scaling the 16-bit analog stream to prevent background leakage current drain.
- **Onboard Sensor Power Gates**: Startup wake routines set `board.IMU_PWR` and `board.MIC_PWR` high to power the silicon chips and connect internal pull-up paths (powered off at boot by default).
- **Shared Peripheral Bus Conflict Separation**: Isolates external I2C bus pins (`board.SDA` and `board.SCL`) inside independent execution wrappers so floating external pins do not cause pull-up faults on the shared internal IMU register bus.
- **PDM Microphone Hardware Bindings**: Maps audio capture to `board.PDM_CLK` and `board.PDM_DATA` targeting an unsigned 16-bit array buffer (`'H'`) aligned with microcontroller audio DMA page boundaries.
- **6-Axis Spatial Telemetry Tracking**: Reads `.acceleration` and `.gyro` properties from the onboard LSM6DS3TR-C IMU to produce orientation and rotational velocity matrices.
- **Soft-Reboot Memory Safety Wrappers**: Wraps hardware object initialization inside `try/except ValueError` blocks to recycle active pins across editor saves and serial terminal soft-reboots without register lock faults.

## Repository Layout & DevOps Pipeline

CircuitPython executes `code.py` from the board root; the repository organizes firmware into modular application and shared library directories:

```text
sensor-net/
└── src/
    ├── main-app/code.py       # Primary application entry point
    ├── testing/code.py        # Hardware diagnostic and sensor test runner
    └── common/                # Shared modules for startup, filtering, diagnostics, and BLE
        ├── code.py
        ├── startup.py
        └── ble.py
```

### CircuitPython Board Deployment & Serial Diagnostics
- **Dependency Sync**: `circup install --update` locates the connected board and updates libraries imported by `code.py`.
- **Serial Port Discovery**: `Get-CimInstance Win32_SerialPort | Select-Object` enumerates active COM endpoints.
- **Serial Monitor**: `putty.exe -serial COM12 -sercfg 115200` connects to the 115200 baud serial console.

### ESP32-C6 Build & Flash Pipeline (ESP-IDF v6.0.2)
- **Environment Activation**: `C:\esp\v6.0.2\esp-idf\export.bat` (or `python c:\esp\v6.0.2\esp-idf\tools\idf_tools.py export --format key-value`).

Target & Build Commands:

```bash
idf.py set-target esp32c6
idf.py menuconfig
idf.py build
idf.py flash
```
