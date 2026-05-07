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


class PWMWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("PWM Modulation")

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
        title = QLabel("PULSE WIDTH MODULATION")

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
            "Pulse Width Modulation changes pulse width according to message signal amplitude."
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
            "Pulse Width ∝ Message Signal Amplitude"
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

        # MESSAGE FREQUENCY
        self.msg_freq_slider = QSlider(
            Qt.Horizontal
        )

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

        # PULSE FREQUENCY
        self.pulse_freq_slider = QSlider(
            Qt.Horizontal
        )

        self.pulse_freq_slider.setMinimum(5)

        self.pulse_freq_slider.setMaximum(50)

        self.pulse_freq_slider.setValue(20)

        self.pulse_freq_input = QLineEdit("20")

        parameter_layout.addWidget(
            QLabel("Pulse Frequency"),
            1,
            0
        )

        parameter_layout.addWidget(
            self.pulse_freq_slider,
            1,
            1
        )

        parameter_layout.addWidget(
            self.pulse_freq_input,
            1,
            2
        )

        # MESSAGE AMPLITUDE
        self.msg_amp_slider = QSlider(
            Qt.Horizontal
        )

        self.msg_amp_slider.setMinimum(1)

        self.msg_amp_slider.setMaximum(10)

        self.msg_amp_slider.setValue(1)

        self.msg_amp_input = QLineEdit("1")

        parameter_layout.addWidget(
            QLabel("Message Amplitude"),
            2,
            0
        )

        parameter_layout.addWidget(
            self.msg_amp_slider,
            2,
            1
        )

        parameter_layout.addWidget(
            self.msg_amp_input,
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
        self.message_plot = pg.PlotWidget()

        self.sawtooth_plot = pg.PlotWidget()

        self.pwm_plot = pg.PlotWidget()

        plots = [

            self.message_plot,
            self.sawtooth_plot,
            self.pwm_plot

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
        self.message_plot.setTitle(
            "Message Signal",
            color="cyan",
            size="14pt"
        )

        self.sawtooth_plot.setTitle(
            "Reference Sawtooth Signal",
            color="yellow",
            size="14pt"
        )

        self.pwm_plot.setTitle(
            "PWM Signal",
            color="lightgreen",
            size="14pt"
        )

        # ADD PLOTS
        main_layout.addWidget(
            self.message_plot,
            stretch=1
        )

        main_layout.addWidget(
            self.sawtooth_plot,
            stretch=1
        )

        main_layout.addWidget(
            self.pwm_plot,
            stretch=1
        )

        self.setLayout(main_layout)

        # CURVES
        self.message_curve = self.message_plot.plot(
            pen=pg.mkPen(
                '#00ff99',
                width=2
            )
        )

        self.sawtooth_curve = self.sawtooth_plot.plot(
            pen=pg.mkPen(
                '#ffff00',
                width=2
            )
        )

        self.pwm_curve = self.pwm_plot.plot(
            pen=pg.mkPen(
                '#00ffff',
                width=2
            )
        )

        # CONNECT SLIDERS
        self.msg_freq_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.pulse_freq_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.msg_amp_slider.valueChanged.connect(
            self.parameters_changed
        )

        # CONNECT INPUTS
        self.msg_freq_input.editingFinished.connect(
            self.update_sliders
        )

        self.pulse_freq_input.editingFinished.connect(
            self.update_sliders
        )

        self.msg_amp_input.editingFinished.connect(
            self.update_sliders
        )

        # CURSOR TRACKING
        self.message_plot.scene().sigMouseMoved.connect(
            self.message_mouse_moved
        )

        self.sawtooth_plot.scene().sigMouseMoved.connect(
            self.sawtooth_mouse_moved
        )

        self.pwm_plot.scene().sigMouseMoved.connect(
            self.pwm_mouse_moved
        )

        # INITIAL DRAW
        self.update_waveforms()

    def reset_view(self):

        amplitude = self.msg_amp_slider.value()

        self.message_plot.setXRange(
            -0.2,
            1.2
        )

        self.message_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

        self.sawtooth_plot.setXRange(
            -0.2,
            1.2
        )

        self.sawtooth_plot.setYRange(
            -1.5,
            1.5
        )

        self.pwm_plot.setXRange(
            -0.2,
            1.2
        )

        self.pwm_plot.setYRange(
            -0.5,
            1.5
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

        self.msg_freq_input.setText(
            str(
                self.msg_freq_slider.value()
            )
        )

        self.pulse_freq_input.setText(
            str(
                self.pulse_freq_slider.value()
            )
        )

        self.msg_amp_input.setText(
            str(
                self.msg_amp_slider.value()
            )
        )

    def update_sliders(self):

        try:

            self.msg_freq_slider.setValue(
                int(
                    self.msg_freq_input.text()
                )
            )

            self.pulse_freq_slider.setValue(
                int(
                    self.pulse_freq_input.text()
                )
            )

            self.msg_amp_slider.setValue(
                int(
                    self.msg_amp_input.text()
                )
            )

            self.update_waveforms()

        except:

            pass

    def message_mouse_moved(self, pos):

        vb = self.message_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[MESSAGE]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def sawtooth_mouse_moved(self, pos):

        vb = self.sawtooth_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[SAWTOOTH]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def pwm_mouse_moved(self, pos):

        vb = self.pwm_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[PWM SIGNAL]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def update_waveforms(self):

        if self.is_running:

            self.phase += 0.05

        # PARAMETERS
        fm = self.msg_freq_slider.value()

        fp = self.pulse_freq_slider.value()

        amplitude = self.msg_amp_slider.value()

        # TIME
        t = np.linspace(
            -0.2,
            1.2,
            7000
        )

        # MESSAGE SIGNAL
        message = amplitude * np.sin(
            2 * np.pi * fm * t +
            self.phase
        )

        # SAWTOOTH SIGNAL
        sawtooth = 2 * (
            (fp * t) % 1
        ) - 1

        # NORMALIZE MESSAGE
        normalized_message = message / (
            amplitude + 0.001
        )

        # PWM SIGNAL
        pwm_signal = np.where(
            normalized_message > sawtooth,
            1,
            0
        )

        # UPDATE RANGES
        self.message_plot.setYRange(
            -amplitude - 1,
            amplitude + 1
        )

        # UPDATE CURVES
        self.message_curve.setData(
            t,
            message
        )

        self.sawtooth_curve.setData(
            t,
            sawtooth
        )

        self.pwm_curve.setData(
            t,
            pwm_signal
        )