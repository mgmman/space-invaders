import os
import pygame


class Bunker(pygame.sprite.Sprite):
    def __init__(self, game_resources, x, y, game_state):
        pygame.sprite.Sprite.__init__(self)
        self.image = game_resources.get_image('bunker_full_health.png')
        self.image.set_alpha(90)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.explosion_sound = game_resources.get_sound('explosion.mp3')
        self.health = 3
        self.game_resources = game_resources
        self.game_state = game_state
        self.size = 40
        self.rect.x = x
        self.rect.y = y
        game_state.all_sprites.add(self)

    def update(self):
        for rocket in self.game_state.invader_rockets:
            if (self.rect.x + self.size > rocket.x > self.rect.x - self.size and
                    self.rect.y + self.size > rocket.y > self.rect.y - self.size):
                self.game_state.invader_rockets.remove(rocket)
                self.game_state.all_sprites.remove(rocket)
                self.health -= 1
                self.explosion_sound.play()
                if self.health <= 0:
                    self.game_state.all_sprites.remove(self)
                else:
                    self.change_sprite()

    def change_sprite(self):
        if self.health == 2:
            self.image = self.game_resources.get_image('bunker_half_health.png')
        else:
            self.image = self.game_resources.get_image('bunker_low_health.png')
        self.image.set_colorkey((255, 255, 255))
        self.image.set_alpha(90)
