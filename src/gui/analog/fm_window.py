import numpy as np
import pyqtgraph as pg

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QSlider,
    QLineEdit,
    QPushButton
)

from PySide6.QtCore import Qt, QTimer


class FMWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("FM Modulation")

        self.resize(1400, 900)

        self.phase = 0

        self.is_running = True

        self.setup_ui()

        # TIMER
        self.timer = QTimer()

        self.timer.timeout.connect(self.update_waveforms)

        self.timer.start(30)

    def setup_ui(self):

        main_layout = QVBoxLayout()

        # TITLE
        title = QLabel("FREQUENCY MODULATION")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

            font-size: 28px;
            font-weight: bold;
            color: cyan;

        """)

        main_layout.addWidget(title)

        # DEFINITION
        definition = QLabel(
            "Frequency Modulation varies carrier frequency according to message signal."
        )

        definition.setWordWrap(True)

        definition.setStyleSheet("""

            font-size: 16px;
            padding: 5px;

        """)

        main_layout.addWidget(definition)

        # FORMULA
        formula = QLabel(
            "s(t) = Ac cos(2πfct + β sin(2πfmt))"
        )

        formula.setAlignment(Qt.AlignCenter)

        formula.setStyleSheet("""

            font-size: 22px;
            font-weight: bold;
            background-color: #222;
            color: cyan;
            padding: 15px;
            border-radius: 10px;

        """)

        main_layout.addWidget(formula)

        # PAUSE BUTTON
        self.pause_button = QPushButton("Pause")

        self.pause_button.setStyleSheet("""

            font-size: 16px;
            padding: 10px;

        """)

        self.pause_button.clicked.connect(
            self.toggle_animation
        )

        main_layout.addWidget(self.pause_button)

        # PARAMETERS
        parameter_layout = QGridLayout()

        # MESSAGE FREQUENCY
        self.msg_freq_slider = QSlider(Qt.Horizontal)

        self.msg_freq_slider.setMinimum(1)

        self.msg_freq_slider.setMaximum(20)

        self.msg_freq_slider.setValue(2)

        self.msg_freq_input = QLineEdit("2")

        parameter_layout.addWidget(
            QLabel("Message Frequency"),
            0,
            0
        )

        parameter_layout.addWidget(
            self.msg_freq_slider,
            0,
            1
        )

        parameter_layout.addWidget(
            self.msg_freq_input,
            0,
            2
        )

        # CARRIER FREQUENCY
        self.carrier_freq_slider = QSlider(Qt.Horizontal)

        self.carrier_freq_slider.setMinimum(10)

        self.carrier_freq_slider.setMaximum(100)

        self.carrier_freq_slider.setValue(30)

        self.carrier_freq_input = QLineEdit("30")

        parameter_layout.addWidget(
            QLabel("Carrier Frequency"),
            1,
            0
        )

        parameter_layout.addWidget(
            self.carrier_freq_slider,
            1,
            1
        )

        parameter_layout.addWidget(
            self.carrier_freq_input,
            1,
            2
        )

        # MODULATION INDEX
        self.mod_index_slider = QSlider(Qt.Horizontal)

        self.mod_index_slider.setMinimum(1)

        self.mod_index_slider.setMaximum(100)

        self.mod_index_slider.setValue(50)

        self.mod_index_input = QLineEdit("5")

        parameter_layout.addWidget(
            QLabel("Modulation Index"),
            2,
            0
        )

        parameter_layout.addWidget(
            self.mod_index_slider,
            2,
            1
        )

        parameter_layout.addWidget(
            self.mod_index_input,
            2,
            2
        )

        # MESSAGE AMPLITUDE
        self.msg_amp_slider = QSlider(Qt.Horizontal)

        self.msg_amp_slider.setMinimum(1)

        self.msg_amp_slider.setMaximum(10)

        self.msg_amp_slider.setValue(1)

        self.msg_amp_input = QLineEdit("1")

        parameter_layout.addWidget(
            QLabel("Message Amplitude"),
            3,
            0
        )

        parameter_layout.addWidget(
            self.msg_amp_slider,
            3,
            1
        )

        parameter_layout.addWidget(
            self.msg_amp_input,
            3,
            2
        )

        main_layout.addLayout(parameter_layout)

        # CURSOR LABEL
        self.cursor_label = QLabel(
            "Time: 0.000 s    Amplitude: 0.000"
        )

        self.cursor_label.setStyleSheet("""

            font-size: 14px;
            color: yellow;

        """)

        main_layout.addWidget(self.cursor_label)

        # PLOTS
        self.message_plot = pg.PlotWidget(
            title="Message Signal"
        )

        self.carrier_plot = pg.PlotWidget(
            title="Carrier Signal"
        )

        self.fm_plot = pg.PlotWidget(
            title="FM Signal"
        )

        main_layout.addWidget(self.message_plot)

        main_layout.addWidget(self.carrier_plot)

        main_layout.addWidget(self.fm_plot)

        self.setLayout(main_layout)

        # CURVES
        self.message_curve = self.message_plot.plot(
            pen=pg.mkPen('g', width=2)
        )

        self.carrier_curve = self.carrier_plot.plot(
            pen=pg.mkPen('y', width=2)
        )

        self.fm_curve = self.fm_plot.plot(
            pen=pg.mkPen('m', width=2)
        )

        # GRID
        self.message_plot.showGrid(x=True, y=True)

        self.carrier_plot.showGrid(x=True, y=True)

        self.fm_plot.showGrid(x=True, y=True)

        # CONNECT SLIDERS
        self.msg_freq_slider.valueChanged.connect(
            self.update_inputs
        )

        self.carrier_freq_slider.valueChanged.connect(
            self.update_inputs
        )

        self.mod_index_slider.valueChanged.connect(
            self.update_inputs
        )

        self.msg_amp_slider.valueChanged.connect(
            self.update_inputs
        )

        # CONNECT INPUT BOXES
        self.msg_freq_input.editingFinished.connect(
            self.update_sliders
        )

        self.carrier_freq_input.editingFinished.connect(
            self.update_sliders
        )

        self.mod_index_input.editingFinished.connect(
            self.update_sliders
        )

        self.msg_amp_input.editingFinished.connect(
            self.update_sliders
        )

        # MOUSE TRACKING
        self.fm_plot.scene().sigMouseMoved.connect(
            self.mouse_moved
        )

    def toggle_animation(self):

        if self.is_running:

            self.timer.stop()

            self.pause_button.setText("Resume")

            self.is_running = False

        else:

            self.timer.start(30)

            self.pause_button.setText("Pause")

            self.is_running = True

    def update_inputs(self):

        self.msg_freq_input.setText(
            str(self.msg_freq_slider.value())
        )

        self.carrier_freq_input.setText(
            str(self.carrier_freq_slider.value())
        )

        self.mod_index_input.setText(
            str(self.mod_index_slider.value() / 10)
        )

        self.msg_amp_input.setText(
            str(self.msg_amp_slider.value())
        )

    def update_sliders(self):

        try:

            self.msg_freq_slider.setValue(
                int(self.msg_freq_input.text())
            )

            self.carrier_freq_slider.setValue(
                int(self.carrier_freq_input.text())
            )

            self.mod_index_slider.setValue(
                int(float(self.mod_index_input.text()) * 10)
            )

            self.msg_amp_slider.setValue(
                int(self.msg_amp_input.text())
            )

        except:

            pass

    def mouse_moved(self, pos):

        vb = self.fm_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        x = point.x()

        y = point.y()

        self.cursor_label.setText(

            f"Time: {x:.3f} s    Amplitude: {y:.3f}"

        )

    def update_waveforms(self):

        self.phase += 0.1

        # PARAMETERS
        fm = self.msg_freq_slider.value()

        fc = self.carrier_freq_slider.value()

        beta = self.mod_index_slider.value() / 10

        amplitude = self.msg_amp_slider.value()

        # TIME
        t = np.linspace(0, 1, 3000)

        # MESSAGE SIGNAL
        message = amplitude * np.sin(
            2 * np.pi * fm * t + self.phase
        )

        # CARRIER SIGNAL
        carrier = np.cos(
            2 * np.pi * fc * t
        )

        # FM SIGNAL
        fm_signal = np.cos(

            2 * np.pi * fc * t +

            beta * np.sin(
                2 * np.pi * fm * t + self.phase
            )

        )

        # UPDATE CURVES
        self.message_curve.setData(
            t,
            message
        )

        self.carrier_curve.setData(
            t,
            carrier
        )

        self.fm_curve.setData(
            t,
            fm_signal
        )