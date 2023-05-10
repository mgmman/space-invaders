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
        game.invaders = [[invader]]
        prev_score = game.score
        self.assertEqual(len(game.invaders), 1)
        rocket = Rocket(game, 0, 0)
        game.rockets = [rocket]
        rocket.draw()
        invader.update()
        self.assertEqual(len(game.invaders[0]), 0)
        self.assertEqual(len(game.rockets), 0)
        self.assertGreater(game.score, prev_score)

    def test_player_takes_damage(self):
        game = Game(600, 800)
        player = Player(game, game.width / 2, game.height - 100)
        rocket = InvaderRocket(game, game.width / 2, game.height - 100)
        game.invader_rockets = [rocket]
        rocket.draw()
        player.update()
        self.assertEqual(player.health, 2)

    def test_game_ends_on_player_death(self):
        game = Game(600, 800)
        player = Player(game, game.width / 2, game.height - 100)
        player.health = 1
        rocket = InvaderRocket(game, game.width / 2, game.height - 100)
        game.invader_rockets = [rocket]
        player.update()
        self.assertTrue(game.lost)

    def test_mystery_ship_destruction_on_leaving_screen(self):
        game = Game(600, 800)
        prev_score = game.score
        ship = MysteryShip(game)
        self.assertEqual(len(game.all_sprites), 1)
        ship.rect.right = 0
        ship.update()
        self.assertEqual(len(game.all_sprites), 0)
        self.assertEqual(prev_score, game.score)

    def test_mystery_ship_destruction(self):
        game = Game(600, 800)
        prev_score = game.score
        ship = MysteryShip(game)
        self.assertEqual(len(game.all_sprites), 1)
        rocket = Rocket(game, ship.rect.center[0], ship.rect.center[1])
        game.rockets = [rocket]
        ship.update()
        self.assertEqual(len(game.all_sprites), 0)
        self.assertLess(prev_score, game.score)
        self.assertEqual(len(game.rockets), 0)

    def test_bunkers(self):
        game = Game(600, 800)
        bunker = Bunker(game, 0, 0)
        rocket = Rocket(game, 0, 0)
        game.rockets = [rocket]
        bunker.update()
        self.assertEqual(bunker.health, 3)
        invader_rocket = InvaderRocket(game, 0, 0)
        game.invader_rockets = [invader_rocket]
        bunker.update()
        self.assertEqual(bunker.health, 2)

    def test_invader_moves(self):
        game = Game(600, 800)
        invader = Invader(game, 0, 0, 0, 1)
        game.invaders = [[invader]]
        time.sleep(1)
        invader.update()
        self.assertGreater(invader.rect.y, 0)

    def test_game_over_on_invasion(self):
        game = Game(600, 800)
        invader = Invader(game, 0, 0, 0, 1)
        game.invaders = [[invader]]
        invader.rect.bottom = game.height - 90
        invader.update()
        self.assertTrue(game.lost)

    def test_bunkers_generation(self):
        game = Game(600, 800)
        game.generate_bunkers(4)
        self.assertEqual(len(game.all_sprites), 4)

    def test_invader_generation(self):
        game = Game(600, 800)
        game.generate_invaders(1)
        self.assertEqual(len(game.all_sprites), 22)
        self.assertEqual(len(game.invaders), 2)
        self.assertEqual(len(game.invaders[0]), 11)