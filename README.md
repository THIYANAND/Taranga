# TARANGA  
## Interactive Communication Systems Visualization Software

TARANGA is a professional desktop-based communication systems visualization software developed for understanding and analyzing analog, digital, and pulse modulation techniques through real-time waveform simulation and interactive parameter control.

The software provides animated waveform generation, dynamic parameter adjustment, and signal visualization for various communication modulation techniques used in modern communication systems.

---

# Download Software

## Windows Executable (.exe)

Download the latest TARANGA software release from:

➡️ [Download TARANGA](../../releases)

---

# Features

- Real-time waveform visualization
- Animated signal generation
- Interactive parameter controls
- Pause and resume waveform simulation
- Zoom and fit waveform view
- Cursor-based waveform inspection
- Professional GUI interface
- Multiple communication system modules
- Smooth real-time plotting using PyQtGraph

---

# Supported Modulation Techniques

## Analog Modulation
- Amplitude Modulation (AM)
- Frequency Modulation (FM)
- Phase Modulation (PM)

## Digital Modulation
- Amplitude Shift Keying (ASK)
- Frequency Shift Keying (FSK)
- Binary Phase Shift Keying (BPSK)
- Quadrature Phase Shift Keying (QPSK)
- Quadrature Amplitude Modulation (QAM)

## Pulse Modulation
- Pulse Width Modulation (PWM)
- Pulse Position Modulation (PPM)

---

# Technologies Used

- Python
- PySide6
- PyQtGraph
- NumPy

---

# Project Structure

```text
src/
│
├── main.py
│
├── gui/
│   ├── main_window.py
│   ├── home_page.py
│   │
│   ├── analog/
│   │   ├── am_window.py
│   │   ├── fm_window.py
│   │   └── pm_window.py
│   │
│   ├── digital/
│   │   ├── ask_window.py
│   │   ├── fsk_window.py
│   │   ├── bpsk_window.py
│   │   ├── qpsk_window.py
│   │   └── qam_window.py
│   │
│   └── pulse/
│       ├── pwm_window.py
│       └── ppm_window.py
│
├── assets/
│
├── requirements.txt
│
└── README.md