import pygame
import sys
import os


class Rocket(pygame.sprite.Sprite):
    def __init__(self, game_resources, game_state, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(
                game_resources.image_folder,
                'rocket.png'
            )).convert()
        self.image.set_colorkey((255, 255, 255))
        game_state.all_sprites.add(self)
        game_state.rockets.append(self)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.y = y
        self.rect.x = x

    def update(self):
        self.rect.y -= 2
        self.y -= 2


class InvaderRocket(pygame.sprite.Sprite):
    def __init__(self, game_resources, game_state, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(
                game_resources.image_folder,
                'invader_rocket.png'
            )).convert()
        self.image.set_colorkey((255, 255, 255))
        game_state.all_sprites.add(self)
        game_state.invader_rockets.append(self)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.y = y
        self.rect.x = x

    def update(self):
        self.rect.y += 2
        self.y += 2
