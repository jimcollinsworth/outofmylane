---
title: AI Metronome
slug: ai-metronome
date: 2026-11-17
modified: 2026-11-17
tags: ai, mine, hardware, music
summary: Embedded acoustic-synchronizing companion for mechanical metronomes using an onboard digital MEMS microphone, Phase-Locked Loop beat clock, and 6-axis IMU gesture control.
author: Jim Collinsworth, LLM-Argon
template: wip
status: published
---

`ai-metronome` is an embedded acoustic-synchronizing companion for mechanical metronomes ([jimcollinsworth/ai-metronome](https://github.com/jimcollinsworth/ai-metronome)). Placed on or inside a physical metronome enclosure, the firmware listens to mechanical escapement clicks through an onboard pulse-density modulation (PDM) digital MEMS microphone, locks onto the tempo with a Phase-Locked Loop (PLL) beat clock, and drives RGB LED visual timing feedback without screens or external buttons.

## Target Hardware & Signal Processing

- **Microcontroller**: Seeed Studio XIAO nRF52840 Sense (`src/xiao_nrf52840_sense/circuitpython/code.py`).
- **Acoustic Input**: Onboard PDM digital MEMS microphone (`audiobusio.PDMIn` DMA ring buffer) with band-limited transient filtering, attack-slope gating, and adaptive ambient noise floor tracking to isolate mechanical tick transients from polyphonic piano audio and room reverberation.
- **Motion Input**: Onboard 6-axis LSM6DS3TR-C inertial measurement unit (IMU) over internal I2C for gesture recognition.
- **Oscillator**: Internal Phase-Locked Loop (PLL) beat clock driving LED timing across acoustic dropouts.

## Operating Modes & IMU Gesture Switching

Mode selection is controlled through the onboard accelerometer using two physical gestures:

1. **Two Shakes**: Pick up the unit and shake it back and forth twice.
2. **Single Drop / Surface Tap**: Set or tap the unit onto the table or piano surface.

Upon gesture detection, the device emits a 350 ms white LED burst (all RGB diodes illuminated), pauses, and flashes *N* pulses in the active mode's color (1 to 4) while resetting refractory audio timers:

- **Mode 1 — On-Beat (Red)**: Emits a red flash synchronized with every physical click (1×).
- **Mode 2 — Upbeat / In-Between (Blue)**: Emits a blue flash halfway between beats (`t + IOI/2`).
- **Mode 3 — 4/4 Meter (Green)**: Emits a green flash on Beat 1 (downbeat) and remains dark on Beats 2, 3, and 4. Resets to Beat 1 after 2 seconds of silence.
- **Mode 4 — 3/4 Meter (Green)**: Emits a green flash on Beat 1 (downbeat) and remains dark on Beats 2 and 3. Resets to Beat 1 after 2 seconds of silence.

## Hardware-in-the-Loop Tooling (`xiao-cli`)

The repository provides `xiao-cli` (`tools/xiao_cli.py`) to discover mounted `CIRCUITPY` USB drives and serial COM ports at 115200 baud:

- `uv run xiao-cli status`: Reports drive mount path, `boot_out.txt` runtime build info, COM port, and USB VID/PID.
- `uv run xiao-cli deploy --test`: Copies firmware to flash and runs the 6-point on-device verification suite (`POWER_DIAG`, `MIC_POWER`, `MIC_DMA_STREAM`, `IMU_BUS`, `IMU_ACCEL`, `CAL_AND_READY`).
- `uv run xiao-cli monitor`: Streams live serial telemetry including click detections, noise floor shifts, BPM calculations, and IMU gesture events.
