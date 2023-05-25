import sys
import thorpy.loops
import pygame
import unittest
import os
import time
import random
import thorpy
sys.path.append(os.path.abspath(os.path.dirname(__file__)[:-6]))
from Invader import Invader
from Player import Player
from Rockets import Rocket, InvaderRocket
from Bunker import Bunker
from MysteryShip import MysteryShip
from SpaceInvaders import Game
from GameState import GameState
from GameResources import GameResources


class CollisionAndDestructionTests(unittest.TestCase):
    def test_rocket_destroys_invader(self):
        game = Game(600, 800)
        game_resources = GameResources()
        game_state = GameState(600, 800)
        invader = Invader(game_resources, 0, 0, 0, 1, game_state)
        game_state.invaders = [[invader]]
        prev_score = game_state.score
        self.assertEqual(len(game_state.invaders), 1)
        rocket = Rocket(game, 0, 0)
        game_state.rockets = [rocket]
        rocket.draw()
        invader.update()
        self.assertEqual(len(game_state.invaders[0]), 0)
        self.assertEqual(len(game_state.rockets), 0)
        self.assertGreater(game_state.score, prev_score)

    def test_player_takes_damage(self):
        game = GameResources()
        game_state = GameState(600, 800)
        player = Player(game, game.width / 2, game.height - 100, game_state)
        rocket = InvaderRocket(game, game.width / 2, game.height - 100)
        game_state.invader_rockets = [rocket]
        rocket.draw()
        player.update()
        self.assertEqual(player.health, 2)

    def test_mystery_ship_destruction(self):
        game = GameResources()
        game_state = GameState(600, 800)
        prev_score = game_state.score
        ship = MysteryShip(game, game_state)
        self.assertEqual(len(game.all_sprites), 1)
        rocket = Rocket(game, ship.rect.center[0], ship.rect.center[1])
        game_state.rockets = [rocket]
        ship.update()
        self.assertEqual(len(game.all_sprites), 0)
        self.assertLess(prev_score, game_state.score)
        self.assertEqual(len(game_state.rockets), 0)

    def test_bunkers(self):
        game = GameResources()
        game_state = GameState(600, 800)
        bunker = Bunker(game, 0, 0, game_state)
        rocket = Rocket(game, 0, 0)
        game_state.rockets = [rocket]
        bunker.update()
        self.assertEqual(bunker.health, 3)
        invader_rocket = InvaderRocket(game, 0, 0)
        game_state.invader_rockets = [invader_rocket]
        bunker.update()
        self.assertEqual(bunker.health, 2)


class GenerationsTests(unittest.TestCase):
    def test_bunkers_generation(self):
        game = GameResources()
        game_state = GameState(600, 800)
        game.generate_bunkers(4, game_state)
        self.assertEqual(len(game.all_sprites), 4)

    def test_invader_generation(self):
        game = GameResources()
        game_state = GameState(600, 800)
        game.generate_invaders(1, game_state)
        self.assertEqual(len(game.all_sprites), 22)
        self.assertEqual(len(game_state.invaders), 2)
        self.assertEqual(len(game_state.invaders[0]), 11)


class MovementTests(unittest.TestCase):
    def test_mystery_ship_destruction_on_leaving_screen(self):
        game = GameResources()
        game_state = GameState(600, 800)
        prev_score = game_state.score
        ship = MysteryShip(game, game_state)
        self.assertEqual(len(game.all_sprites), 1)
        ship.rect.right = 0
        ship.update()
        self.assertEqual(len(game.all_sprites), 0)
        self.assertEqual(prev_score, game_state.score)

    def test_invader_moves(self):
        game = GameResources()
        game_state = GameState(600, 800)
        invader = Invader(game, 0, 0, 0, 1, game_state)
        game_state.invaders = [[invader]]
        time.sleep(1)
        invader.update()
        self.assertGreater(invader.rect.y, 0)


class GameOverTests(unittest.TestCase):
    def test_game_over_on_invasion(self):
        game = GameResources()
        game_state = GameState(600, 800)
        invader = Invader(game, 0, 0, 0, 1, game_state)
        game_state.invaders = [[invader]]
        invader.rect.bottom = game.height - 90
        invader.update()
        self.assertTrue(game_state.lost)

    def test_game_ends_on_player_death(self):
        game = GameResources()
        game_state = GameState(600, 800)
        player = Player(game, game.width / 2, game.height - 100, game_state)
        player.health = 1
        rocket = InvaderRocket(game, game.width / 2, game.height - 100)
        game_state.invader_rockets = [rocket]
        player.update()
        self.assertTrue(game_state.lost)
