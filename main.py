import time
import pygame
import random
from pygame.transform import scale

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 100, 100)
        self.images = []
        self.index = 0
        for i in range(8):
            image = scale(pygame.image.load(f'explosion/tile00{i}.png'), (100, 100))
            self.images.append(image)

    def draw(self, screen):
        if self.index < 32:
            screen.blit(self.images[self.index // 4], (self.rect.x, self.rect.y))
            self.index += 1
        else:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = scale(pygame.image.load('orange.png'), (50, 50))
        self.rect = pygame.Rect(x, y, 50, 50)
        self.yvel = 5

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += self.yvel

        if self.rect.y > 900:
            self.kill()

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 100, 100)
        self.image = scale(pygame.image.load('cheburashka.png'), (100, 100))
        self.xvel = 0
        self.yvel = 0
        self.score = 0
        self.explosions = []

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        for explosion in self.explosions:
            explosion.draw(screen)

    def update(self, left, right, up, down, asteroids):
        if left:
            self.xvel -= 3
        if right:
            self.xvel += 3
        if up:
            self.yvel -= 3
        if down:
            self.yvel += 3
        if not (left or right or up or down):
            self.xvel = 0
            self.yvel = 0
        self.rect.x += self.xvel
        self.rect.y += self.yvel

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.x > 750:
            self.rect.x = 750
        if self.rect.y > 500:
            self.rect.y = 500

        for asteroid in asteroids:
            if self.rect.colliderect(asteroid.rect):
                self.score += 1

                rx = random.randint(-5, 40)
                ry = random.randint(-5, 40)
                explosion = Explosion(self.rect.x + rx, self.rect.y + ry)
                self.explosions.append(explosion)
                asteroid.kill()



pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('ChebuRun Pro')
sky = scale(pygame.image.load('beach.jpg'), (800, 600))
ship = Spaceship(400, 400)
player_rect = screen.get_rect()
clock = pygame.time.Clock()

left = False
right = False
up = False
down = False
asteroids = pygame.sprite.Group()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans Ms', 30)
state = 'game'

starttime = time.time()

while True:
    if state == 'game':
        if random.randint(1, 1000) > 900:
            asteroid_x = random.randint(-100, 700)
            asteroid_y = -100
            asteroid = Asteroid(asteroid_x, asteroid_y)
            asteroids.add(asteroid)


        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                right = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                down = True

            if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                left = False
            if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                down = False

            if e.type == pygame.QUIT:
                raise SystemExit("QUIT")

        screen.blit(sky, (0, 0))
        ship.update(left, right, up, down, asteroids)
        ship.draw(screen)

        if ship.score < 0:
            endtime = time.time()
            state = 'gameover'

        for asteroid in asteroids:
            asteroid.update()
            asteroid.draw(screen)

        texturface = font.render(f'Апельсины: {ship.score}', False, (255, 255, 255))
        screen.blit(texturface, (20, 20))
    if state == "gameover":
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise SystemExit("QUIT")
        playtime = endtime - starttime
        playtime = round(playtime)
        gameover = font.render('GAME OVER', False, (255,255,255))
        timeplay = font.render(f'You play in this game {playtime} seconds!', False, (255, 255, 255))
        screen.blit(gameover, (20, 200))
        screen.blit(timeplay, (20, 400))


    pygame.display.update()
    clock.tick(60)