import sys
import os


class GameResources:
    def __init__(self):
        self.game_folder = os.path.dirname(__file__)
        self.image_folder = os.path.join(self.game_folder, 'images')
        self.sounds_folder = os.path.join(self.game_folder, 'sounds')
