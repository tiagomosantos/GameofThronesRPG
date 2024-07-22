from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGridLayout,
                                QPushButton, QFrame, QInputDialog, QListWidget, QTextEdit, QDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import random

from gui.combat_dialog import CombatDialog
from gui.widgets import StyledListWidget, CharacterInfoWidget
from gui.widgets import StyledTextEdit, StyledButton  
from game.game_board import GameBoard
from models.quest import Quest
from models.inventory import Item
from models.character import Character, Boss

class GameGUI(QMainWindow):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.game_board = GameBoard()
        self.quests = [
            Quest("The King's Errand", 
                  "Deliver a message to the Night's Watch.", 
                  lambda p: p.earn_gold(100),
                  lambda p: p.position == (5, 5)),
            Quest("Dragon's Egg", 
                  "Find a dragon egg in Dragonstone.", 
                  lambda p: p.inventory.add_item(Item("Dragon Egg", 1000, lambda x: None)),
                  lambda p: any(item.name == "Dragon Egg" for item in p.inventory.items)),
            Quest("Defend the Wall", 
                  "Help the Night's Watch defend against wildlings.", 
                  lambda p: setattr(p, 'strength', p.strength + 2),
                  lambda p: p.position == (0, 9) and p.strength > 12)
        ]
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game of Thrones RPG')
        self.setGeometry(100, 100, 1000, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
            }
            QListWidget {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
            }
            QTextEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

       # Left panel: Character info, inventory, and location legend
        left_panel = QVBoxLayout()

        # Add CharacterInfoWidget
        self.char_info_widget = CharacterInfoWidget(self.player)
        left_panel.addWidget(self.char_info_widget)

        # Inventory
        left_panel.addWidget(QLabel("Inventory:"))
        self.inventory_list = StyledListWidget()
        left_panel.addWidget(self.inventory_list)

        # Location legend
        left_panel.addWidget(QLabel("Locations:"))
        self.location_legend = QGridLayout()
        self.update_location_legend()
        left_panel.addLayout(self.location_legend)

        # Available NPCs
        left_panel.addWidget(QLabel("Available NPCs:"))
        self.npc_list = StyledListWidget()
        left_panel.addWidget(self.npc_list)

        # Center panel: Game board
        center_panel = QVBoxLayout()
        self.game_map = QGridLayout()
        self.update_game_map()
        center_panel.addLayout(self.game_map)

        # Action buttons
        # Action buttons
        action_layout = QGridLayout()
        action_buttons = {
            'move': QPushButton('🧭 Move'),
            'interact': QPushButton('🤝 Interact with NPC'),
            'use_item': QPushButton('🎒 Use Item'),
            'view_quests': QPushButton('📜 View Quests'),
            'initiate_combat': QPushButton('⚔️ Initiate Combat')
        }
        for button in action_buttons.values():
            button.setFont(QFont("Segoe UI Emoji", 12))
            button.setStyleSheet("""                
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

        action_layout.addWidget(action_buttons['move'], 0, 0)
        action_layout.addWidget(action_buttons['interact'], 0, 1)
        action_layout.addWidget(action_buttons['use_item'], 1, 0)
        action_layout.addWidget(action_buttons['view_quests'], 1, 1)
        action_layout.addWidget(action_buttons['initiate_combat'], 2, 0, 1, 2)

        action_buttons['move'].clicked.connect(self.show_move_options)
        action_buttons['interact'].clicked.connect(self.interact_with_npc)
        action_buttons['use_item'].clicked.connect(self.use_item)
        action_buttons['view_quests'].clicked.connect(self.view_quests)
        action_buttons['initiate_combat'].clicked.connect(self.initiate_combat)

        center_panel.addLayout(action_layout)

        # Right panel: Quest log and dialogue box
        right_panel = QVBoxLayout()
        self.quest_list = StyledListWidget()
        right_panel.addWidget(QLabel("Quests:"))
        right_panel.addWidget(self.quest_list)

        self.dialogue_box = StyledTextEdit()
        self.dialogue_box.setReadOnly(True)
        right_panel.addWidget(QLabel("Events:"))
        right_panel.addWidget(self.dialogue_box)

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(center_panel, 2)
        main_layout.addLayout(right_panel, 1)

        self.update_character_info()
        self.update_inventory()
        self.update_quests()
        self.update_available_npcs()


    def update_game_map(self):
        for i in reversed(range(self.game_map.count())): 
            self.game_map.itemAt(i).widget().setParent(None)

        for y in range(self.game_board.size):
            for x in range(self.game_board.size):
                location = self.game_board.get_location(x, y)
                label = QLabel(location.name[0])
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet(f"""
                    background-color: {location.color};
                    color: black;
                    border: 1px solid black;
                    font-weight: bold;
                    min-width: 30px;
                    min-height: 30px;
                """)
                if self.player and (x, y) == self.player.position:
                    label.setStyleSheet(label.styleSheet() + "border: 2px solid red;")
                self.game_map.addWidget(label, y, x)


    def update_location_legend(self):
        for i, location in enumerate(self.game_board.locations + [self.game_board.wilderness]):
            color_label = QLabel()
            color_label.setStyleSheet(f"background-color: {location.color}; border: 1px solid black;")
            color_label.setFixedSize(20, 20)
            self.location_legend.addWidget(color_label, i, 0)
            self.location_legend.addWidget(QLabel(location.name), i, 1)

    def show_move_options(self):
        directions = ['North', 'South', 'East', 'West']
        direction, ok = QInputDialog.getItem(self, "Move", "Choose a direction:", directions, 0, False)
        if ok and direction:
            self.move_player(direction.lower())

    def move_player(self, direction):
        x, y = self.player.position
        if direction == 'north' and y > 0:
            self.player.position = (x, y - 1)
        elif direction == 'south' and y < self.game_board.size - 1:
            self.player.position = (x, y + 1)
        elif direction == 'west' and x > 0:
            self.player.position = (x - 1, y)
        elif direction == 'east' and x < self.game_board.size - 1:
            self.player.position = (x + 1, y)

        self.update_game_map()
        self.check_for_events()
        self.update_available_npcs()  # Update NPC list after moving

    def update_available_npcs(self):
        self.npc_list.clear()
        current_location = self.game_board.get_location(*self.player.position)
        if current_location.name != "Wilderness":
            for npc in current_location.npcs:
                self.npc_list.addItem(f"{npc.name} ({npc.type})")
        else:
            self.npc_list.addItem("No NPCs in the wilderness")

    def interact_with_npc(self):
        current_location = self.game_board.get_location(*self.player.position)
        if current_location.name == "Wilderness":
            self.dialogue_box.append("There are no NPCs in the wilderness.")
            return

        available_npcs = current_location.npcs
        if not available_npcs:
            self.dialogue_box.append(f"There are no NPCs available in {current_location.name}.")
            return

        npc_names = [f"{npc.name} ({npc.type})" for npc in available_npcs]
        npc, ok = QInputDialog.getItem(self, "Interact", f"Choose an NPC in {current_location.name}:", npc_names, 0, False)
        
        if ok and npc:
            chosen_npc = available_npcs[npc_names.index(npc)]
            if chosen_npc.type == 'Merchant':
                self.interact_with_merchant(chosen_npc)
            elif chosen_npc.type == 'Innkeeper':
                self.interact_with_innkeeper(chosen_npc)
            elif chosen_npc.type == 'Guard':
                self.interact_with_guard(chosen_npc)

    def interact_with_merchant(self, merchant):
        self.dialogue_box.append(f"{merchant.name}: 'Welcome! What would you like to do?'")
        options = ['Buy', 'Sell', 'Exit']
        choice, ok = QInputDialog.getItem(self, merchant.name, "Choose an action:", options, 0, False)
        
        if ok and choice == 'Buy':
            items_for_sale = [
                Item("Health Potion", 50, lambda p: setattr(p, 'health', min(100, p.health + 30))),
                Item("Strength Potion", 100, lambda p: setattr(p, 'strength', p.strength + 5)),
                Item("Shield", 150, lambda p: setattr(p, 'defense', p.defense + 5))
            ]
            item_names = [f"{item.name} ({item.value} gold)" for item in items_for_sale]
            item, ok = QInputDialog.getItem(self, "Buy", "Choose an item to buy:", item_names, 0, False)
            
            if ok and item:
                chosen_item = items_for_sale[item_names.index(item)]
                if self.player.gold >= chosen_item.value:
                    self.player.gold -= chosen_item.value
                    self.player.inventory.add_item(chosen_item)
                    self.dialogue_box.append(f"You bought {chosen_item.name} for {chosen_item.value} gold.")
                    self.update_inventory()
                    self.update_character_info()
                else:
                    self.dialogue_box.append("Not enough gold to buy this item.")
        
        elif ok and choice == 'Sell':
            if not self.player.inventory.items:
                self.dialogue_box.append("You have no items to sell.")
            else:
                item_names = [f"{item.name} ({item.value//2} gold)" for item in self.player.inventory.items]
                item, ok = QInputDialog.getItem(self, "Sell", "Choose an item to sell:", item_names, 0, False)
                
                if ok and item:
                    chosen_item = self.player.inventory.items[item_names.index(item)]
                    self.player.gold += chosen_item.value // 2
                    self.player.inventory.remove_item(chosen_item)
                    self.dialogue_box.append(f"You sold {chosen_item.name} for {chosen_item.value//2} gold.")
                    self.update_inventory()
                    self.update_character_info()

    def interact_with_innkeeper(self, innkeeper):
        self.dialogue_box.append(f"{innkeeper.name}: 'Need a room for the night?'")
        options = ['Rest (20 gold)', 'Exit']
        choice, ok = QInputDialog.getItem(self, innkeeper.name, "Choose an action:", options, 0, False)
        
        if ok and choice == 'Rest (20 gold)':
            if self.player.gold >= 20:
                self.player.gold -= 20
                health_recovered = min(100 - self.player.health, 50)
                self.player.health += health_recovered
                self.dialogue_box.append(f"You rested for the night and recovered {health_recovered} health.")
                self.update_character_info()
            else:
                self.dialogue_box.append("Not enough gold to rest for the night.")

    def interact_with_guard(self, guard):
        self.dialogue_box.append(f"{guard.name}: 'Move along, citizen. Nothing to see here.'")
        options = ['Ask for Information', 'Request Quest', 'Exit']
        choice, ok = QInputDialog.getItem(self, guard.name, "Choose an action:", options, 0, False)
        
        if ok and choice == 'Ask for Information':
            information = [
                "I heard rumors of a dragon sighting near Dragonstone.",
                "The Lannisters are plotting something in King's Landing.",
                "Winter is coming, and the Night's Watch needs more men.",
                "There's unrest in the Iron Islands."
            ]
            info = random.choice(information)
            self.dialogue_box.append(f"Guard: '{info}'")
        
        elif ok and choice == 'Request Quest':
            if len([q for q in self.quests if not q.completed]) < 3:  # Limit active quests
                new_quest = random.choice([
                    Quest("Patrol the Walls", "Help the city guard patrol the walls.", 
                          lambda p: p.earn_gold(75), lambda p: p.position == (3, 3)),
                    Quest("Deliver a Message", "Deliver a confidential message to the Maester.", 
                          lambda p: p.inventory.add_item(Item("Rare Book", 100, lambda x: None)), 
                          lambda p: p.position == (7, 7)),
                    Quest("Investigate Rumors", "Investigate rumors of bandits in the nearby forest.", 
                          lambda p: setattr(p, 'strength', p.strength + 3), 
                          lambda p: any(item.name == "Bandit's Emblem" for item in p.inventory.items))
                ])
                self.quests.append(new_quest)
                self.dialogue_box.append(f"New quest received: {new_quest.name}")
                self.dialogue_box.append(new_quest.description)
                self.update_quests()
            else:
                self.dialogue_box.append("Guard: 'You already have enough tasks. Complete some of your current quests first.'")

    def use_item(self):
        items = [item for item in self.player.inventory.items]
        if not items:
            self.dialogue_box.append("No usable items in inventory!")
            return
        item_names = [item.name for item in items]
        item, ok = QInputDialog.getItem(self, "Use Item", "Choose an item to use:", item_names, 0, False)
        if ok and item:
            chosen_item = next(i for i in items if i.name == item)
            chosen_item.use(self.player)
            self.player.inventory.remove_item(chosen_item)
            self.update_character_info()  # Update character info after using item
            self.update_inventory()
            self.dialogue_box.append(f"Used {chosen_item.name}")



    def view_quests(self):
        quest_info = ""
        for quest in self.quests:
            status = "Completed" if quest.completed else "Active"
            quest_info += f"{quest.name} - {status}\n{quest.description}\n\n"
        self.dialogue_box.setText(quest_info)


    def initiate_combat(self):
        current_location = self.game_board.get_location(*self.player.position)
        if current_location.boss:
            enemy = current_location.boss
            self.dialogue_box.append(f"You encounter {enemy.name}, prepare for a boss battle!")
        else:
            enemies = ['Bandit', 'Wild Animal', 'Rival House Soldier']
            enemy_name, ok = QInputDialog.getItem(self, "Combat", "Choose an enemy to fight:", enemies, 0, False)
            if not (ok and enemy_name):
                return
            enemy = Character(enemy_name, None, 
                              strength=random.randint(8, 15),
                              intelligence=random.randint(5, 15), 
                              charisma=random.randint(5, 15), 
                              defense=random.randint(3, 8))
        self.start_combat(enemy)


    def start_combat(self, enemy):
        combat_dialog = CombatDialog(self.player, enemy, self)
        result = combat_dialog.exec_()
        if result == QDialog.Accepted:
            self.update_character_info()
            self.update_inventory()
            self.dialogue_box.append("Combat ended.")
            if self.player.is_alive():
                self.dialogue_box.append(f"You defeated {enemy.name}!")
                if isinstance(enemy, Boss):
                    self.dialogue_box.append("You've defeated a powerful boss!")
                    # Add special rewards for defeating a boss
                    self.player.earn_gold(200)
                    self.dialogue_box.append("You earned 200 gold for your victory!")
            else:
                self.dialogue_box.append("You were defeated in combat.")
        
        combat_dialog.deleteLater()  # Ensure the dialog is properly destroyed

    def check_for_events(self):
        location = self.game_board.get_location(*self.player.position)
        if location.trigger_event():
            self.trigger_random_event()


    def trigger_random_event(self):
        events = [
            ("You find a bag of gold!", lambda: self.player.earn_gold(50)),
            ("You are ambushed by bandits!", self.trigger_combat_event),
            ("You discover an ancient artifact!", lambda: self.player.inventory.add_item(Item("Ancient Artifact", 200, lambda x: None))),
            ("A kind stranger offers you food and rest.", lambda: setattr(self.player, 'health', min(100, self.player.health + 10))),
        ]
        event, effect = random.choice(events)
        self.dialogue_box.append(event)
        effect()
        self.update_character_info()
        self.update_inventory()

    def trigger_combat_event(self):
        enemy = Character("Bandit", None, 
                          strength=random.randint(8, 15),
                          intelligence=random.randint(5, 15), 
                          charisma=random.randint(5, 15), 
                          defense=random.randint(3, 8))
        self.start_combat(enemy)


    def update_character_info(self):
        self.char_info_widget.update_info()
        
    def update_inventory(self):
        self.inventory_list.clear()
        for item in self.player.inventory.items:
            self.inventory_list.addItem(f"{item.name} (Value: {item.value})")

    def update_quests(self):
        self.quest_list.clear()
        for quest in self.quests:
            status = "Completed" if quest.completed else "Active"
            self.quest_list.addItem(f"{quest.name} - {status}")



