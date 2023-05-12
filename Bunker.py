import os
import pygame


class Bunker(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(game.image_folder, 'bunker_full_health.png')).convert()
        self.image.set_alpha(90)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.game = game
        self.explosion_sound = pygame.mixer.Sound(os.path.join(game.sounds_folder, 'explosion.mp3'))
        self.health = 3
        self.size = 40
        self.rect.x = x
        self.rect.y = y
        game.all_sprites.add(self)

    def update(self):
        for rocket in self.game.invader_rockets:
            if (self.rect.x + self.size > rocket.x > self.rect.x - self.size and
                    self.rect.y + self.size > rocket.y > self.rect.y - self.size):
                self.game.invader_rockets.remove(rocket)
                self.health -= 1
                self.explosion_sound.play()
                if self.health <= 0:
                    self.game.all_sprites.remove(self)
                else:
                    self.change_sprite()

    def change_sprite(self):
        if self.health == 2:
            self.image = pygame.image.load(os.path.join(self.game.image_folder, 'bunker_half_health.png')).convert()
        else:
            self.image = pygame.image.load(os.path.join(self.game.image_folder, 'bunker_low_health.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.image.set_alpha(90)
