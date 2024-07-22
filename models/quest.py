class Quest:
    def __init__(self, name, description, reward, completion_condition):
        self.name = name
        self.description = description
        self.reward = reward
        self.completion_condition = completion_condition
        self.completed = False

    def complete(self, player):
        if not self.completed:
            self.completed = True
            self.reward(player)
