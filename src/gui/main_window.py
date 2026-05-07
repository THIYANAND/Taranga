from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QListWidget,
    QStackedWidget
)

from gui.home_page import HomePage

from gui.analog.am_window import AMWindow
from gui.analog.fm_window import FMWindow
from gui.analog.pm_window import PMWindow

from gui.digital.ask_window import ASKWindow
from gui.digital.bpsk_window import BPSKWindow
from gui.digital.fsk_window import FSKWindow
from gui.digital.qam_window import QAMWindow
from gui.digital.qpsk_window import QPSKWindow

from gui.pulse.ppm_window import PPMWindow
from gui.pulse.pwm_window import PWMWindow


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("TARANGA")

        self.resize(1800, 1000)

        self.setup_ui()

    def setup_ui(self):

        layout = QHBoxLayout()

        # SIDEBAR
        self.sidebar = QListWidget()

        self.sidebar.setFixedWidth(250)

        self.sidebar.addItem("Home")

        self.sidebar.addItem("AM Modulation")
        self.sidebar.addItem("FM Modulation")
        self.sidebar.addItem("PM Modulation")

        self.sidebar.addItem("ASK Modulation")
        self.sidebar.addItem("BPSK Modulation")
        self.sidebar.addItem("FSK Modulation")
        self.sidebar.addItem("QAM Modulation")
        self.sidebar.addItem("QPSK Modulation")
        
        self.sidebar.addItem("PPM Modulation")
        self.sidebar.addItem("PWM Modulation")

        self.sidebar.setStyleSheet("""

            QListWidget {

                background-color: #111;
                color: white;
                font-size: 16px;
                padding: 10px;

            }

            QListWidget::item {

                padding: 15px;

            }

            QListWidget::item:selected {

                background-color: cyan;
                color: black;
                border-radius: 8px;

            }

        """)

        # STACK
        self.stack = QStackedWidget()

        # PAGES
        self.home_page = HomePage()

        self.am_page = AMWindow()
        self.fm_page = FMWindow()
        self.pm_page = PMWindow()

        self.ask_page = ASKWindow()
        self.bpsk_page = BPSKWindow()
        self.fsk_page = FSKWindow()
        self.qam_page = QAMWindow()
        self.qpsk_page = QPSKWindow()

        self.ppm_page = PPMWindow()
        self.pwm_page = PWMWindow()

        # ADD PAGES
        self.stack.addWidget(self.home_page)

        self.stack.addWidget(self.am_page)
        self.stack.addWidget(self.fm_page)
        self.stack.addWidget(self.pm_page)
        
        self.stack.addWidget(self.ask_page)
        self.stack.addWidget(self.bpsk_page)
        self.stack.addWidget(self.fsk_page)
        self.stack.addWidget(self.qam_page)
        self.stack.addWidget(self.qpsk_page)

        self.stack.addWidget(self.ppm_page)
        self.stack.addWidget(self.pwm_page)

        # CHANGE PAGE
        self.sidebar.currentRowChanged.connect(
            self.stack.setCurrentIndex
        )

        # DEFAULT PAGE
        self.sidebar.setCurrentRow(0)

        # ADD TO LAYOUT
        layout.addWidget(self.sidebar)

        layout.addWidget(self.stack)

        self.setLayout(layout)