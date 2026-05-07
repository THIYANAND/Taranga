from gui import TarangaGUI
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

window = TarangaGUI()
window.show()

sys.exit(app.exec())