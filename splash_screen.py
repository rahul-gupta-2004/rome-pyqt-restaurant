from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
import colors

class SplashScreen(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.init_ui()

    def init_ui(self):
        # Layout for the splash screen
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Welcome text
        self.welcome_text = QLabel("Welcome to R.O.M.E. - Restaurant Orders Made Easy")
        self.welcome_text.setStyleSheet(f"color: {colors.color_1}; font-size: 32px; font-weight: bold; padding: 15px;")
        self.welcome_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.welcome_text)

        # Add a logo
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("assets/logo.png"))
        self.logo.setStyleSheet("padding: 15px;")
        self.logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo)

        # Add a progress bar for loading animation
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid {colors.color_5};
                background-color: {colors.color_5};
                border-radius: 5px;
                text-align: center;
                font-size: 18px;
                color: {colors.color_3};
                margin: 15px;
            }}
            QProgressBar::chunk {{
                background-color: {colors.color_1};
                width: 20px;
            }}
        """)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Set layout and start loading animation
        self.setLayout(layout)
        self.start_loading()

    def start_loading(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)

    def update_progress(self):
        value = self.progress_bar.value()
        if value < 100:
            self.progress_bar.setValue(value + 1)
        else:
            self.timer.stop()
            self.switch_to_login()
