from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from supabase import create_client, Client
import hashlib
import os
from dotenv import load_dotenv
import colors

# Load environment variables
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def create_profile_tab(restaurant_id):
    class ProfileTab(QWidget):
        def __init__(self, restaurant_id):
            super().__init__()
            self.restaurant_id = restaurant_id
            self.init_ui()
            self.load_profile()

        def init_ui(self):
            layout = QVBoxLayout()

            # Card
            card = QFrame()
            card_layout = QVBoxLayout()

            # Form layout
            form_layout = QVBoxLayout()

            # Name
            name_layout = QHBoxLayout()
            self.name_label = QLabel("Name:")
            self.name_label.setStyleSheet(f"color: {colors.color_1}; font-size: 20px;")
            self.name_input = QLineEdit()
            self.name_input.setStyleSheet("font-size: 20px;")
            name_layout.addWidget(self.name_label)
            name_layout.addWidget(self.name_input)
            form_layout.addLayout(name_layout)

            # Address
            address_layout = QHBoxLayout()
            self.address_label = QLabel("Address:")
            self.address_label.setStyleSheet(f"color: {colors.color_1}; font-size: 20px;")
            self.address_input = QLineEdit()
            self.address_input.setStyleSheet("font-size: 20px;")
            address_layout.addWidget(self.address_label)
            address_layout.addWidget(self.address_input)
            form_layout.addLayout(address_layout)

            # Contact
            contact_layout = QHBoxLayout()
            self.contact_label = QLabel("Contact:")
            self.contact_label.setStyleSheet(f"color: {colors.color_1}; font-size: 20px;")
            self.contact_input = QLineEdit()
            self.contact_input.setStyleSheet("font-size: 20px;")
            contact_layout.addWidget(self.contact_label)
            contact_layout.addWidget(self.contact_input)
            form_layout.addLayout(contact_layout)

            # Update Button
            update_button = QPushButton("Update Profile")
            update_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3}; padding: 10px; font-size: 20px;")
            update_button.clicked.connect(self.update_profile)
            form_layout.addWidget(update_button)

            card.setLayout(form_layout)
            layout.addWidget(card)
            self.setLayout(layout)

        def load_profile(self):
            """Load restaurant profile data from the database"""
            try:
                response = supabase.table("restaurants").select("*").eq("restaurant_id", self.restaurant_id).execute()
                if response.data:
                    restaurant = response.data[0]
                    self.name_input.setText(restaurant["restaurant_name"])
                    self.address_input.setText(restaurant["address"])
                    self.contact_input.setText(restaurant["contact"])
                else:
                    print("No data found for the given restaurant_id")
            except Exception as e:
                print(f"Error loading profile: {str(e)}")

        def update_profile(self):
            """Update restaurant profile data in the database"""
            try:
                name = self.name_input.text().strip()
                address = self.address_input.text().strip()
                contact = self.contact_input.text().strip()

                updated_data = {
                    "restaurant_name": name,
                    "address": address,
                    "contact": contact,
                }

                supabase.table("restaurants").update(updated_data).eq("restaurant_id", self.restaurant_id).execute()
                QMessageBox.information(self, "Success", "Profile updated successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update profile: {str(e)}")

    return ProfileTab(restaurant_id)