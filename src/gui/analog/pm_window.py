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


class PMWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("PM Modulation")

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
        title = QLabel("PHASE MODULATION")

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
            "Phase Modulation varies carrier phase according to message signal."
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
            "s(t) = Ac cos(2πfct + kp m(t))"
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

        # PHASE DEVIATION
        self.phase_dev_slider = QSlider(
            Qt.Horizontal
        )

        self.phase_dev_slider.setMinimum(1)

        self.phase_dev_slider.setMaximum(100)

        self.phase_dev_slider.setValue(50)

        self.phase_dev_input = QLineEdit("5")

        parameter_layout.addWidget(
            QLabel("Phase Deviation"),
            2,
            0
        )

        parameter_layout.addWidget(
            self.phase_dev_slider,
            2,
            1
        )

        parameter_layout.addWidget(
            self.phase_dev_input,
            2,
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

        self.carrier_plot = pg.PlotWidget()

        self.pm_plot = pg.PlotWidget()

        plots = [

            self.message_plot,
            self.carrier_plot,
            self.pm_plot

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

        self.carrier_plot.setTitle(
            "Carrier Signal",
            color="yellow",
            size="14pt"
        )

        self.pm_plot.setTitle(
            "PM Signal",
            color="lightgreen",
            size="14pt"
        )

        # ADD PLOTS
        main_layout.addWidget(
            self.message_plot,
            stretch=1
        )

        main_layout.addWidget(
            self.carrier_plot,
            stretch=1
        )

        main_layout.addWidget(
            self.pm_plot,
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

        self.carrier_curve = self.carrier_plot.plot(
            pen=pg.mkPen(
                '#ffff00',
                width=2
            )
        )

        self.pm_curve = self.pm_plot.plot(
            pen=pg.mkPen(
                '#00ffff',
                width=2
            )
        )

        # CONNECT SLIDERS
        self.msg_freq_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.carrier_freq_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.phase_dev_slider.valueChanged.connect(
            self.parameters_changed
        )

        self.msg_amp_slider.valueChanged.connect(
            self.parameters_changed
        )

        # CONNECT INPUTS
        self.msg_freq_input.editingFinished.connect(
            self.update_sliders
        )

        self.carrier_freq_input.editingFinished.connect(
            self.update_sliders
        )

        self.phase_dev_input.editingFinished.connect(
            self.update_sliders
        )

        self.msg_amp_input.editingFinished.connect(
            self.update_sliders
        )

        # CURSOR TRACKING
        self.message_plot.scene().sigMouseMoved.connect(
            self.message_mouse_moved
        )

        self.carrier_plot.scene().sigMouseMoved.connect(
            self.carrier_mouse_moved
        )

        self.pm_plot.scene().sigMouseMoved.connect(
            self.pm_mouse_moved
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

        self.carrier_plot.setXRange(
            -0.2,
            1.2
        )

        self.carrier_plot.setYRange(
            -1.5,
            1.5
        )

        self.pm_plot.setXRange(
            -0.2,
            1.2
        )

        self.pm_plot.setYRange(
            -1.5,
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

        self.carrier_freq_input.setText(
            str(
                self.carrier_freq_slider.value()
            )
        )

        self.phase_dev_input.setText(
            str(
                self.phase_dev_slider.value() / 10
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

            self.carrier_freq_slider.setValue(
                int(
                    self.carrier_freq_input.text()
                )
            )

            self.phase_dev_slider.setValue(
                int(
                    float(
                        self.phase_dev_input.text()
                    ) * 10
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

    def carrier_mouse_moved(self, pos):

        vb = self.carrier_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[CARRIER]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def pm_mouse_moved(self, pos):

        vb = self.pm_plot.plotItem.vb

        point = vb.mapSceneToView(pos)

        self.cursor_label.setText(

            f"[PM SIGNAL]   Time: {point.x():.4f} s    Amplitude: {point.y():.4f}"

        )

    def update_waveforms(self):

        if self.is_running:

            self.phase += 0.1

        # PARAMETERS
        fm = self.msg_freq_slider.value()

        fc = self.carrier_freq_slider.value()

        kp = self.phase_dev_slider.value() / 10

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

        # CARRIER SIGNAL
        carrier = np.cos(

            2 * np.pi * fc * t

        )

        # PM SIGNAL
        pm_signal = np.cos(

            2 * np.pi * fc * t +

            kp * message

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

        self.carrier_curve.setData(
            t,
            carrier
        )

        self.pm_curve.setData(
            t,
            pm_signal
        )