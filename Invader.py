import pygame
import os
import time


class Invader(pygame.sprite.Sprite):
    def __init__(self, game, x, y, row):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(game.image_folder, 'invader.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.timer = time.time()
        self.rect.x = x
        self.row = row
        self.rect.y = y
        self.game = game
        self.size = 42

    def update(self):
        if time.time() - self.timer > 1:
            self.timer = time.time()
            self.rect.y += 3
        self.check_collision(self.game)

    def check_collision(self, game):
        for rocket in game.rockets:
            if (self.rect.x + self.size > rocket.x > self.rect.x - self.size and
                    self.rect.y + self.size > rocket.y > self.rect.y - self.size):
                game.rockets.remove(rocket)
                game.invaders[self.row].remove(self)
                game.all_sprites.remove(self)
                game.score += (10 - self.row) * 4
