from models.inventory import Inventory

class Character:
    def __init__(self, name, house, strength, intelligence, charisma, defense):
        self.name = name
        self.house = house
        self.strength = max(1, strength)  # Ensure strength is at least 1
        self.intelligence = intelligence
        self.charisma = charisma
        self.defense = max(0, defense)  # Ensure defense is non-negative
        self.health = 100
        self.gold = 100
        self.inventory = Inventory()
        self.position = (0, 0)
        self.defending = False

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def move(self, direction):
        x, y = self.position
        if direction == 'north':
            self.position = (x, y - 1)
        elif direction == 'south':
            self.position = (x, y + 1)
        elif direction == 'east':
            self.position = (x + 1, y)
        elif direction == 'west':
            self.position = (x - 1, y)

    def use_item(self, item_name):
        for item in self.inventory.items:
            if item.name == item_name:
                item.use(self)
                self.inventory.remove_item(item)
                return True
        return False

    def earn_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def is_alive(self):
        return self.health > 0

class Warrior(Character):
    def __init__(self, name, house):
        super().__init__(name, house, strength=12, intelligence=8, charisma=8, defense=10)

    def special_ability(self):
        return "Sword Strike", 10  # Name and extra damage

class Diplomat(Character):
    def __init__(self, name, house):
        super().__init__(name, house, strength=8, intelligence=10, charisma=12, defense=8)

    def special_ability(self):
        return "Persuasive Speech", 5  # Name and charisma boost

class Maester(Character):
    def __init__(self, name, house):
        super().__init__(name, house, strength=7, intelligence=13, charisma=9, defense=9)

    def special_ability(self):
        return "Healing Touch", 20  # Name and healing amount

class NPC:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class Boss(Character):
    def __init__(self, name, house, strength, intelligence, charisma, defense, special_ability):
        super().__init__(name, house, strength, intelligence, charisma, defense)
        self.special_ability = special_ability
        self.max_health = 150
        self.health = self.max_health

    def use_special_ability(self, target):
        return self.special_ability(self, target)

# Define boss characters
def cersei_ability(self, target):
    damage = self.intelligence * 2
    target.take_damage(damage)
    return f"Cersei uses 'Wildfire Plot' and deals {damage} damage!"

def night_king_ability(self, target):
    self.health += 20
    return f"The Night King uses 'Raise the Dead' and heals for 20 health!"

def dragon_ability(self, target):
    damage = self.strength * 3
    target.take_damage(damage)
    return f"Drogon uses 'Dragonfire' and deals {damage} damage!"

bosses = [
    Boss("Cersei Lannister", "Lannister", 10, 15, 18, 8, cersei_ability),
    Boss("Night King", "White Walkers", 20, 15, 10, 15, night_king_ability),
    Boss("Drogon", "Targaryen", 25, 10, 5, 20, dragon_ability)
]

class NPC:
    def __init__(self, name, type):
        self.name = name
        self.type = type