import pygame
import os
import time

class Game:
    screen = None
    aliens = []
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
        generator = Generator(self)
        rocket = None

        while not done:
            if len(self.aliens) == 0:
                self.displayText("VICTORY ACHIEVED")

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

            if len(self.aliens[-1]) == 0:
                self.aliens.pop()
            if self.aliens[-1][0].rect.y > height-100:
                self.lost = True
                self.displayText("YOU DIED")

            for rocket in self.rockets:
                rocket.draw()

            if not self.lost:
                self.all_sprites.update()
                self.all_sprites.draw(self.screen)

    def displayText(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 50)
        textsurface = font.render(text, False, (44, 0, 62))
        self.screen.blit(textsurface, (110, 160))


class Alien(pygame.sprite.Sprite):
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
                game.aliens[self.row].remove(self)
                game.all_sprites.remove(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, game: Game, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(game.image_folder, 'player.png')).convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (game.width / 2, game.height / 2)
        self.game = game
        self.rect.x = x
        self.rect.y = y

    #def draw(self):
        #pygame.draw.rect(self.game.screen,
                         #(210, 250, 251),
                         #pygame.Rect(self.x, self.y, 8, 5))


class Generator:
    def __init__(self, game):
        vertical_margin = 30
        horizontal_margin = 150
        width = 50
        row = -1
        for y in range(horizontal_margin, int(game.height / 2), width):
            row += 1
            invaders_row = []
            for x in range(vertical_margin, game.width - vertical_margin, width):
                alien = Alien(game, x, y, row)
                invaders_row.append(alien)
                game.all_sprites.add(alien)
            game.aliens.append(invaders_row)


        # game.aliens.append(Alien(game, 280, 50))


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


if __name__ == '__main__':
    game = Game(600, 800)