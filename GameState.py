import pygame


class GameState:
    def __init__(self, height, width):
        self.invaders = []
        self.height = height
        self.width = width
        self.invader_rockets = []
        self.rockets = []
        self.lost = False
        self.score = 0
        self.done = False
        self.won = False
        self.mystery_ship_flying = False
        self.all_sprites = pygame.sprite.Group()

