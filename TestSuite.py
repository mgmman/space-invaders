import sys
import thorpy.loops
import pygame
import unittest
import os
import time
import random
import thorpy
from Invader import Invader
from Player import Player
from Rockets import Rocket, InvaderRocket
from Bunker import Bunker
from MysteryShip import MysteryShip
from main import Game


class TestSuite(unittest.TestCase):
    def test_rocket_destroys_invader(self):
        game = Game(600, 800)
        invader = Invader(game, 0, 0, 0, 1)
        game.invaders.append([invader])
        prev_score = game.score
        self.assertEqual(len(game.invaders), 1)
        game.rockets.append(Rocket(game, 0, 0))
        invader.update()
        self.assertEqual(len(game.invaders[0]), 0)
        self.assertEqual(len(game.rockets), 0)
        self.assertGreater(game.score, prev_score)

    def test_player_takes_damage(self):
        pass

