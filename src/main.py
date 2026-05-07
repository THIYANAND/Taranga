import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from PySide6.QtGui import QIcon

app = QApplication(sys.argv)
window = MainWindow()
window.setWindowIcon(
    QIcon("assets/Taranga_Logo.ico")
)
window.showMaximized()
sys.exit(app.exec())