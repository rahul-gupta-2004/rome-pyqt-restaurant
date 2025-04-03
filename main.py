from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QIcon
from splash_screen import SplashScreen
from login import LoginScreen
from signup import SignupScreen
from home import HomeScreen
import sys
import colors

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("R.O.M.E - Restaurant Orders Made Easy Desktop Application")
        self.setGeometry(0, 0, 1920, 1080)
        self.setStyleSheet(f"background-color: {colors.color_3};")
        self.setWindowIcon(QIcon("assets/logo.png"))

        # Create the stacked widget to manage screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create instances of screens
        self.splash_screen = SplashScreen(self.show_login)
        self.login_screen = LoginScreen(self.show_signup, self.login_success)  # Pass the login_success callback
        self.signup_screen = SignupScreen(self.show_login)

        # Add screens to the stacked widget
        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.signup_screen)

        # Show the splash screen
        self.stacked_widget.setCurrentWidget(self.splash_screen)

    def show_login(self):
        self.login_screen.clear_fields()  # Clear input fields
        self.stacked_widget.setCurrentWidget(self.login_screen)

    def show_signup(self):
        self.stacked_widget.setCurrentWidget(self.signup_screen)

    def login_success(self, restaurant_name, restaurant_id, has_tables):
        """
        Callback for successful login.
        Switches to HomeScreen and passes the restaurant_name, restaurant_id, and has_tables.
        """
        # Make sure only three arguments are passed when calling this method
        self.home_screen = HomeScreen(restaurant_name=restaurant_name, restaurant_id=restaurant_id)  # Pass has_tables if needed
        self.stacked_widget.addWidget(self.home_screen)
        self.stacked_widget.setCurrentWidget(self.home_screen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())