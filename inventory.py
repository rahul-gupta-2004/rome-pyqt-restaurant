from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
    QPushButton, QLineEdit, QHBoxLayout, QComboBox, QMessageBox, QDialog, QLabel
)
from PyQt5.QtGui import QColor, QDoubleValidator
from PyQt5.QtCore import Qt
from supabase import create_client, Client
import colors
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def create_inventory_tab(restaurant_id):
    class InventoryTab(QWidget):
        def __init__(self):
            super().__init__()
            self.restaurant_id = restaurant_id
            self.setStyleSheet("background-color: white;")
            self.init_ui()
            self.load_inventory()

        def init_ui(self):
            layout = QVBoxLayout()
            
            # Search Bar
            search_layout = QHBoxLayout()
            self.search_bar = QLineEdit()
            self.search_bar.setPlaceholderText("Find an item by name...")
            self.search_bar.textChanged.connect(self.filter_inventory)
            search_layout.addWidget(self.search_bar)
            layout.addLayout(search_layout)
            
            # Form layout
            form_layout = QHBoxLayout()
            
            self.is_veg_dropdown = QComboBox()
            self.is_veg_dropdown.addItems(["Veg", "Non-Veg", "Egg"])
            form_layout.addWidget(self.is_veg_dropdown)
            
            self.item_name_input = QLineEdit()
            self.item_name_input.setPlaceholderText("Item Name")
            form_layout.addWidget(self.item_name_input)
            
            self.item_desc_input = QLineEdit()
            self.item_desc_input.setPlaceholderText("Item Description")
            form_layout.addWidget(self.item_desc_input)
            
            self.price_input = QLineEdit()
            self.price_input.setPlaceholderText("Price")
            self.price_input.setValidator(QDoubleValidator(0.00, 99999.99, 2))  # Allow only numbers
            form_layout.addWidget(self.price_input)
            
            self.category_dropdown = QComboBox()
            self.load_categories()
            form_layout.addWidget(self.category_dropdown)
            
            add_button = QPushButton("Add Item")
            add_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3}; border-radius: 5px; padding: 5px;")
            add_button.clicked.connect(self.add_item)
            form_layout.addWidget(add_button)

            layout.addLayout(form_layout)
            
            # Table setup
            self.table_widget = QTableWidget()
            self.table_widget.setColumnCount(8)  # Changed from 9 to 8
            self.table_widget.setRowCount(1)
            self.table_widget.setHorizontalHeaderLabels(["", "", "", "", "", "", "", ""])
            self.table_widget.horizontalHeader().setVisible(False)
            self.table_widget.verticalHeader().setVisible(False)
            
            header = self.table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            
            header_items = ["Sr. No.", "Category", "Veg", "Item Name", "Item Description", "Price (₹)", "Update", "Delete"]
            for col, header_text in enumerate(header_items):
                header_item = QTableWidgetItem(header_text)
                header_item.setTextAlignment(Qt.AlignCenter)
                header_item.setFlags(Qt.ItemIsEnabled)
                header_item.setBackground(QColor(colors.color_1))
                header_item.setForeground(QColor(colors.color_3))
                self.table_widget.setItem(0, col, header_item)
            
            layout.addWidget(self.table_widget)
            self.setLayout(layout)
        
        def load_categories(self):
            """Load categories from the database"""
            response = supabase.table("categories").select("category_id", "category_name").order("category_id", desc=False).execute()
            categories = response.data or []
            self.category_dropdown.clear()
            for category in categories:
                self.category_dropdown.addItem(category["category_name"], category["category_id"])
        
        def load_inventory(self):
            """Load inventory items from the database"""
            response = supabase.table("inventory").select("*", "categories(category_name)")\
                .eq("restaurant_id", self.restaurant_id)\
                .order("category_id", desc=False)\
                .order("is_veg", desc=True)\
                .execute()
            
            # Store the fetched inventory in a class attribute
            self.inventory_items = response.data or []  # Store inventory data for filtering
            
            self.table_widget.setRowCount(len(self.inventory_items) + 1)
            
            for row, item in enumerate(self.inventory_items, start=1):
                self.table_widget.setItem(row, 0, QTableWidgetItem(str(row)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(item.get("categories", {}).get("category_name", "Unknown")))
                self.table_widget.setItem(row, 2, QTableWidgetItem(item.get("is_veg", "Unknown")))
                self.table_widget.setItem(row, 3, QTableWidgetItem(item.get("item_name", "Unknown")))
                self.table_widget.setItem(row, 4, QTableWidgetItem(item.get("item_desc", "Unknown")))
                self.table_widget.setItem(row, 5, QTableWidgetItem(f"₹{item.get('price', 0):.2f}"))

                update_button = QPushButton("Update")
                update_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3}; border-radius: 5px; padding: 5px;")
                update_button.clicked.connect(lambda _, i=item: self.show_update_dialog(i))
                self.table_widget.setCellWidget(row, 6, update_button)  # Changed from 7 to 6

                delete_button = QPushButton("Delete")
                delete_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3}; border-radius: 5px; padding: 5px;")
                delete_button.clicked.connect(lambda _, i=item: self.delete_item(i))
                self.table_widget.setCellWidget(row, 7, delete_button)  # Changed from 8 to 7
        
        def display_inventory(self, items):
            """Display filtered inventory items in the table"""
            self.table_widget.setRowCount(len(items) + 1)
            
            for row, item in enumerate(items, start=1):
                self.table_widget.setItem(row, 0, QTableWidgetItem(str(row)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(item.get("categories", {}).get("category_name", "Unknown")))
                self.table_widget.setItem(row, 2, QTableWidgetItem(item.get("is_veg", "Unknown")))
                self.table_widget.setItem(row, 3, QTableWidgetItem(item.get("item_name", "Unknown")))
                self.table_widget.setItem(row, 4, QTableWidgetItem(item.get("item_desc", "Unknown")))
                self.table_widget.setItem(row, 5, QTableWidgetItem(f"₹{item.get('price', 0):.2f}"))
                
                update_button = QPushButton("Update")
                update_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3}; border-radius: 5px; padding: 5px;")
                update_button.clicked.connect(lambda _, i=item: self.show_update_dialog(i))
                self.table_widget.setCellWidget(row, 6, update_button)  # Changed from 7 to 6
                
                delete_button = QPushButton("Delete")
                delete_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3}; border-radius: 5px; padding: 5px;")
                delete_button.clicked.connect(lambda _, i=item: self.delete_item(i))
                self.table_widget.setCellWidget(row, 7, delete_button)  # Changed from 8 to 7
               
        def filter_inventory(self):
            """Filter inventory items based on search query"""
            search_text = self.search_bar.text().strip().lower()
            if not search_text:
                self.display_inventory(self.inventory_items)  # Show all if search is empty
                return
            
            filtered_items = [
                item for item in self.inventory_items
                if search_text in item.get("item_name", "").lower()
            ]
            self.display_inventory(filtered_items)
        
        def add_item(self):
            """Add a new item to the inventory"""
            try:
                item_name = self.item_name_input.text().strip()
                item_desc = self.item_desc_input.text().strip()
                price_text = self.price_input.text().strip()

                if not item_name or not price_text:
                    QMessageBox.warning(self, "Warning", "Please fill in all required fields!")
                    return
                
                item_data = {
                    "restaurant_id": self.restaurant_id,
                    "category_id": self.category_dropdown.currentData(),
                    "is_veg": self.is_veg_dropdown.currentText(),
                    "item_name": item_name,
                    "item_desc": item_desc,
                    "price": float(price_text),
                }
                
                supabase.table("inventory").insert(item_data).execute()
                self.load_inventory()
                QMessageBox.information(self, "Success", "Item added successfully!")

                # Clear input fields after adding item
                self.is_veg_dropdown.setCurrentIndex(0)
                self.item_name_input.clear()
                self.item_desc_input.clear()
                self.price_input.clear()
                self.category_dropdown.setCurrentIndex(0)

            except ValueError:
                QMessageBox.critical(self, "Error", "Price must be valid numbers!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add item: {str(e)}")

        def show_update_dialog(self, item):
            """Show dialog to update item details"""
            dialog = QDialog(self)
            dialog.setWindowTitle("Update Item")
            dialog.setFixedWidth(500)

            layout = QVBoxLayout()

            # Veg/Non-Veg Dropdown
            is_veg_dropdown = QComboBox()
            is_veg_dropdown.addItems(["Veg", "Non-Veg", "Egg"])
            is_veg_dropdown.setCurrentText(item["is_veg"])  # Set current value
            layout.addWidget(QLabel("Veg/Non-Veg:"))
            layout.addWidget(is_veg_dropdown)

            # Category Dropdown
            category_dropdown = QComboBox()
            self.load_categories_into_dropdown(category_dropdown)
            category_dropdown.setCurrentText(self.get_category_name(item["category_id"]))
            layout.addWidget(QLabel("Category:"))
            layout.addWidget(category_dropdown)

            # Item Name
            name_input = QLineEdit(item["item_name"])
            layout.addWidget(QLabel("Item Name:"))
            layout.addWidget(name_input)

            # Description
            desc_input = QLineEdit(item["item_desc"])
            layout.addWidget(QLabel("Description:"))
            layout.addWidget(desc_input)

            # Price
            price_input = QLineEdit(str(item["price"]))
            price_input.setValidator(QDoubleValidator(0.00, 99999.99, 2))
            layout.addWidget(QLabel("Price (₹):"))
            layout.addWidget(price_input)

            # Update Button
            update_button = QPushButton("Save Changes")
            update_button.setStyleSheet(f"background-color: {colors.color_1}; color: {colors.color_3};")
            update_button.clicked.connect(lambda: self.update_item(
                item["item_id"], category_dropdown.currentData(), is_veg_dropdown.currentText(),
                name_input.text(), desc_input.text(), price_input.text(), dialog
            ))
            
            layout.addWidget(update_button)
            dialog.setLayout(layout)
            dialog.exec_()

        def load_categories_into_dropdown(self, dropdown):
            """Load categories into a given dropdown"""
            response = supabase.table("categories").select("category_id", "category_name").execute()
            categories = response.data or []
            dropdown.clear()
            for category in categories:
                dropdown.addItem(category["category_name"], category["category_id"])
        
        def get_category_name(self, category_id):
            """Fetch category name using category_id"""
            response = supabase.table("categories").select("category_name").eq("category_id", category_id).execute()
            category = response.data
            return category[0]["category_name"] if category else "Unknown"

        def update_item(self, item_id, category_id, is_veg, name, desc, price, dialog):
            """Update an inventory item"""
            try:
                updated_data = {
                    "category_id": category_id,
                    "is_veg": is_veg,
                    "item_name": name.strip(),
                    "item_desc": desc.strip(),
                    "price": float(price.strip()),
                }
                supabase.table("inventory").update(updated_data).eq("item_id", item_id).execute()
                self.load_inventory()
                QMessageBox.information(self, "Success", "Item updated successfully!")
                dialog.accept()
            except ValueError:
                QMessageBox.critical(self, "Error", "Price must be numbers!")

        def delete_item(self, item):
            """Ask for confirmation before deleting an item"""
            confirmation = QMessageBox.question(
                self, "Delete Confirmation",
                f"Are you sure you want to delete '{item['item_name']}'?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if confirmation == QMessageBox.Yes:
                supabase.table("inventory").delete().eq("item_id", item["item_id"]).execute()
                self.load_inventory()
    return InventoryTab()