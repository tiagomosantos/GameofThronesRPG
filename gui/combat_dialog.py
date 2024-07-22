from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar, QPushButton, QTextEdit, QInputDialog, QMessageBox
import random
from models.character import Boss

class CombatDialog(QDialog):
    def __init__(self, player, enemy, parent=None):
        super().__init__(parent)
        self.player = player
        self.enemy = enemy
        self.setWindowTitle("Combat")
        self.setModal(True)
        self.layout = QVBoxLayout()

        self.info_label = QLabel(f"{player.name} vs {enemy.name}")
        self.layout.addWidget(self.info_label)

        self.player_health = QProgressBar()
        self.player_health.setRange(0, 100)
        self.player_health.setValue(player.health)
        self.layout.addWidget(QLabel("Player Health:"))
        self.layout.addWidget(self.player_health)

        self.enemy_health = QProgressBar()
        self.enemy_health.setRange(0, 100)
        self.enemy_health.setValue(enemy.health)
        self.layout.addWidget(QLabel("Enemy Health:"))
        self.layout.addWidget(self.enemy_health)

        self.action_buttons = {
            'attack': QPushButton('Attack'),
            'defend': QPushButton('Defend'),
            'use_item': QPushButton('Use Item'),
            'flee': QPushButton('Flee')
        }

        for button in self.action_buttons.values():
            self.layout.addWidget(button)
            button.clicked.connect(self.handle_action)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.layout.addWidget(self.log)

        self.setLayout(self.layout)

        if isinstance(enemy, Boss):
            self.boss_ability_button = QPushButton('Use Special Ability')
            self.boss_ability_button.clicked.connect(self.use_boss_ability)
            self.layout.addWidget(self.boss_ability_button)

    def use_boss_ability(self):
        if isinstance(self.enemy, Boss):
            result = self.enemy.use_special_ability(self.player)
            self.log.append(result)
            self.update_health_bars()
            self.check_combat_end()
            if self.player.is_alive():
                self.enemy_turn()

    def handle_action(self):
        action = self.sender().text().lower()
        if action == 'attack':
            self.player_attack()
        elif action == 'defend':
            self.player_defend()
        elif action == 'use_item':
            self.use_item()
        elif action == 'flee':
            self.flee()

        if self.enemy.is_alive() and self.player.is_alive():
            self.enemy_turn()

        self.update_health_bars()
        self.check_combat_end()


    def player_defend(self):
        self.player.defending = True
        self.log.append(f"{self.player.name} takes a defensive stance.")

    def use_item(self):
        items = [item for item in self.player.inventory.items if item.combat_usable]
        if not items:
            self.log.append("No usable items in inventory!")
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

    def flee(self):
        if random.random() < 0.5:
            self.log.append(f"{self.player.name} successfully fled from combat!")
            self.accept()
        else:
            self.log.append(f"{self.player.name} failed to flee!")

    def check_combat_end(self):
        if not self.player.is_alive():
            self.log.append(f"{self.player.name} has been defeated!")
            self.finish_combat(victor=self.enemy)
        elif not self.enemy.is_alive():
            self.log.append(f"{self.enemy.name} has been defeated!")
            self.finish_combat(victor=self.player)

    def finish_combat(self, victor):
        if victor == self.player:
            reward = random.randint(10, 50)
            self.player.earn_gold(reward)
            self.log.append(f"{self.player.name} wins! Earned {reward} gold.")
        QMessageBox.information(self, "Combat Ended", self.log.toPlainText())
        self.accept()

    def player_attack(self):
        damage = max(1, self.player.strength - self.enemy.defense)
        self.enemy.take_damage(damage)
        self.log.append(f"{self.player.name} attacks for {damage} damage!")
        self.update_health_bars()

    def enemy_turn(self):
        if self.player.defending:
            damage = max(1, (self.enemy.strength // 2) - self.player.defense)
            self.player.defending = False
        else:
            damage = max(1, self.enemy.strength - self.player.defense)
        self.player.take_damage(damage)
        self.log.append(f"{self.enemy.name} attacks for {damage} damage!")
        self.update_health_bars()

    def update_health_bars(self):
        self.player_health.setValue(self.player.health)
        self.enemy_health.setValue(self.enemy.health)
        self.player_health.setFormat(f"{self.player.health}/{100}")
        self.enemy_health.setFormat(f"{self.enemy.health}/{100}")
