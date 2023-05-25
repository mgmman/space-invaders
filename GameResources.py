import sys
import os
import pygame


class GameResources:
    def __init__(self):
        self.game_folder = os.path.dirname(__file__)
        self.image_folder = os.path.join(self.game_folder, 'images')
        self.sounds_folder = os.path.join(self.game_folder, 'sounds')

    def get_image(self, image_name):
        return pygame.image.load(
            os.path.join(
                self.image_folder,
                image_name
            )).convert()

    def get_sound(self, sound_name):
        return pygame.mixer.Sound(
            os.path.join(
                self.sounds_folder,
                sound_name))
