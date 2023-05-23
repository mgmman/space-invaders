import pygame
import os
import time
import thorpy.loops


class Invader(pygame.sprite.Sprite):
    def __init__(self, game, x, y, row, difficulty, game_state):
        self.game_state = game_state
        pygame.sprite.Sprite.__init__(self)
        if row % 2 == 0:
            self.image = pygame.image.load(os.path.join(game.image_folder, 'invader.png')).convert()
        else:
            self.image = pygame.image.load(os.path.join(game.image_folder, 'invader_2.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.timer = time.time()
        self.rect.x = x
        self.explosion_sound = pygame.mixer.Sound(os.path.join(game.sounds_folder, 'explosion.mp3'))
        self.difficulty = difficulty
        self.row = row
        self.rect.y = y
        self.game = game
        self.size = 42 - difficulty * 3
        game.all_sprites.add(self)

    def update(self):
        if time.time() - self.timer > 1:
            self.timer = time.time()
            self.rect.y += 5 * self.difficulty
        self.check_collision()
        if self.rect.bottom >= self.game.height - 100:
            self.game_state.done = True
            self.game_state.lost = True
            thorpy.loops.quit_all_loops()

    def check_collision(self):
        for rocket in self.game_state.rockets:
            if (self.rect.x + self.size > rocket.x > self.rect.x - self.size and
                    self.rect.y + self.size > rocket.y > self.rect.y - self.size):
                self.game_state.rockets.remove(rocket)
                self.game_state.invaders[self.row].remove(self)
                self.game.all_sprites.remove(self)
                self.game_state.score += (10 - self.row) * self.difficulty * 2
                self.explosion_sound.play()
