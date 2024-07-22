from gui.character_creation import CharacterCreationWindow
from gui.main_window import GameGUI
from PyQt5.QtWidgets import (
    QApplication
)
from PyQt5.QtCore import QTimer
import sys

def main():
    app = QApplication(sys.argv)

    def on_character_created(character):
        game_window = GameGUI(character)
        game_window.show()
        game_loop(game_window)

    character_creation = CharacterCreationWindow(on_character_created)
    character_creation.show()

    sys.exit(app.exec_())


def game_loop(gui):
    # This function will be called repeatedly by a QTimer
    if gui.player.is_alive():
        # Handle any recurring game logic here
        gui.update_character_info()
        gui.update_inventory()
        gui.update_quests()
        
        # Check for quest completion
        for quest in gui.quests:
            if not quest.completed and quest.completion_condition(gui.player):
                quest.complete(gui.player)
                gui.dialogue_box.append(f"Quest completed: {quest.name}")
        
        # Schedule the next call to game_loop
        QTimer.singleShot(100, lambda: game_loop(gui))
    else:
        gui.dialogue_box.append("Game Over!")

if __name__ == '__main__':
    main()