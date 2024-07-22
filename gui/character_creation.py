from PyQt5.QtWidgets import (
    QComboBox, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from models.character import Warrior, Diplomat, Maester
from models.house import House
from gui.widgets import StyledQLabel


class CharacterCreationWindow(QWidget):
    def __init__(self, on_character_created):
        super().__init__()
        self.on_character_created = on_character_created
        self.setWindowTitle("Create Your Character")
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;  /* Dark blue-gray */
                color: #ECF0F1;  /* Light gray */
                font-family: 'Trajan Pro', serif;
            }
            QLineEdit, QComboBox {
                background-color: #34495E;  /* Lighter blue-gray */
                border: 2px solid #D4AF37;  /* Gold */
                border-radius: 5px;
                padding: 5px;
                color: #ECF0F1;
                font-size: 14px;
            }
            QPushButton {
                background-color: #D4AF37;  /* Gold */
                color: #2C3E50;  /* Dark blue-gray */
                border: none;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F1C40F;  /* Lighter gold */
            }
        """)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Title
        title = StyledQLabel("Game of Thrones RPG")
        title.setFont(QFont("Trajan Pro", 24, QFont.Bold))
        layout.addWidget(title)

        # Character Name Input
        layout.addWidget(StyledQLabel("Character Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # House Selection
        layout.addWidget(StyledQLabel("Choose your House:"))
        self.house_combo = QComboBox()
        self.house_combo.addItems(["Stark", "Lannister", "Targaryen"])
        layout.addWidget(self.house_combo)

        # Character Class Selection
        layout.addWidget(StyledQLabel("Choose your Class:"))
        self.class_combo = QComboBox()
        self.class_combo.addItems(["Warrior", "Diplomat", "Maester"])
        layout.addWidget(self.class_combo)

        # Create Character Button
        self.create_button = QPushButton("Create Character")
        self.create_button.clicked.connect(self.create_character)
        layout.addWidget(self.create_button)

        # Add some spacing at the bottom
        layout.addStretch()

        self.setLayout(layout)

    def create_character(self):
        name = self.name_input.text()
        house = self.house_combo.currentText()
        character_class = self.class_combo.currentText()

        if name and house and character_class:
            house_obj = House(house, f"{house} Sigil", f"{house} Words")
            
            if character_class == "Warrior":
                character = Warrior(name, house_obj)
            elif character_class == "Diplomat":
                character = Diplomat(name, house_obj)
            else:
                character = Maester(name, house_obj)
            
            self.on_character_created(character)
            self.close()
        else:
            self.show_error_dialog()

    def show_error_dialog(self):
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setText("Please fill in all fields.")
        error_dialog.setWindowTitle("Error")
        error_dialog.setStyleSheet("""
            QMessageBox {
                background-color: #2C3E50;
                color: #ECF0F1;
            }
            QMessageBox QPushButton {
                background-color: #D4AF37;
                color: #2C3E50;
                padding: 5px 15px;
                border-radius: 3px;
            }
        """)
        error_dialog.exec_()