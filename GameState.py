class GameState:
    def __init__(self):
        self.invaders = []
        self.invader_rockets = []
        self.rockets = []
        self.lost = False
        self.score = 0
        self.done = False
        self.won = False
        self.mystery_ship_flying = False