import sys
import thorpy.loops
import pygame
import os
import time
import random
import thorpy
from Invader import Invader
from Player import Player
from Rockets import Rocket, InvaderRocket
from Bunker import Bunker
from MysteryShip import MysteryShip


class Game:
    invaders = []
    invader_rockets = []
    rockets = []
    lost = False

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.game_folder = os.path.dirname(__file__)
        self.image_folder = os.path.join(self.game_folder, 'images')
        self.all_sprites = pygame.sprite.Group()
        self.score = 0
        self.won = False
        self.number_of_bunkers = 4
        self.mystery_ship_flying = False
        done = False
        player = Player(self, width / 2, height-100)
        self.all_sprites.add(player)
        self.generate_invaders()
        self.generate_bunkers()
        self.run_game(done, height, player, width)

    def run_game(self, done, height, player, width):
        while not done:
            self.display_HUD_text(f"score: {self.score}", 10, 0)
            self.display_HUD_text(f"health: {player.health}", 10, 20)
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                player.rect.x -= 2 if player.rect.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                player.rect.x += 2 if player.rect.x < width - 20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.rockets.append(Rocket(self, player.rect.center[0], player.rect.center[1]))

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            if len(self.invaders) == 0:
                done = True
                self.won = True
            else:
                if len(self.invaders) != 0 and len(self.invaders[-1]) == 0:
                    self.invaders.pop()

                if len(self.invaders) != 0 and self.invaders[-1][0].rect.y > height - 100 or player.health <= 0:
                    self.lost = True
                    done = True


                if random.random() > 0.98:
                    shooting_invader = random.choice(self.invaders[-1])
                    invader_rocket = InvaderRocket(self, shooting_invader.rect.center[0],
                                                   shooting_invader.rect.center[1])
                    self.invader_rockets.append(invader_rocket)

                if not self.mystery_ship_flying and random.random() > 0.999:
                    MysteryShip(self)
                    self.mystery_ship_flying = True

            if not self.lost:
                self.all_sprites.update()
                self.all_sprites.draw(self.screen)

                for rocket in self.rockets:
                    rocket.draw()

                for rocket in self.invader_rockets:
                    rocket.draw()
        if self.lost:
            self.display_game_over_text("DEFEAT")
        elif self.won:
            self.display_game_over_text("VICTORY ACHIEVED")
        print("3333")

    def generate_invaders(self, max_rows = 1):
        vertical_margin = 30
        horizontal_margin = 150
        width = 50
        row = -1
        for y in range(horizontal_margin, int(self.height / 2), width):
            row += 1
            if row > max_rows:
                break
            invaders_row = []
            for x in range(vertical_margin, self.width - vertical_margin, width):
                invader = Invader(self, x, y, row)
                invaders_row.append(invader)
                self.all_sprites.add(invader)
            self.invaders.append(invaders_row)

    def generate_bunkers(self):
        vertical_margin = 30
        width = self.width // self.number_of_bunkers
        for x in range(vertical_margin, self.width - vertical_margin, width):
            bunker = Bunker(self, x, self.height - 200)

    def display_game_over_text(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        text_surface = font.render(text, False, (44, 0, 62))
        self.screen.blit(text_surface,
                         ((self.width - text_surface.get_width()) // 2,
                          self.height // 2 - 100))
        thorpy.init(self.screen)
        button = thorpy.Button("back to main menu")
        button.at_unclick = lambda: thorpy.loops.quit_all_loops()
        input_box = thorpy.TextInput("", placeholder="enter your name")
        input_box.on_validation = lambda: self.write_to_leaderboard(input_box.value, self.score)
        box = thorpy.Box([input_box, button])
        box.center_on(self.screen)
        loop = box.get_updater()
        loop.launch()

    def write_to_leaderboard(self, name, score):
        with open("leaderboard.txt", "w") as lb:
            lb.write("{:^40}{:>4}\n".format(name, score))

    def draw_main_menu(self):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        text_surface = font.render(text, False, (44, 0, 62))
        self.screen.blit(text_surface,
                         ((self.width - text_surface.get_width()) // 2,
                          200))
        start_button = thorpy.Button("New game")
        start_button.at_unclick = lambda: self.run_game(done, height, player, width)
    def display_HUD_text(self, text, x, y):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 16)
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))


if __name__ == '__main__':
    game = Game(600, 800)
