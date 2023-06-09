import pygame
import os
import thorpy.loops


class Player(pygame.sprite.Sprite):
    def __init__(self, game_resources, x, y, game_state):
        pygame.sprite.Sprite.__init__(self)
        self.image = game_resources.get_image('player.png')
        self.image.set_colorkey((255, 255, 255))
        self.life_lost_sound = game_resources.get_sound('life_lost.mp3')
        self.rect = self.image.get_rect()
        self.game_state = game_state
        self.health = 3
        self.size = 30
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
                self.life_lost_sound.play()
                if self.health <= 0:
                    self.game_state.done = True
                    self.game_state.lost = True
                    thorpy.loops.quit_all_loops()
                    return
