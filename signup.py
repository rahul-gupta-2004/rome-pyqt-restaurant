import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFrame, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import colors
import hashlib
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class SignupScreen(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.switch_to_login = switch_to_login
        self.password_shown = False
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Card
        card = QFrame()
        card.setStyleSheet(f"""
            background-color: {colors.color_4};
            border-radius: 10px;
            padding: 20px;
            max-width: 500px;
        """)
        card_layout = QVBoxLayout()

        # Title
        title = QLabel("Signup")
        title.setStyleSheet(f"color: {colors.color_3}; font-size: 32px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Input fields
        self.restaurant_name = QLineEdit()
        self.restaurant_name.setPlaceholderText("Restaurant Name")
        self.restaurant_name.setStyleSheet(f"background-color: {colors.color_3}; padding: 15px; font-size: 20px;")
        card_layout.addWidget(self.restaurant_name)

        self.address = QLineEdit()
        self.address.setPlaceholderText("Address")
        self.address.setStyleSheet(f"background-color: {colors.color_3}; padding: 15px; font-size: 20px;")
        card_layout.addWidget(self.address)

        self.contact = QLineEdit()
        self.contact.setPlaceholderText("Contact Number")
        self.contact.setStyleSheet(f"background-color: {colors.color_3}; padding: 15px; font-size: 20px;")
        card_layout.addWidget(self.contact)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.email.setStyleSheet(f"background-color: {colors.color_3}; padding: 15px; font-size: 20px;")
        card_layout.addWidget(self.email)

        # Password field with toggle visibility button
        password_layout = QHBoxLayout()
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet(f"background-color: {colors.color_3}; padding: 15px; font-size: 20px;")
        password_layout.addWidget(self.password)

        # Eye button for toggling password visibility
        self.toggle_password_button = QPushButton()
        self.toggle_password_button.setIcon(QIcon("assets/eye_closed.png"))  
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

        # Buttons
        signup_button = QPushButton("Signup")
        signup_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3}; padding: 15px; font-size: 20px;")
        signup_button.clicked.connect(self.handle_signup)
        card_layout.addWidget(signup_button)

        switch_button = QPushButton("Go to Login")
        switch_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3}; padding: 15px; font-size: 20px;")
        switch_button.clicked.connect(self.switch_to_login)
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

    def handle_signup(self):
        # Fetch input values
        restaurant_name = self.restaurant_name.text().strip()
        address = self.address.text().strip()
        contact = self.contact.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Regex patterns
        contact_pattern = r"^\d{10}$"
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        # Validation
        if not (restaurant_name and address and contact and email and password):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        if not re.match(contact_pattern, contact):
            QMessageBox.warning(self, "Input Error", "Contact number must be 10 digits.")
            return

        if not re.match(email_pattern, email):
            QMessageBox.warning(self, "Input Error", "Please enter a valid email address.")
            return

        # Check if email already exists in the database
        try:
            response = supabase.table("restaurants").select("email").eq("email", email).execute()
            if response.data:
                QMessageBox.warning(self, "Error", "This email is already registered.")
                return
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error checking email existence: {str(e)}")
            return

        # Insert new restaurant into the database
        try:
            supabase.table("restaurants").insert({
                "restaurant_name": restaurant_name,
                "address": address,
                "contact": contact,
                "email": email,
                "password": hashed_password
            }).execute()
            QMessageBox.information(self, "Success", "Signup successful! You can now login.")
            self.switch_to_login()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error creating account: {str(e)}")