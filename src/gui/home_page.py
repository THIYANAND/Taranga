import sys
from gui.analog.am_window import AMWindow

from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QGridLayout
)

from PySide6.QtCore import Qt


class HomePage(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("TARANGA")

        self.resize(900, 600)

        self.setup_ui()

    def setup_ui(self):

        main_layout = QVBoxLayout()

        # TITLE
        title = QLabel("TARANGA")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Communication Systems Simulator")
        subtitle.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # GRID
        grid = QGridLayout()

        # ANALOG
        analog_label = QLabel("ANALOG MODULATION")
        grid.addWidget(analog_label, 0, 0)

        am_btn = QPushButton("AM")
        am_btn.clicked.connect(self.open_am_window)
        fm_btn = QPushButton("FM")
        pm_btn = QPushButton("PM")

        grid.addWidget(am_btn, 1, 0)
        grid.addWidget(fm_btn, 1, 1)
        grid.addWidget(pm_btn, 1, 2)

        # DIGITAL
        digital_label = QLabel("DIGITAL MODULATION")
        grid.addWidget(digital_label, 2, 0)

        ask_btn = QPushButton("ASK")
        fsk_btn = QPushButton("FSK")
        bpsk_btn = QPushButton("BPSK")
        qpsk_btn = QPushButton("QPSK")
        qam_btn = QPushButton("QAM")

        grid.addWidget(ask_btn, 3, 0)
        grid.addWidget(fsk_btn, 3, 1)
        grid.addWidget(bpsk_btn, 3, 2)
        grid.addWidget(qpsk_btn, 4, 0)
        grid.addWidget(qam_btn, 4, 1)

        # PULSE
        pulse_label = QLabel("PULSE MODULATION")
        grid.addWidget(pulse_label, 5, 0)

        pwm_btn = QPushButton("PWM")
        ppm_btn = QPushButton("PPM")

        grid.addWidget(pwm_btn, 6, 0)
        grid.addWidget(ppm_btn, 6, 1)

        main_layout.addLayout(grid)

        self.setLayout(main_layout)
    def open_am_window(self):
        self.am_window = AMWindow()
        self.am_window.show()