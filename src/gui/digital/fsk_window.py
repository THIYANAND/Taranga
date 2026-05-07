import numpy as np
import pyqtgraph as pg

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QSlider,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)

from PySide6.QtCore import Qt, QTimer

# SMOOTH CURVES
pg.setConfigOptions(antialias=True)


class FSKWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("FSK Modulation")

        self.resize(1600, 900)

        self.phase = 0

        self.is_running = True

        self.setup_ui()

        # TIMER
        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_waveforms
        )

        self.timer.start(30)

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setSpacing(6)

        main_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        # TITLE
        title = QLabel("FREQUENCY SHIFT KEYING")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

            font-size: 22px;
            font-weight: bold;
            color: cyan;
            padding: 4px;

        """)

        main_layout.addWidget(title)

        # DEFINITION
        definition = QLabel(
            "Frequency Shift Keying changes carrier frequency according to binary data."
        )

        definition.setWordWrap(True)

        definition.setStyleSheet("""

            font-size: 13px;
            color: white;
            padding: 2px;

        """)

        main_layout.addWidget(definition)

        # FORMULA
        formula = QLabel(
            "s(t) = A cos(2πf₁t) or A cos(2πf₂t)"
        )

        formula.setAlignment(Qt.AlignCenter)

        formula.setStyleSheet("""

            font-size: 18px;
            font-weight: bold;
            background-color: #1a1a1a;
            color: cyan;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid cyan;

        """)

        main_layout.addWidget(formula)

        # BUTTONS
        button_layout = QHBoxLayout()

        self.pause_button = QPushButton(
            "Pause"
        )

        self.pause_button.clicked.connect(
            self.toggle_animation
        )

        self.fit_button = QPushButton(
            "Fit Waveform"
        )

        self.fit_button.clicked.connect(
            self.reset_view
        )

        button_style = """

            QPushButton {

                background-color: #222;
                color: white;
                padding: 8px;
                border-radius: 6px;
                border: 1px solid cyan;
                font-size: 13px;

            }

            QPushButton:hover {

                background-color: cyan;
                color: black;

            }

        """

        self.pause_button.setStyleSheet(
            button_style
        )

        self.fit_button.setStyleSheet(
            button_style
        )

        button_layout.addWidget(
            self.pause_button
        )

        button_layout.addWidget(
            self.fit_button
        )

        main_layout.addLayout(
            button_layout
        )

        # PARAMETERS
        parameter_layout = QGridLayout()

        parameter_layout.setVerticalSpacing(6)

        # BIT FREQUENCY
        self.bit_freq_slider = QSlider(
            Qt.Horizontal
        )

        self.bit_freq_slider.setMinimum(1)

        self.bit_freq_slider.setMaximum(20)

        self.bit_freq_slider.setValue(5)

        self.bit_freq_input = QLineEdit("5")

        parameter_layout.addWidget(
            QLabel("Bit Frequency"),
            0,
            0
        )

        parameter_layout.addWidget(
            self.bit_freq_slider,
            0,
            1
        )

        parameter_layout.addWidget(
            self.bit_freq_input,
            0,
            2
        )

        # FREQUENCY 1
        self.freq1_slider = QSlider(
            Qt.Horizontal
        )

        self.freq1_slider.setMinimum(10)

        self.freq1_slider.setMaximum(100)

        self.freq1_slider.setValue(20)

        self.freq1_input = QLineEdit("20")

        parameter_layout.addWidget(
            QLabel("Frequency for Binary 0"),
            1,
            0
        )

        parameter_layout.addWidget(
            self.freq1_slider,
            1,
            1
        )

        parameter_layout.addWidget(
            self.freq1_input,
            1,
            2
        )

        # FREQUENCY 2
        self.freq2_slider = QSlider(
            Qt.Horizontal
        )

        self.freq2_slider.setMinimum(10)

        self.freq2_slider.setMaximum(100)

        self.freq2_slider.setValue(50)

        self.freq2_input = QLineEdit("50")

        parameter_layout.addWidget(
            QLabel("Frequency for Binary 1"),
            2,
            0
        )

        parameter_layout.addWidget(
            self.freq2_slider,
            2,
            1
        )

        parameter_layout.addWidget(
            self.freq2_input,
            2,
            2
        )

        # AMPLITUDE
        self.amplitude_slider = QSlider(
            Qt.Horizontal
        )

        self.amplitude_slider.setMinimum(1)

        self.amplitude_slider.setMaximum(10)

        self.amplitude_slider.setValue(1)

        self.amplitude_input = QLineEdit("1")

        parameter_layout.addWidget(
            QLabel("Carrier Amplitude"),
            3,
            0
        )

        parameter_layout.addWidget(
            self.amplitude_slider,
            3,
            1
        )

        parameter_layout.addWidget(
            self.amplitude_input,
            3,
            2
        )

        main_layout.addLayout(
            parameter_layout
        )

        # CURSOR LABEL
        self.cursor_label = QLabel(
            "Move cursor over graphs to inspect waveform values"
        )

        self.cursor_label.setStyleSheet("""

            font-size: 12px;
            color: yellow;
            padding: 3px;

        """)

        main_layout.addWidget(
            self.cursor_label
        )

        # PLOTS
        self.binary_plot = pg.PlotWidget()

        self.f0_plot = pg.PlotWidget()

        self.fsk_plot = pg.PlotWidget()

        plots = [

            self.binary_plot,
            self.f0_plot,
            self.fsk_plot

        ]

        # STYLE ALL PLOTS
        for plot in plots:

            plot.setBackground(
                "#0d1117"
            )

            plot.showGrid(
                x=True,
                y=True,
                alpha=0.3
            )

            plot.setLabel(
                'left',
                'Amplitude'
            )

            plot.setLabel(
                'bottom',
                'Time'
            )

            plot.setMouseEnabled(
                x=True,
                y=True
            )

            plot.getViewBox().setDefaultPadding(
                0.08
            )

            plot.setMinimumHeight(170)

        # TITLES
        self.binary_plot.setTitle(
            "Binary Signal",
            color="cyan",
            size="14pt"
        )

        self.f0_plot.setTitle(
            "Carrier Signal",
            color="yellow",
            size="14pt"
        )

        self.fsk_plot.setTitle(
            "FSK Signal",
            color="lightgreen",
            size="14pt"
        )

        # ADD PLOTS
        main_layout.addWidget(
            self.binary_plot,
            stretch=1
        )

        main_layout.addWidget(
            self.f0_plot,
            stretch=1
        )

        main_layout.addWidget(
            self.fsk_plot,
            stretch=1
        )

        self.setLayout(main_layout)

        # CURVES
        self.binary_curve = self.binary_plot.plot(
            pen=pg.mkPen(
                '#00ff99',
                width=2
            )
        )

        self.f0_curve = self.f0_plot.plot(
            pen=pg.mkPen(
                '#ffff00',
                width=2
            )
        )

        self.fsk_curve = self.fsk_plot.plot(
            pen=pg.mkPen(
                '#00ffff',
                width=2
            )
        )

        # CONNECT SLIDERS
        self.bit_freq_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.freq1_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.freq2_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.amplitude_slider.valueChanged.connect(
            self.parameters_changed
        )

        # CONNECT INPUTS
        self.bit_freq_input.editingFinished.connect(
            self.update_sliders
        )

        self.freq1_input.editingFinished.connect(
            self.update_sliders
        )

        self.freq2_input.editingFinished.connect(
            self.update_sliders
        )

        self.amplitude_input.editingFinished.connect(
            self.update_sliders
        )

        # CURSOR TRACKING
        self.binary_plot.scene().sigMouseMoved.connect(
            self.binary_mouse_moved
        )

        self.f0_plot.scene().sigMouseMoved.connect(
            self.carrier_mouse_moved
        )

        self.fsk_plot.scene().sigMouseMoved.connect(
            self.fsk_mouse_moved
        )

        # INITIAL DRAW
        self.update_waveforms()

    def reset_view(self):

        amplitude = self.amplitude_slider.value()

        self.binary_plot.setXRange(
            -0.2,
            1.2
        )

        self.binary_plot.setYRange(
            -0.5,
            1.5
        )

        self.f0_plot.setXRange(
            -0.2,
            1.2
        )

        self.f0_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

        self.fsk_plot.setXRange(
            -0.2,
            1.2
        )

        self.fsk_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

    def toggle_animation(self):

        if self.is_running:

            self.pause_button.setText(
                "Resume"
            )

            self.is_running = False

        else:

            self.pause_button.setText(
                "Pause"
            )

            self.is_running = True

    def parameters_changed(self):

        self.update_inputs()

        self.update_waveforms()

    def update_inputs(self):

        self.bit_freq_input.setText(
            str(
                self.bit_freq_slider.value()
            )
        )

        self.freq1_input.setText(
            str(
                self.freq1_slider.value()
            )
        )

        self.freq2_input.setText(
            str(
                self.freq2_slider.value()
            )
        )

        self.amplitude_input.setText(
            str(
                self.amplitude_slider.value()
            )
        )

    def update_sliders(self):

        try:

            self.bit_freq_slider.setValue(
                int(
                    self.bit_freq_input.text()
                )
            )

            self.freq1_slider.setValue(
                int(
                    self.freq1_input.text()
                )
            )

            self.freq2_slider.setValue(
                int(
                    self.freq2_input.text()
                )
            )

            self.amplitude_slider.setValue(
                int(
                    self.amplitude_input.text()
                )
            )

            self.update_waveforms()

        except:

            pass

    def binary_mouse_moved(self, pos):

        vb = self.binary_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[BINARY]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def carrier_mouse_moved(self, pos):

        vb = self.f0_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[CARRIER]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def fsk_mouse_moved(self, pos):

        vb = self.fsk_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[FSK SIGNAL]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def update_waveforms(self):

        if self.is_running:

            self.phase += 0.05

        # PARAMETERS
        fb = self.bit_freq_slider.value()

        f0 = self.freq1_slider.value()

        f1 = self.freq2_slider.value()

        amplitude = self.amplitude_slider.value()

        # TIME
        t = np.linspace(
            -0.2,
            1.2,
            7000
        )

        # BINARY DATA
        binary = np.sign(
            np.sin(
                2 * np.pi * fb * t +
                self.phase
            )
        )

        binary = (binary + 1) / 2

        # CARRIER REFERENCE
        carrier = amplitude * np.cos(
            2 * np.pi * f0 * t
        )

        # FSK SIGNAL
        instantaneous_freq = np.where(
            binary == 1,
            f1,
            f0
        )

        fsk_signal = amplitude * np.cos(
            2 * np.pi * instantaneous_freq * t
        )

        # UPDATE RANGES
        self.f0_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

        self.fsk_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

        # UPDATE CURVES
        self.binary_curve.setData(
            t,
            binary
        )

        self.f0_curve.setData(
            t,
            carrier
        )

        self.fsk_curve.setData(
            t,
            fsk_signal
        )