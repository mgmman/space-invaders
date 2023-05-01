import pygame
import os
import time
import random

class Game:
    screen = None
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
        done = False

        player = Player(self, width / 2, height-100)
        self.all_sprites.add(player)
        self.generate_invaders()
        rocket = None

        self.run_game(done, height, player, width)

    def run_game(self, done, height, player, width):
        while not done:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                player.rect.x -= 2 if player.rect.x > 20 else 0
            elif pressed[pygame.K_RIGHT]:
                player.rect.x += 2 if player.rect.x < width - 20 else 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.lost:
                    self.rockets.append(Rocket(self, player.rect.x, player.rect.y))

            pygame.display.flip()
            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            if len(self.invaders) == 0:
                self.displayText("VICTORY ACHIEVED")
            else:
                if len(self.invaders[-1]) == 0:
                    self.invaders.pop()

                if self.invaders[-1][0].rect.y > height - 100 or player.health <= 0:
                    self.lost = True
                    self.displayText("DEFEAT")

                if random.random() > 0.98:
                    shooting_invader = random.choice(self.invaders[-1])
                    invader_rocket = InvaderRocket(self, shooting_invader.rect.center[0], shooting_invader.rect.center[1])
                    self.invader_rockets.append(invader_rocket)

            if not self.lost:
                self.all_sprites.update()
                self.all_sprites.draw(self.screen)

                for rocket in self.rockets:
                    rocket.draw()

                for rocket in self.invader_rockets:
                    rocket.draw();

    def generate_invaders(self):
        vertical_margin = 30
        horizontal_margin = 150
        width = 50
        row = -1
        for y in range(horizontal_margin, int(self.height / 2), width):
            row += 1
            invaders_row = []
            for x in range(vertical_margin, self.width - vertical_margin, width):
                invader = Invader(self, x, y, row)
                invaders_row.append(invader)
                self.all_sprites.add(invader)
            self.invaders.append(invaders_row)

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))


class Invader(pygame.sprite.Sprite):
    def __init__(self, game, x, y, row):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(game.image_folder, 'invader.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.timer = time.time()
        self.rect.x = x
        self.row = row
        self.rect.y = y
        self.game = game
        self.size = 30

    def update(self):
        if time.time() - self.timer > 1:
            self.timer = time.time()
            self.rect.y += 3
        self.check_collision(self.game)


    def check_collision(self, game):
        for rocket in game.rockets:
            if (self.rect.x + self.size > rocket.x > self.rect.x - self.size and
                    self.rect.y + self.size > rocket.y > self.rect.y - self.size):
                game.rockets.remove(rocket)
                game.invaders[self.row].remove(self)
                game.all_sprites.remove(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, game: Game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(game.image_folder, 'player.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.game = game
        self.health = 3
        self.size = 30
        self.rect.x = x
        self.rect.y = y

    def update(self):
        for rocket in self.game.invader_rockets:
            if (self.rect.x + self.size > rocket.x > self.rect.x - self.size and
                    self.rect.y + self.size > rocket.y > self.rect.y - self.size):
                self.game.invader_rockets.remove(rocket)
                self.health -= 1



class Rocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (254, 52, 110),
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y -= 2

class InvaderRocket:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.game = game

    def draw(self):
        pygame.draw.rect(self.game.screen,
                         (100, 255, 50),
                         pygame.Rect(self.x, self.y, 2, 4))
        self.y += 2

if __name__ == '__main__':
    game = Game(600, 800)