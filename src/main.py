import sys

from PySide6.QtWidgets import QApplication

from gui.home_page import HomePage

app = QApplication(sys.argv)

window = HomePage()

window.show()

sys.exit(app.exec())