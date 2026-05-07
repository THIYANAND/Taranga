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


class QAMWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("QAM Modulation")

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
        title = QLabel("QUADRATURE AMPLITUDE MODULATION")

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
            "Quadrature Amplitude Modulation combines amplitude and phase variations for data transmission."
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
            "s(t) = I cos(2πfct) + Q sin(2πfct)"
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

        # SYMBOL FREQUENCY
        self.symbol_freq_slider = QSlider(
            Qt.Horizontal
        )

        self.symbol_freq_slider.setMinimum(1)

        self.symbol_freq_slider.setMaximum(20)

        self.symbol_freq_slider.setValue(5)

        self.symbol_freq_input = QLineEdit("5")

        parameter_layout.addWidget(
            QLabel("Symbol Frequency"),
            0,
            0
        )

        parameter_layout.addWidget(
            self.symbol_freq_slider,
            0,
            1
        )

        parameter_layout.addWidget(
            self.symbol_freq_input,
            0,
            2
        )

        # CARRIER FREQUENCY
        self.carrier_freq_slider = QSlider(
            Qt.Horizontal
        )

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

        # AMPLITUDE
        self.amplitude_slider = QSlider(
            Qt.Horizontal
        )

        self.amplitude_slider.setMinimum(1)

        self.amplitude_slider.setMaximum(10)

        self.amplitude_slider.setValue(2)

        self.amplitude_input = QLineEdit("2")

        parameter_layout.addWidget(
            QLabel("Carrier Amplitude"),
            2,
            0
        )

        parameter_layout.addWidget(
            self.amplitude_slider,
            2,
            1
        )

        parameter_layout.addWidget(
            self.amplitude_input,
            2,
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
        self.i_plot = pg.PlotWidget()

        self.q_plot = pg.PlotWidget()

        self.qam_plot = pg.PlotWidget()

        plots = [

            self.i_plot,
            self.q_plot,
            self.qam_plot

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
        self.i_plot.setTitle(
            "In-Phase Component (I)",
            color="cyan",
            size="14pt"
        )

        self.q_plot.setTitle(
            "Quadrature Component (Q)",
            color="yellow",
            size="14pt"
        )

        self.qam_plot.setTitle(
            "QAM Signal",
            color="lightgreen",
            size="14pt"
        )

        # ADD PLOTS
        main_layout.addWidget(
            self.i_plot,
            stretch=1
        )

        main_layout.addWidget(
            self.q_plot,
            stretch=1
        )

        main_layout.addWidget(
            self.qam_plot,
            stretch=1
        )

        self.setLayout(main_layout)

        # CURVES
        self.i_curve = self.i_plot.plot(
            pen=pg.mkPen(
                '#00ff99',
                width=2
            )
        )

        self.q_curve = self.q_plot.plot(
            pen=pg.mkPen(
                '#ffff00',
                width=2
            )
        )

        self.qam_curve = self.qam_plot.plot(
            pen=pg.mkPen(
                '#00ffff',
                width=2
            )
        )

        # CONNECT SLIDERS
        self.symbol_freq_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.carrier_freq_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.amplitude_slider.valueChanged.connect(
            self.parameters_changed
        )

        # CONNECT INPUTS
        self.symbol_freq_input.editingFinished.connect(
            self.update_sliders
        )

        self.carrier_freq_input.editingFinished.connect(
            self.update_sliders
        )

        self.amplitude_input.editingFinished.connect(
            self.update_sliders
        )

        # CURSOR TRACKING
        self.i_plot.scene().sigMouseMoved.connect(
            self.i_mouse_moved
        )

        self.q_plot.scene().sigMouseMoved.connect(
            self.q_mouse_moved
        )

        self.qam_plot.scene().sigMouseMoved.connect(
            self.qam_mouse_moved
        )

        # INITIAL DRAW
        self.update_waveforms()

    def reset_view(self):

        amplitude = self.amplitude_slider.value()

        self.i_plot.setXRange(
            -0.2,
            1.2
        )

        self.i_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

        self.q_plot.setXRange(
            -0.2,
            1.2
        )

        self.q_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

        self.qam_plot.setXRange(
            -0.2,
            1.2
        )

        self.qam_plot.setYRange(
            -2 * amplitude - 1,
            2 * amplitude + 1
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

        self.symbol_freq_input.setText(
            str(
                self.symbol_freq_slider.value()
            )
        )

        self.carrier_freq_input.setText(
            str(
                self.carrier_freq_slider.value()
            )
        )

        self.amplitude_input.setText(
            str(
                self.amplitude_slider.value()
            )
        )

    def update_sliders(self):

        try:

            self.symbol_freq_slider.setValue(
                int(
                    self.symbol_freq_input.text()
                )
            )

            self.carrier_freq_slider.setValue(
                int(
                    self.carrier_freq_input.text()
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

    def i_mouse_moved(self, pos):

        vb = self.i_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[I COMPONENT]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def q_mouse_moved(self, pos):

        vb = self.q_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[Q COMPONENT]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def qam_mouse_moved(self, pos):

        vb = self.qam_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[QAM SIGNAL]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def update_waveforms(self):

        if self.is_running:

            self.phase += 0.05

        # PARAMETERS
        fs = self.symbol_freq_slider.value()

        fc = self.carrier_freq_slider.value()

        amplitude = self.amplitude_slider.value()

        # TIME
        t = np.linspace(
            -0.2,
            1.2,
            7000
        )

        # I COMPONENT
        i_signal = amplitude * np.sign(
            np.sin(
                2 * np.pi * fs * t +
                self.phase
            )
        )

        # Q COMPONENT
        q_signal = amplitude * np.sign(
            np.cos(
                2 * np.pi * fs * t +
                self.phase
            )
        )

        # QAM SIGNAL
        qam_signal = (

            i_signal * np.cos(
                2 * np.pi * fc * t
            )

            +

            q_signal * np.sin(
                2 * np.pi * fc * t
            )

        )

        # UPDATE RANGES
        self.i_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

        self.q_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

        self.qam_plot.setYRange(
            -2 * amplitude - 1,
            2 * amplitude + 1
        )

        # UPDATE CURVES
        self.i_curve.setData(
            t,
            i_signal
        )

        self.q_curve.setData(
            t,
            q_signal
        )

        self.qam_curve.setData(
            t,
            qam_signal
        )