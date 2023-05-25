import sys
import thorpy
import thorpy.loops
import pygame
import os
import time
import random
from Invader import Invader
from Player import Player
from Rockets import Rocket, InvaderRocket
from Bunker import Bunker
from MysteryShip import MysteryShip
from GameState import GameState
from GameResources import GameResources


class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.game_resources = GameResources()
        self.rocket_sound = pygame.mixer.Sound(
            os.path.join(
                self.game_resources.sounds_folder,
                'rocket.mp3'))
        self.game_over_sound = pygame.mixer.Sound(
            os.path.join(
                self.game_resources.sounds_folder,
                'game_over.mp3'))
        self.win_sound = pygame.mixer.Sound(
            os.path.join(
                self.game_resources.sounds_folder,
                'win.mp3'))
        thorpy.init(self.screen)

    def run_game(self, height, width, difficulty):
        game_state = GameState(height, width)
        thorpy.loops.quit_all_loops()
        self.screen.fill((0, 0, 0))
        self.generate_invaders(difficulty, game_state)
        self.generate_bunkers(5 - difficulty, game_state)
        pygame.mixer.music.load(
            os.path.join(
                self.game_resources.sounds_folder,
                'music.mp3'))
        pygame.mixer.music.play(-1)
        player = Player(self.game_resources, width / 2, height - 100, game_state)
        while not game_state.done:
            self.display_HUD_text(f"score: {game_state.score}", 10, 0)
            self.display_HUD_text(f"health: {player.health}", 10, 20)
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                player.rect.x -= 2 if player.rect.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                player.rect.x += 2 if player.rect.x < width - 20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN and not game_state.lost:
                    if event.key == pygame.K_SPACE:
                        game_state.rockets.append(Rocket(self.game_resources,
                                                         game_state,
                                                         player.rect.center[0],
                                                         player.rect.center[1]))
                        self.rocket_sound.play()
                    if event.key == pygame.K_ESCAPE:
                        self.draw_pause()

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            if len(game_state.invaders) == 0:
                game_state.done = True
                game_state.won = True
            else:
                if len(game_state.invaders) != 0 and len(game_state.invaders[-1]) == 0:
                    game_state.invaders.pop()

                if random.random() > 0.99 - difficulty * 0.005:
                    shooting_invader = random.choice(game_state.invaders[-1])
                    invader_rocket = InvaderRocket(self.game_resources,
                                                   game_state,
                                                   shooting_invader.rect.center[0],
                                                   shooting_invader.rect.center[1])
                    game_state.invader_rockets.append(invader_rocket)
                    self.rocket_sound.play()

                if not game_state.mystery_ship_flying and random.random() > 0.999:
                    MysteryShip(self.game_resources, game_state)
                    game_state.mystery_ship_flying = True

            if not game_state.lost:
                game_state.all_sprites.update()
                game_state.all_sprites.draw(self.screen)

        pygame.mixer.music.stop()
        if game_state.lost:
            self.game_over_sound.play()
            self.display_game_over_text("DEFEAT", game_state)
        elif game_state.won:
            self.win_sound.play()
            self.display_game_over_text("VICTORY ACHIEVED", game_state)

    def generate_invaders(self, difficulty, game_state):
        vertical_margin = 30
        horizontal_margin = 150
        max_rows = difficulty*2
        width = 50
        row = -1
        for y in range(horizontal_margin, int(self.height / 2), width):
            row += 1
            if row >= max_rows:
                break
            invaders_row = []
            for x in range(vertical_margin, self.width - vertical_margin, width):
                invader = Invader(self.game_resources, x, y, row, difficulty, game_state)
                invaders_row.append(invader)
            game_state.invaders.append(invaders_row)

    def generate_bunkers(self, number_of_bunkers, game_state):
        vertical_margin = 30
        margin = self.width // number_of_bunkers
        for x in range(vertical_margin, self.width - vertical_margin, margin):
            Bunker(self.game_resources, x, self.height - 200, game_state)

    def draw_pause(self):
        resume_button = thorpy.Button("resume")
        resume_button.at_unclick = lambda: thorpy.loops.quit_current_loop()
        back_button = thorpy.Button("back to main menu")
        back_button.at_unclick = lambda: self.draw_main_menu()
        box = thorpy.TitleBox("Paused", [resume_button, back_button])
        box.center_on(self.screen)
        box.get_updater().launch()

    def display_game_over_text(self, text, game_state):
        thorpy.loops.quit_all_loops()
        self.screen.fill((0, 0, 0))
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        text_surface = font.render(text, False, (44, 0, 62))
        self.screen.blit(text_surface,
                         ((self.width - text_surface.get_width()) // 2,
                          self.height // 2 - 100))
        button = thorpy.Button("back to main menu")
        button.at_unclick = lambda: self.draw_main_menu()
        input_box = thorpy.TextInput("", placeholder="enter your name")
        input_box.on_validation = lambda: self.write_to_leaderboard(input_box.value, game_state.score)
        box = thorpy.Box([input_box, button])
        box.center_on(self.screen)
        loop = box.get_updater()
        loop.launch()

    def write_to_leaderboard(self, name, score):
        if name != "":
            with open("leaderboard.txt", "a") as lb:
                lb.write("{:^40}{:>4}\n".format(name, score))

    def draw_main_menu(self):
        thorpy.loops.quit_all_loops()
        self.screen.fill((0, 0, 0))
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        text_surface = font.render("Space Invaders", False, (44, 0, 62))
        self.screen.blit(text_surface,
                         ((self.width - text_surface.get_width()) // 2,
                          200))
        start_button = thorpy.Button("New game")
        start_button._at_click = lambda: self.draw_difficulty_selection()
        leaderboard_button = thorpy.Button("Leaderboard")
        leaderboard_button._at_click = lambda: self.draw_leaderboard()
        quit_button = thorpy.Button("Quit")
        quit_button.at_unclick = lambda: sys.exit(0)
        box = thorpy.Box([start_button, leaderboard_button, quit_button])
        box.center_on(self.screen)
        box.get_updater().launch()

    def display_HUD_text(self, text, x, y):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 16)
        text_surface = font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))

    def draw_leaderboard(self):
        top10_list = []
        thorpy.loops.quit_all_loops()
        self.screen.fill((0, 0, 0))
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        text_surface = font.render("Leaderboard", False, (44, 0, 62))
        self.screen.blit(text_surface,
                         ((self.width - text_surface.get_width()) // 2,
                          200))
        with open("leaderboard.txt") as lb:
            top10_list = lb.read().split('\n')
        top10_list = top10_list[:-1]
        top10_list = sorted(top10_list, key=lambda x: int(x.split()[-1]), reverse=True)
        leaderboard_start = 300
        leader_font = font = pygame.font.SysFont('Arial', 20)
        for i in range(10):
            if i >= len(top10_list):
                break
            leader_text = font.render(f"{i+1}. " + top10_list[i], True, (100, 0, 200))
            self.screen.blit(leader_text,
                             ((self.width - text_surface.get_width()) // 2,
                              leaderboard_start + i*20))

        button = thorpy.Button("back to main menu")
        button._at_click = lambda: self.draw_main_menu()
        button.rect.center = (self.width // 2, self.height - 200)
        button.get_updater().launch()

    def draw_difficulty_selection(self):
        thorpy.loops.quit_all_loops()
        self.screen.fill((0, 0, 0))
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        text_surface = font.render("Chose difficulty", False, (44, 0, 62))
        self.screen.blit(text_surface,
                         ((self.width - text_surface.get_width()) // 2,
                          200))
        very_easy = thorpy.Button("Very easy")
        very_easy.at_unclick = lambda: self.run_game(self.height, self.width, 1)
        easy = thorpy.Button("Easy")
        easy.at_unclick = lambda: self.run_game(self.height, self.width, 2)
        normal = thorpy.Button("Normal")
        normal.at_unclick = lambda: self.run_game(self.height, self.width, 3)
        hard = thorpy.Button("Hard")
        hard.at_unclick = lambda: self.run_game(self.height, self.width, 4)
        box = thorpy.Box([very_easy, easy, normal, hard])
        box.center_on(self.screen)
        time.sleep(0.1)
        box.get_updater().launch()


if __name__ == '__main__':
    game = Game(600, 800)
    game.draw_main_menu()
