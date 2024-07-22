class Item:
    def __init__(self, name, value, effect):
        self.name = name
        self.value = value
        self.effect = effect

    def use(self, player):
        print(f"{player.name} uses {self.name}")
        self.effect(player)


class Inventory:
    def __init__(self, capacity=10):
        self.items = []
        self.capacity = capacity

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def get_total_value(self):
        return sum(item.value for item in self.items)

