import random
from models.character import NPC, bosses

class Location:
    def __init__(self, name, color, event_probability=0.3, npcs=None):
        self.name = name
        self.color = color
        self.event_probability = event_probability
        self.npcs = npcs or []
        self.boss = None

    def trigger_event(self):
        return random.random() < self.event_probability


class GameBoard:
    def __init__(self, size=10):
        self.size = size
        self.locations = [
            Location("Winterfell", "#444444", npcs=[
                NPC("Stark Steward", "Merchant"),
                NPC("Maester Luwin", "Innkeeper"),
                NPC("Ser Rodrik Cassel", "Guard")
            ]),
            Location("King's Landing", "#f1c232", npcs=[
                NPC("Street Vendor", "Merchant"),
                NPC("Tavern Keeper", "Innkeeper"),
                NPC("City Watch Guard", "Guard")
            ]),
            Location("The Wall", "#fffafa", npcs=[
                NPC("Night's Watch Steward", "Merchant"),
                NPC("Castle Black Cook", "Innkeeper"),
                NPC("Night's Watch Ranger", "Guard")
            ]),
            Location("Dragonstone", "#6a329f", npcs=[
                NPC("Smuggler", "Merchant"),
                NPC("Dragonstone Servant", "Innkeeper")
            ]),
            Location("Riverrun", "#2986cc", npcs=[
                NPC("Tully Merchant", "Merchant"),
                NPC("Riverrun Innkeeper", "Innkeeper"),
                NPC("Tully Guard", "Guard")
            ]),
            Location("The Eyrie", "skyblue", npcs=[
                NPC("Vale Trader", "Merchant"),
                NPC("Eyrie Steward", "Innkeeper"),
                NPC("Knight of the Vale", "Guard")
            ]),
            Location("Casterly Rock", "#990000", npcs=[
                NPC("Lannister Merchant", "Merchant"),
                NPC("Golden Tooth Innkeeper", "Innkeeper"),
                NPC("Lannister Guard", "Guard")
            ]),
            Location("Highgarden", "#a64d79", npcs=[
                NPC("Reach Trader", "Merchant"),
                NPC("Highgarden Servant", "Innkeeper"),
                NPC("Tyrell Guard", "Guard")
            ]),
            Location("Dorne", "#ffe599", npcs=[
                NPC("Dornish Merchant", "Merchant"),
                NPC("Sunspear Innkeeper", "Innkeeper"),
                NPC("Martell Guard", "Guard")
            ]),
            Location("Iron Islands", "#999999", npcs=[
                NPC("Ironborn Trader", "Merchant"),
                NPC("Pyke Servant", "Innkeeper"),
                NPC("Ironborn Warrior", "Guard")
            ])
        ]
        self.wilderness = Location("Wilderness", "#4a6741")
        self.board = self.generate_board()
        self.place_bosses()

    def generate_board(self):
        board = [[self.wilderness for _ in range(self.size)] for _ in range(self.size)]
        available_positions = [(x, y) for x in range(self.size) for y in range(self.size)]
        
        for location in self.locations:
            if available_positions:
                x, y = random.choice(available_positions)
                board[y][x] = location
                available_positions.remove((x, y))
            else:
                break  # No more available positions
        
        return board

    def get_location(self, x, y):
        return self.board[y][x]


    def place_bosses(self):
        boss_locations = {
            "King's Landing": bosses[0],  # Cersei
            "The Wall": bosses[1],        # Night King
            "Dragonstone": bosses[2]      # Drogon
        }
        for y in range(self.size):
            for x in range(self.size):
                location = self.board[y][x]
                if location.name in boss_locations:
                    location.boss = boss_locations[location.name]

