from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QListWidget,
    QProgressBar,
    QVBoxLayout,
    QPushButton,
    QTextEdit
)

class CharacterInfoWidget(QFrame):
    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet("background-color: #34495e; border-radius: 10px; padding: 10px;")
        
        self.layout = QVBoxLayout()
        
        # Character name
        self.name_label = QLabel(player.name)
        self.name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ecf0f1;")
        self.layout.addWidget(self.name_label, alignment=Qt.AlignCenter)
        
        # Stats
        self.stats_layout = QGridLayout()
        self.stat_labels = {}
        stats = [
            ("⚔️", "Strength", player.strength),
            ("🛡️", "Defense", player.defense),
            ("📚", "Intelligence", player.intelligence),
            ("💬", "Charisma", player.charisma)
        ]
        for row, (icon, stat_name, stat_value) in enumerate(stats):
            icon_label = QLabel(icon)
            icon_label.setFont(QFont("Segoe UI Emoji", 14))
            self.stats_layout.addWidget(icon_label, row, 0)
            self.stats_layout.addWidget(QLabel(f"{stat_name}:"), row, 1)
            value_label = QLabel(str(stat_value))
            self.stats_layout.addWidget(value_label, row, 2)
            self.stat_labels[stat_name.lower()] = value_label
        self.layout.addLayout(self.stats_layout)
        
        # Health bar
        self.health_bar = StyledProgressBar()  # Using StyledProgressBar
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(player.health)
        self.health_bar.setFormat("Health: %v/%m")
        self.health_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4a4a4a;
                border-radius: 5px;
                text-align: center;
                color: #fff;
                background-color: #2c3e50;
            }
            QProgressBar::chunk {
                background-color: #c0392b;
            }
        """)
        self.layout.addWidget(self.health_bar)
        
        # Gold display
        self.gold_label = QLabel(f"Gold: {player.gold}")
        self.gold_label.setStyleSheet("color: #f1c40f; font-weight: bold;")
        self.layout.addWidget(self.gold_label)
        
        self.setLayout(self.layout)
    
    def update_info(self):
        # Update name (in case it can change)
        self.name_label.setText(self.player.name)
        
        # Update stats
        stats_to_update = [
            ("strength", self.player.strength),
            ("defense", self.player.defense),
            ("intelligence", self.player.intelligence),
            ("charisma", self.player.charisma)
        ]
        for stat_name, new_value in stats_to_update:
            label = self.stat_labels[stat_name]
            old_value = int(label.text())
            label.setText(str(new_value))
            if new_value > old_value:
                self.flash_label(label, QColor(0, 255, 0))  # Green flash for increase
            elif new_value < old_value:
                self.flash_label(label, QColor(255, 0, 0))  # Red flash for decrease
        
        # Update health
        self.health_bar.setRange(0, 100)
        self.health_bar.setValue(self.player.health)
        health_percentage = (self.player.health / 100) * 100
        if health_percentage > 66:
            color = "#27ae60"  # Green for high health
        elif health_percentage > 33:
            color = "#f39c12"  # Orange for medium health
        else:
            color = "#c0392b"  # Red for low health
        self.health_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 2px solid #4a4a4a;
                border-radius: 5px;
                text-align: center;
                color: #fff;
                background-color: #2c3e50;
            }}
            QProgressBar::chunk {{
                background-color: {color};
            }}
        """)
        
        # Update gold
        self.gold_label.setText(f"Gold: {self.player.gold}")
    
    def flash_label(self, label, color):
        original_style = label.styleSheet()
        label.setStyleSheet(f"color: {color.name()}; font-weight: bold;")
        QTimer.singleShot(500, lambda: label.setStyleSheet(original_style))


class StyledProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 5px;
                text-align: center;
                color: #ECF0F1;
                background-color: #2C3E50;
            }
            QProgressBar::chunk {
                background-color: #E74C3C;
                border-radius: 5px;
            }
        """)

class StyledQLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Trajan Pro", 12))
        self.setStyleSheet("color: #D4AF37;")  # Gold color


class StyledButton(QPushButton):
    def __init__(self, text, icon=None):
        super().__init__(text)
        self.setFont(QFont("Trajan Pro", 10))
        self.setStyleSheet("""
            QPushButton {
                background-color: #D4AF37;
                color: #2C3E50;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #F1C40F;
            }
        """)
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(24, 24))

class StyledListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QListWidget {
                background-color: #34495E;
                border: 2px solid #D4AF37;
                border-radius: 5px;
                color: #ECF0F1;
                font-family: 'Trajan Pro', serif;
            }
            QListWidget::item:selected {
                background-color: #D4AF37;
                color: #2C3E50;
            }
        """)

class StyledTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #34495E;
                border: 2px solid #D4AF37;
                border-radius: 5px;
                color: #ECF0F1;
                font-family: 'Trajan Pro', serif;
            }
        """)