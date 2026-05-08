# TARANGA  
### Interactive Communication Systems Visualization Software

<p align="center">

Real-Time Communication Systems Simulation and Visualization Platform

</p>

---

## Overview

TARANGA is a modern desktop-based communication systems visualization software developed for understanding, simulating, and analyzing various analog, digital, and pulse modulation techniques through real-time animated waveform generation and interactive parameter control.

The software is designed for:
- Communication Systems Learning
- Engineering Laboratories
- Academic Demonstrations
- Signal Visualization
- Modulation Analysis

TARANGA provides an intuitive graphical interface for visualizing modulation techniques used in modern communication systems.

---

# Download Software

## Windows Executable (.exe)

The latest executable version of TARANGA can be downloaded from:

➡️ **[Download TARANGA Releases](../../releases)**

> Download the `.exe` file from the latest release section for direct usage on Windows systems.

---

# Key Features

- Real-time animated waveform visualization
- Interactive parameter tuning using sliders and input fields
- Dynamic modulation signal generation
- Pause and resume waveform animation
- Zoom and fit waveform controls
- Cursor-based signal amplitude inspection
- Professional desktop-based GUI
- Modular architecture for scalability
- Smooth plotting using PyQtGraph
- Optimized real-time rendering engine
- Categorized communication system modules

---

# Supported Modulation Techniques

## Analog Modulation
| Technique | Description |
|---|---|
| AM | Amplitude Modulation |
| FM | Frequency Modulation |
| PM | Phase Modulation |

---

## Digital Modulation
| Technique | Description |
|---|---|
| ASK | Amplitude Shift Keying |
| FSK | Frequency Shift Keying |
| BPSK | Binary Phase Shift Keying |
| QPSK | Quadrature Phase Shift Keying |
| QAM | Quadrature Amplitude Modulation |

---

## Pulse Modulation
| Technique | Description |
|---|---|
| PWM | Pulse Width Modulation |
| PPM | Pulse Position Modulation |

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core Development |
| PySide6 | GUI Framework |
| PyQtGraph | Real-Time Plotting |
| NumPy | Signal Processing & Mathematical Computation |

---

# Software Architecture

```text
TARANGA/
│
├── src/
│   ├── main.py
│   │
│   ├── gui/
│   │   ├── main_window.py
│   │   ├── home_page.py
│   │   │
│   │   ├── analog/
│   │   │   ├── am_window.py
│   │   │   ├── fm_window.py
│   │   │   └── pm_window.py
│   │   │
│   │   ├── digital/
│   │   │   ├── ask_window.py
│   │   │   ├── fsk_window.py
│   │   │   ├── bpsk_window.py
│   │   │   ├── qpsk_window.py
│   │   │   └── qam_window.py
│   │   │
│   │   └── pulse/
│   │       ├── pwm_window.py
│   │       └── ppm_window.py
│   │
│   └── assets/
│
├── requirements.txt
│
└── README.md