import pygame
import sys
from pygame.locals import *
from random import *
from os import path

WIDTH = 1000
HEIGHT = 500

FPS = 60

number_of_meteorites = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BSP Game")
fpsClock = pygame.time.Clock()

# load graphics
img_dir = path.join(path.dirname(__file__), 'IMG')
spaceship_img = pygame.image.load(path.join(img_dir, "241-2410583_spaceship-pacific-rim-pixel-art.png")).convert()
meteorite_img = pygame.image.load(path.join(img_dir, "318b773d551baac.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir, "241-2410583_spaceship-pacific-rim-pixel-art2.png")).convert()


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, Color("white"))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spaceship_img, (50, 47))
        self.image.set_colorkey(Color("white"))             # so there is no white rectangle around the image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 5
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[K_LEFT]:
            self.speedx = -5
        if keystate[K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = BulletSpacehip(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        spaceship_bullets.add(bullet)


class BulletSpacehip(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 10))
        self.image.fill(Color("green"))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()                 # delete bullet if it is out of the screen


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (40, 47))
        self.image.set_colorkey(Color("white"))             # so there is no white rectangle around the image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.top = 40
        self.speedx = 0

    def move(self, spaceship):
        self.speedx = 0
        if self.rect.x > spaceship.rect.x:              # "artificial intelligence"
            self.speedx -= randint(1, 2)
        if self.rect.x < spaceship.rect.x:
            self.speedx = randint(1, 2)
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = BulletEnemy(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)


class BulletEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5, 10))
        self.image.fill(Color("red"))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 0:
            self.kill()                 # delete bullet if it is out of the screen


class Meteorite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(meteorite_img, (44, 36))
        self.image.set_colorkey(Color("black"))             # so there is no black rectangle around the image
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, WIDTH - self.rect.width)
        self.rect.y = randrange(-HEIGHT, -50)
        self.speedy = randrange(1, 4)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 40:
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-HEIGHT, -50)
            self.speedy = randrange(1, 4)


# add all objects to the corresponding sprite group
all_sprites = pygame.sprite.Group()
meteorites = pygame.sprite.Group()
spaceship_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

s = Spaceship()
all_sprites.add(s)

e = Enemy()
all_sprites.add(e)

for i in range(number_of_meteorites):
    m = Meteorite()
    all_sprites.add(m)
    meteorites.add(m)

life = 200
score = 0

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                s.shoot()

    # random shooting rate of enemy
        enemy_event = USEREVENT + 1
        enemy_shoot_rate = randint(100, 400)
        pygame.time.set_timer(enemy_event, enemy_shoot_rate)
        if event.type == enemy_event:
            e.shoot()

    if life > 0:
        all_sprites.update()
        e.move(s)

    # check collision between bullets and meteorites (every bullet and meteorite hit gets deleted (-> "True"))
    hits = pygame.sprite.groupcollide(meteorites, spaceship_bullets, True, True)
    for hit in hits:
        score += 10
        m = Meteorite()
        all_sprites.add(m)
        meteorites.add(m)

    # check collision between spaceship and meteorites (create list of all meteorites that hit the spaceship)
    if pygame.sprite.spritecollide(s, meteorites, True):
        life -= 40

    # check collision between spaceship and EnemyBullets
    if pygame.sprite.spritecollide(s, enemy_bullets, True):
        life -= 40

    # check collision between enemy and SpaceshipBullets
    if pygame.sprite.spritecollide(e, spaceship_bullets, True):
        score += 50

    screen.fill(Color("black"))
    all_sprites.draw(screen)

    draw_text(screen, "Score: "+str(score), 20, WIDTH/2, 20)

    # draw life bar
    if life > 0:
        pygame.draw.rect(screen, Color("green"), (WIDTH - 210, 10, life, 20))
        pygame.draw.rect(screen, Color("white"), (WIDTH - 210, 10, 200, 20), 1)

    if life == 0:
        draw_text(screen, "GAME OVER!", 100, WIDTH/2, HEIGHT/2)

    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
sys.exit()
