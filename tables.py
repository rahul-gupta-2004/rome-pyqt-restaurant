from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QFileDialog
)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt
from dotenv import load_dotenv
from supabase import create_client, Client
import os
import colors
import qrcode
from io import BytesIO
import zipfile
import re

# Load environment variables
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


def create_table_tab(restaurant_id):
    class TableManagementTab(QWidget):
        def __init__(self):
            super().__init__()
            self.restaurant_id = restaurant_id
            self.setStyleSheet("background-color: white;")
            self.init_ui()
            self.load_tables()

        def init_ui(self):
            layout = QVBoxLayout()

            # Input and button layout
            input_layout = QHBoxLayout()

            self.table_number_input = QLineEdit()
            self.table_number_input.setPlaceholderText("Enter Table Number")
            self.table_number_input.setFixedHeight(45)
            input_layout.addWidget(self.table_number_input)

            add_button = QPushButton("Add Table")
            add_button.setFixedHeight(45)
            add_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3};")
            add_button.clicked.connect(self.add_table)
            input_layout.addWidget(add_button)

            download_all_button = QPushButton("Download All QR Codes")
            download_all_button.setFixedHeight(45)
            download_all_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3};")
            download_all_button.clicked.connect(self.download_all_qr_codes)
            input_layout.addWidget(download_all_button)

            layout.addLayout(input_layout)

            # Table to display the data
            self.table_widget = QTableWidget()
            self.table_widget.setColumnCount(5)
            self.table_widget.setRowCount(1)  # Start with just the custom header
            self.table_widget.setHorizontalHeaderLabels(["", "", "", "", ""])  # Remove default headers
            self.table_widget.horizontalHeader().setVisible(False)  # Hide header completely
            self.table_widget.verticalHeader().setVisible(False)  # Hide row headers

            # Spread columns evenly
            header = self.table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            # Add custom header row
            header_items = ["Table Number", "QR Code Data", "", "", ""]
            for col, header_text in enumerate(header_items):
                header_item = QTableWidgetItem(header_text)
                header_item.setTextAlignment(Qt.AlignCenter)
                header_item.setFlags(Qt.ItemIsEnabled)  # Non-editable
                header_item.setBackground(QColor(colors.color_1))
                header_item.setForeground(QColor(colors.color_3))
                self.table_widget.setItem(0, col, header_item)

            layout.addWidget(self.table_widget)
            self.setLayout(layout)

        def load_tables(self):
            """Load tables from the database."""
            response = supabase.table("tables").select("*").eq("restaurant_id", self.restaurant_id).order("table_number", desc=False).execute()
            
            tables = response.data or []
            self.table_widget.setRowCount(len(tables) + 1)

            # Add rows for tables
            for row, table in enumerate(tables, start=1):
                self.table_widget.setItem(row, 0, QTableWidgetItem(str(table["table_number"])))
                self.table_widget.setItem(row, 1, QTableWidgetItem(table["qr_code_data"]))

                # View QR Code button
                view_button = QPushButton("View QR Code")
                view_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3};")
                view_button.clicked.connect(lambda _, t=table: self.view_qr_code(t["qr_code_data"]))
                self.table_widget.setCellWidget(row, 2, view_button)

                # Download QR Code button
                download_button = QPushButton("Download QR Code")
                download_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3};")
                download_button.clicked.connect(lambda _, t=table: self.download_qr_code(t["qr_code_data"], t["table_number"]))
                self.table_widget.setCellWidget(row, 3, download_button)

                # Delete Table button
                delete_button = QPushButton("Delete Table")
                delete_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3};")
                delete_button.clicked.connect(lambda _, t=table: self.delete_table(t["table_id"], t["table_number"]))
                self.table_widget.setCellWidget(row, 4, delete_button)

        def add_table(self):
            """Add a table to the database."""
            table_number = self.table_number_input.text().strip()
            if not table_number:
                QMessageBox.warning(self, "Error", "Table Number cannot be empty.")
                return

            # Check for duplicate table number
            response = supabase.table("tables").select("table_id").eq("restaurant_id", self.restaurant_id).eq("table_number", table_number).execute()
            if response.data:
                QMessageBox.warning(self, "Error", f"Table Number {table_number} already exists.")
                return

            # Add table to the database
            base_url = "192.168.29.30:3000/"
            qr_code_data = f"{base_url}{table_number}/{restaurant_id}"
            supabase.table("tables").insert({
                "restaurant_id": self.restaurant_id,
                "table_number": table_number,
                "qr_code_data": qr_code_data
            }).execute()
            QMessageBox.information(self, "Success", "Table added successfully.")
            self.table_number_input.clear()
            self.load_tables()

        def view_qr_code(self, qr_code_data):
            """Display QR Code for a table."""
            dialog = QDialog(self)
            dialog.setWindowTitle("QR Code Viewer")
            layout = QVBoxLayout()

            qr_image = qrcode.make(qr_code_data)
            buffer = BytesIO()
            qr_image.save(buffer, format="PNG")
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            label = QLabel()
            label.setPixmap(pixmap)
            layout.addWidget(label)

            dialog.setLayout(layout)
            dialog.exec_()

        def download_qr_code(self, qr_code_data, table_number):
            """Download the QR code for the specific table."""
            qr_image = qrcode.make(qr_code_data)

            # Replace invalid filename characters
            safe_qr_code_data = re.sub(r'[<>:"/\\|?*]', '_', qr_code_data)

            filename = f"Table Number - {table_number}.png"
            qr_image.save(filename)

            QMessageBox.information(self, "Success", "QR Code downloaded successfully.")

        def delete_table(self, table_id, table_number):
            """Delete a table from the database with confirmation."""
            confirmation = QMessageBox.question(
                self, "Confirm Deletion",
                f"Are you sure you want to delete Table {table_number}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirmation == QMessageBox.Yes:
                supabase.table("tables").delete().eq("table_id", table_id).execute()
                QMessageBox.information(self, "Success", f"Table {table_number} deleted successfully.")
                self.load_tables()

        def download_all_qr_codes(self):
            """Download all QR Codes as a ZIP file."""
            response = supabase.table("tables").select("*").eq("restaurant_id", self.restaurant_id).order("table_number").execute()
            if not response.data:
                QMessageBox.warning(self, "Error", "No tables to download.")
                return

            # Create an in-memory ZIP file
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for table in response.data:
                    qr_image = qrcode.make(table["qr_code_data"])
                    qr_buffer = BytesIO()
                    qr_image.save(qr_buffer, format="PNG")
                    qr_buffer.seek(0)

                    # Add the QR code to the ZIP file
                    qr_filename = f"Table_{table['table_number']}.png"
                    zip_file.writestr(qr_filename, qr_buffer.getvalue())

            # Write the ZIP file to the user's chosen location
            zip_buffer.seek(0)
            save_path, _ = QFileDialog.getSaveFileName(self, "Save QR Codes ZIP", "qr_codes.zip", "ZIP files (*.zip)")
            if save_path:
                with open(save_path, "wb") as f:
                    f.write(zip_buffer.getvalue())
                QMessageBox.information(self, "Success", f"QR Codes saved as {save_path}.")

    return TableManagementTab()