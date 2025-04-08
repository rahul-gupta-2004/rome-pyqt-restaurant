from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QTabWidget, QFrame, QPushButton
from PyQt5.QtCore import Qt
import colors
from user_profile import create_profile_tab
from tables import create_table_tab
from inventory import create_inventory_tab

class HomeScreen(QWidget):
    def __init__(self, restaurant_name, restaurant_id):  # Only these two parameters should be here
        super().__init__()
        self.restaurant_name = restaurant_name
        self.restaurant_id = restaurant_id
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)

        # Header layout (Restaurant Name and Logout Button)
        header_layout = QHBoxLayout()
        header_frame = QFrame()
        header_frame.setStyleSheet(f"background-color: {colors.color_4}; padding: 10px; border-radius: 5px;")

        restaurant_label = QLabel(self.restaurant_name)
        restaurant_label.setStyleSheet(f"color: {colors.color_3}; font-size: 20px; font-weight: bold;")
        restaurant_label.setAlignment(Qt.AlignLeft)

        logout_button = QPushButton("Logout")
        logout_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3}; padding: 10px;")
        logout_button.clicked.connect(self.logout)

        header_layout.addWidget(restaurant_label)
        header_layout.addStretch()
        header_layout.addWidget(logout_button)
        header_frame.setLayout(header_layout)

        # Tab widget
        tabs = QTabWidget()
        tabs.setStyleSheet(f"background-color: {colors.color_3}; padding: 10px;")

        # Adding tabs
        tabs.addTab(create_table_tab(self.restaurant_id), "Table Management")
        tabs.addTab(create_inventory_tab(self.restaurant_id), "Inventory Management")
        tabs.addTab(create_profile_tab(self.restaurant_id), "Profile")  # Ensure restaurant_id is passed

        # Add widgets to main layout
        main_layout.addWidget(header_frame)
        main_layout.addWidget(tabs)

        self.setLayout(main_layout)
        self.setWindowTitle("Home")

    def logout(self):
        """Log out the user and navigate back to the login screen."""
        self.parentWidget().setCurrentWidget(self.parentWidget().parent().login_screen)
        self.parentWidget().parent().show_login()

    def show_home(self, restaurant_id):
        # Pass the restaurant ID after login
        self.restaurant_id = restaurant_id
        self.init_ui()
