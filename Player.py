import pygame
import os
import thorpy.loops


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, game_state):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(game.image_folder, 'player.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.life_lost_sound = pygame.mixer.Sound(os.path.join(game.sounds_folder, 'life_lost.mp3'))
        self.rect = self.image.get_rect()
        self.game = game
        self.game_state = game_state
        self.health = 3
        self.size = 30
        self.rect.x = x
        self.rect.y = y
        game.all_sprites.add(self)

    def update(self):
        for rocket in self.game_state.invader_rockets:
            if (self.rect.x + self.size > rocket.x > self.rect.x - self.size and
                    self.rect.y + self.size > rocket.y > self.rect.y - self.size):
                self.game_state.invader_rockets.remove(rocket)
                self.health -= 1
                self.life_lost_sound.play()
                if self.health <= 0:
                    self.game_state.done = True
                    self.game_state.lost = True
                    thorpy.loops.quit_all_loops()
                    return
