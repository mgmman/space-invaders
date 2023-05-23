import os
import pygame
import random


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, game, game_state):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(game.image_folder, 'mystery_ship.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.explosion_sound = pygame.mixer.Sound(os.path.join(game.sounds_folder, 'explosion.mp3'))
        self.game = game
        self.game_state = game_state
        self.health = 3
        self.size = 100
        self.rect.x = game.width
        self.rect.y = 44
        game.all_sprites.add(self)

    def update(self):
        self.rect.x -= 1
        for rocket in self.game_state.rockets:
            if (self.rect.x + self.size > rocket.x > self.rect.x - self.size and
                    self.rect.y + self.size > rocket.y > self.rect.y - self.size):
                self.game_state.rockets.remove(rocket)
                self.game.all_sprites.remove(self)
                self.game_state.score += random.choice([50, 100, 150, 200])
                self.explosion_sound.play()
                self.game_state.mystery_ship_flying = False
        if self.rect.right <= 0:
            self.game.all_sprites.remove(self)
            self.game_state.mystery_ship_flying = False
