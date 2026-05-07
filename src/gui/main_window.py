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

        # ADD PAGES
        self.stack.addWidget(
            self.home_page
        )

        self.stack.addWidget(
            self.am_page
        )

        self.stack.addWidget(
            self.fm_page
        )

        self.stack.addWidget(
            self.pm_page
        )

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