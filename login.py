import hashlib
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QMessageBox,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
import colors
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class LoginScreen(QWidget):
    def __init__(self, switch_to_signup, switch_to_home):
        super().__init__()
        self.switch_to_signup = switch_to_signup
        self.switch_to_home = switch_to_home
        self.password_shown = False  # Default state: password hidden
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setStyleSheet(
            f"""
            background-color: {colors.color_4};
            border-radius: 10px;
            padding: 20px;
            max-width: 500px;
        """
        )
        card_layout = QVBoxLayout()

        title = QLabel("Login")
        title.setStyleSheet(
            f"color: {colors.color_3}; font-size: 28px; font-weight: bold;"
        )
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.email.setStyleSheet(
            f"background-color: {colors.color_3}; padding: 15px; font-size: 20px;"
        )
        card_layout.addWidget(self.email)

        # Password field with toggle visibility button
        password_layout = QHBoxLayout()
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)  # Default to hidden
        self.password.setStyleSheet(
            f"background-color: {colors.color_3}; padding: 15px; font-size: 20px;"
        )
        password_layout.addWidget(self.password)

        # Eye button for toggling password visibility
        self.toggle_password_button = QPushButton()
        self.toggle_password_button.setIcon(QIcon("assets/eye_closed.png"))  # Path to the closed eye icon
        self.toggle_password_button.setIconSize(self.toggle_password_button.sizeHint())
        self.toggle_password_button.setStyleSheet(
            f"""
            background-color: {colors.color_3};
            border: 2px solid {colors.color_5};
            border-radius: 5px;
            padding: 5px;
        """
        )
        self.toggle_password_button.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.toggle_password_button)

        card_layout.addLayout(password_layout)

        login_button = QPushButton("Login")
        login_button.setStyleSheet(
            f"background-color: {colors.color_1}; color: {colors.color_3}; padding: 15px; font-size: 20px;"
        )
        login_button.clicked.connect(self.handle_login)
        card_layout.addWidget(login_button)

        switch_button = QPushButton("Go to Signup")
        switch_button.setStyleSheet(
            f"background-color: {colors.color_1}; color: {colors.color_3}; padding: 15px; font-size: 20px;"
        )
        switch_button.clicked.connect(self.switch_to_signup)
        card_layout.addWidget(switch_button)

        card.setLayout(card_layout)
        layout.addWidget(card)
        self.setLayout(layout)

    def toggle_password_visibility(self):
        """Toggle password visibility."""
        if self.password_shown:
            self.password.setEchoMode(QLineEdit.Password)
            self.toggle_password_button.setIcon(QIcon("assets/eye_closed.png"))
        else:
            self.password.setEchoMode(QLineEdit.Normal)
            self.toggle_password_button.setIcon(QIcon("assets/eye_open.png"))
        self.password_shown = not self.password_shown

    def handle_login(self):
        email = self.email.text().strip()
        password = self.password.text().strip()

        if not (email and password):
            QMessageBox.warning(self, "Input Error", "Please fill in both fields.")
            return

        try:
            # Fetch user data from Supabase
            response = supabase.table("restaurants").select(
                "email, password, restaurant_name, restaurant_id"
            ).eq("email", email).execute()
            if not response.data:
                QMessageBox.warning(
                    self, "Error", "Email not found. Please sign up first."
                )
                return

            # Retrieve the stored hashed password
            stored_password = response.data[0]["password"]
            restaurant_name = response.data[0]["restaurant_name"]
            restaurant_id = response.data[0]["restaurant_id"]

            # Hash the entered password using the same method as during signup
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Compare the hashed entered password with the stored hashed password
            if hashed_password == stored_password:
                # Fetch tables for the restaurant
                tables_response = (
                    supabase.table("tables")
                    .select("table_id")
                    .eq("restaurant_id", restaurant_id)
                    .execute()
                )

                if tables_response.data is None or len(tables_response.data) == 0:
                    has_tables = False  # No tables added
                else:
                    has_tables = True  # Tables exist

                # Login success, pass restaurant info and table availability to HomeScreen
                self.switch_to_home(restaurant_name, restaurant_id, has_tables)

            else:
                QMessageBox.warning(self, "Error", "Incorrect password.")
        except Exception as e:
            QMessageBox.critical(
                self, "Database Error", f"Error during login: {str(e)}"
            )

    def clear_fields(self):
        """Clear the input fields and reset UI elements."""
        self.email.clear()
        self.password.clear()
        self.password.setEchoMode(QLineEdit.Password)  # Reset password visibility
        self.password_shown = False  # Reset password visibility state
        self.toggle_password_button.setIcon(QIcon("assets/eye_closed.png"))  # Reset icon to closed eye