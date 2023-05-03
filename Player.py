import pygame
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(game.image_folder, 'player.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.game = game
        self.health = 3
        self.size = 30
        self.rect.x = x
        self.rect.y = y

    def update(self):
        for rocket in self.game.invader_rockets:
            if (self.rect.x + self.size > rocket.x > self.rect.x - self.size and
                    self.rect.y + self.size > rocket.y > self.rect.y - self.size):
                self.game.invader_rockets.remove(rocket)
                self.health -= 1
