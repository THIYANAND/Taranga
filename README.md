from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QVBoxLayout,
    QLabel
)

from PySide6.QtCore import Qt

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

        # MAIN LAYOUT
        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.setSpacing(0)

        # SIDEBAR CONTAINER
        sidebar_container = QVBoxLayout()

        sidebar_container.setContentsMargins(
            0,
            0,
            0,
            0
        )

        sidebar_container.setSpacing(0)

        # SOFTWARE TITLE
        title = QLabel("TARANGA")

        title.setAlignment(Qt.AlignCenter)

        title.setFixedHeight(90)

        title.setStyleSheet("""

            background-color: #0b0f14;
            color: cyan;
            font-size: 28px;
            font-weight: bold;
            border-bottom: 1px solid #222;

        """)

        sidebar_container.addWidget(title)

        # SIDEBAR
        self.sidebar = QListWidget()

        self.sidebar.setFixedWidth(280)

        # MENU ITEMS
        self.sidebar.addItem("🏠   Home")

        self.sidebar.addItem("──────── ANALOG ────────")

        self.sidebar.addItem("📡   AM Modulation")
        self.sidebar.addItem("📡   FM Modulation")
        self.sidebar.addItem("📡   PM Modulation")

        self.sidebar.addItem("──────── DIGITAL ────────")

        self.sidebar.addItem("💻   ASK Modulation")
        self.sidebar.addItem("💻   BPSK Modulation")
        self.sidebar.addItem("💻   FSK Modulation")
        self.sidebar.addItem("💻   QAM Modulation")
        self.sidebar.addItem("💻   QPSK Modulation")

        self.sidebar.addItem("──────── PULSE ────────")

        self.sidebar.addItem("⚡   PPM Modulation")
        self.sidebar.addItem("⚡   PWM Modulation")

        self.sidebar.setStyleSheet("""

            QListWidget {

                background-color: #0f1419;
                color: white;
                border: none;
                font-size: 15px;
                padding-top: 10px;
                outline: none;

            }

            QListWidget::item {

                padding: 14px;
                margin-left: 6px;
                margin-right: 6px;
                border-radius: 8px;

            }

            QListWidget::item:selected {

                background-color: cyan;
                color: black;
                font-weight: bold;

            }

            QListWidget::item:hover {

                background-color: #1b2733;

            }

        """)

        sidebar_container.addWidget(
            self.sidebar
        )

        # SIDEBAR WIDGET
        sidebar_widget = QWidget()

        sidebar_widget.setLayout(
            sidebar_container
        )

        sidebar_widget.setFixedWidth(280)

        sidebar_widget.setStyleSheet("""

            background-color: #0f1419;
            border-right: 1px solid #222;

        """)

        # STACK
        self.stack = QStackedWidget()

        self.stack.setStyleSheet("""

            background-color: #111827;

        """)

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

        # PAGE MAP
        self.page_map = {

            0: 0,

            2: 1,
            3: 2,
            4: 3,

            6: 4,
            7: 5,
            8: 6,
            9: 7,
            10: 8,

            12: 9,
            13: 10

        }

        # CONNECT SIDEBAR
        self.sidebar.currentRowChanged.connect(
            self.change_page
        )

        # DEFAULT PAGE
        self.sidebar.setCurrentRow(0)

        # ADD TO MAIN LAYOUT
        main_layout.addWidget(
            sidebar_widget
        )

        main_layout.addWidget(
            self.stack
        )

        self.setLayout(main_layout)

    def change_page(self, index):

        if index in self.page_map:

            self.stack.setCurrentIndex(
                self.page_map[index]
            )