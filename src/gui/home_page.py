from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSizePolicy
)

from PySide6.QtCore import Qt


class HomePage(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        # MAIN WINDOW STYLE
        self.setStyleSheet("""

            QWidget {

                background-color: #111111;
                color: white;
                font-family: Segoe UI;

            }

        """)

        # MAIN LAYOUT
        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            35,
            25,
            35,
            20
        )

        main_layout.setSpacing(18)

        # =====================================================
        # HEADER
        # =====================================================

        header_frame = QFrame()

        header_frame.setStyleSheet("""

            QFrame {

                background-color: #181818;
                border-radius: 15px;
                border: 1px solid #2f2f2f;

            }

        """)

        header_layout = QVBoxLayout()

        header_layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        header_layout.setSpacing(8)

        title = QLabel("TARANGA")

        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""

            font-size: 44px;
            font-weight: bold;
            color: #00d9ff;

        """)

        subtitle = QLabel(
            "Interactive Modulation and Demodulation Visualizer"
        )

        subtitle.setAlignment(Qt.AlignCenter)

        subtitle.setStyleSheet("""

            font-size: 18px;
            color: #d0d0d0;

        """)

        line = QLabel(
            "Analog • Digital • Pulse Communication Systems"
        )

        line.setAlignment(Qt.AlignCenter)

        line.setStyleSheet("""

            font-size: 14px;
            color: #9a9a9a;

        """)

        header_layout.addWidget(title)

        header_layout.addWidget(subtitle)

        header_layout.addWidget(line)

        header_frame.setLayout(header_layout)

        main_layout.addWidget(header_frame)

        # =====================================================
        # CENTER SECTION
        # =====================================================

        center_layout = QHBoxLayout()

        center_layout.setSpacing(18)

        # =====================================================
        # ABOUT CARD
        # =====================================================

        about_card = QFrame()

        about_card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        about_card.setStyleSheet("""

            QFrame {

                background-color: #181818;
                border-radius: 15px;
                border: 1px solid #2f2f2f;

            }

        """)

        about_layout = QVBoxLayout()

        about_layout.setContentsMargins(
            22,
            20,
            22,
            20
        )

        about_layout.setSpacing(15)

        about_title = QLabel(
            "About Software"
        )

        about_title.setAlignment(Qt.AlignCenter)

        about_title.setStyleSheet("""

            font-size: 24px;
            font-weight: bold;
            color: #00d9ff;

        """)

        about_text = QLabel(

            "TARANGA is an interactive communication "
            "systems visualization platform developed "
            "for understanding modulation and demodulation techniques.\n\n"

            "Features:\n\n"

            "• Real-time waveform generation\n"
            "• Interactive parameter control\n"
            "• Signal visualization\n"
            "• Dynamic waveform animation\n"
            "• Analog modulation analysis\n"
            "• Digital modulation analysis\n"
            "• Pulse modulation analysis\n\n"

            "Modules:\n"
            "AM • FM • PM • ASK • FSK • PSK • QAM • PWM • PPM"

        )

        about_text.setWordWrap(True)

        about_text.setAlignment(Qt.AlignTop)

        about_text.setStyleSheet("""

            font-size: 15px;
            line-height: 1.5;
            color: #f0f0f0;

        """)

        about_layout.addWidget(about_title)

        about_layout.addWidget(about_text)

        about_card.setLayout(about_layout)

        # =====================================================
        # DEVELOPER CARD
        # =====================================================

        developer_card = QFrame()

        developer_card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        developer_card.setStyleSheet("""

            QFrame {

                background-color: #181818;
                border-radius: 15px;
                border: 1px solid #2f2f2f;

            }

        """)

        developer_layout = QVBoxLayout()

        developer_layout.setContentsMargins(
            22,
            20,
            22,
            20
        )

        developer_layout.setSpacing(14)

        developer_title = QLabel(
            "Developed By"
        )

        developer_title.setAlignment(Qt.AlignCenter)

        developer_title.setStyleSheet("""

            font-size: 24px;
            font-weight: bold;
            color: #00d9ff;

        """)

        names = QLabel(
            "Chaithanya & Thiyanand M"
        )

        names.setAlignment(Qt.AlignCenter)

        names.setStyleSheet("""

            font-size: 22px;
            font-weight: bold;
            color: white;

        """)

        department = QLabel(

            "Department of Electronics and\n"
            "Communication Engineering\n\n"

            "3rd Year • 6th Semester"

        )

        department.setAlignment(Qt.AlignCenter)

        department.setStyleSheet("""

            font-size: 16px;
            color: #d0d0d0;
            line-height: 1.5;

        """)

        college = QLabel(

            "Vivekananda College of\n"
            "Engineering and Technology\n\n"

            "Puttur - 574203"

        )

        college.setAlignment(Qt.AlignCenter)

        college.setStyleSheet("""

            font-size: 16px;
            color: white;
            line-height: 1.5;

        """)

        contacts_title = QLabel(
            "Contact Information"
        )

        contacts_title.setAlignment(Qt.AlignCenter)

        contacts_title.setStyleSheet("""

            font-size: 18px;
            font-weight: bold;
            color: #00d9ff;

        """)

        contacts = QLabel(

            "thiyanandm@gmail.com\n"
            "chaitu.puttur@gmail.com"

        )

        contacts.setAlignment(Qt.AlignCenter)

        contacts.setStyleSheet("""

            font-size: 15px;
            color: #f0f0f0;
            line-height: 1.7;

        """)

        developer_layout.addWidget(developer_title)

        developer_layout.addWidget(names)

        developer_layout.addWidget(department)

        developer_layout.addWidget(college)

        developer_layout.addWidget(contacts_title)

        developer_layout.addWidget(contacts)

        developer_card.setLayout(developer_layout)

        # ADD BOTH CARDS
        center_layout.addWidget(about_card)

        center_layout.addWidget(developer_card)

        main_layout.addLayout(center_layout)

        # =====================================================
        # FOOTER
        # =====================================================

        footer = QLabel(
            "TARANGA © 2026 | Communication Systems Visualization Platform"
        )

        footer.setAlignment(Qt.AlignCenter)

        footer.setStyleSheet("""

            font-size: 13px;
            color: #808080;
            padding-top: 4px;

        """)

        main_layout.addWidget(footer)

        self.setLayout(main_layout)