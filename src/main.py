import sys

from PySide6.QtWidgets import QApplication

from gui.home_page import HomePage

app = QApplication(sys.argv)

window = HomePage()

window.show()
app.setStyleSheet("""

    QWidget {
        background-color: #111;
        color: white;
        font-size: 14px;
    }

    QPushButton {
        background-color: #222;
        border: 1px solid cyan;
        padding: 10px;
        border-radius: 8px;
    }

    QPushButton:hover {
        background-color: cyan;
        color: black;
    }

    QLineEdit {
        background-color: #222;
        border: 1px solid cyan;
        padding: 5px;
    }

""")
sys.exit(app.exec())