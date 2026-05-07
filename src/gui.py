import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSlider
)

from PySide6.QtCore import Qt

import pyqtgraph as pg

from signal_generator import generate_sine_wave


class TarangaGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("TARANGA")
        self.resize(800, 500)

        layout = QVBoxLayout()

        title = QLabel("TARANGA - Signal Visualizer")
        layout.addWidget(title)

        # Frequency Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(20)
        self.slider.setValue(5)

        layout.addWidget(QLabel("Frequency"))
        layout.addWidget(self.slider)

        # Plot Widget
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        self.setLayout(layout)

        # Initial Plot
        self.update_plot()

        # Slider Event
        self.slider.valueChanged.connect(self.update_plot)

    def update_plot(self):

        freq = self.slider.value()

        t, y = generate_sine_wave(freq=freq)

        self.plot_widget.clear()

        self.plot_widget.plot(t, y)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = TarangaGUI()

    window.show()

    sys.exit(app.exec())