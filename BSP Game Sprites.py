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

# ----------------------------------------- MODEL ---------------------------------------------------------------------

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(spaceship_img, (50, 47))
        self.image.set_colorkey(Color("white"))             # so there is no white rectangle around the image
        self.rect = self.image.get_rect()
        self.radius = 23                                    # improves collision
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
        bullet = BulletSpaceship(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        spaceship_bullets.add(bullet)

    def reset(self):
        for bullet in spaceship_bullets:
            spaceship_bullets.remove(bullet)
            bullet.image = pygame.Surface((0, 0))
        self.rect.centerx = WIDTH/2


class BulletSpaceship(pygame.sprite.Sprite):
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
        self.image = pygame.transform.scale(enemy_img, (50, 47))
        self.image.set_colorkey(Color("white"))             # so there is no white rectangle around the image
        self.rect = self.image.get_rect()
        self.radius = 23                                    # improves collision
        self.rect.centerx = randint(50, WIDTH - 50)
        self.rect.top = 40
        self.speedx = 0

    def move(self, spaceship):
        self.speedx = 0
        if self.rect.x > spaceship.rect.x:              # "artificial intelligence"
            self.speedx -= randint(1, 2)
        if self.rect.x < spaceship.rect.x:
            self.speedx += randint(1, 2)
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = BulletEnemy(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullets.add(bullet)

    def reset(self):
        for bullet in enemy_bullets:
            enemy_bullets.remove(bullet)
            bullet.image = pygame.Surface((0, 0))
        self.rect.centerx = randint(50, WIDTH - 50)


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
        self.radius = 19                                    # improves collision
        self.rect.x = randrange(0, WIDTH - self.rect.width)
        self.rect.y = randrange(-HEIGHT, -50)
        self.speedy = randrange(1, 4)
        self.speedx = randrange(-4, 4)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 40 or self.rect.right < -40 or self.rect.left > WIDTH + 40:
            self.rect.x = randrange(0, WIDTH - self.rect.width)
            self.rect.y = randrange(-HEIGHT, -50)
            self.speedy = randrange(1, 4)
            self.speedx = randrange(-4, 4)


# ----------------------------------------- VIEW ----------------------------------------------------------------------

# load graphics
img_dir = path.join(path.dirname(__file__), 'IMG')
spaceship_img = pygame.image.load(path.join(img_dir, "241-2410583_spaceship-pacific-rim-pixel-art.png")).convert()
meteorite_img = pygame.image.load(path.join(img_dir, "318b773d551baac.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir, "241-2410583_spaceship-pacific-rim-pixel-art2.png")).convert()
background_img = pygame.image.load(path.join(img_dir, "background2.png")).convert()
background_img_rect = background_img.get_rect()


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, Color("white"))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)


def GameMenu():
    title = pygame.image.load(path.join(img_dir, "BSP-Asteroids-Game.png")).convert_alpha()
    title = pygame.transform.scale(title, (900, 100))
    background = pygame.image.load(path.join(img_dir, "background.png")).convert()
    background_rect = background.get_rect()

    # show game instructions
    arrow_keys = pygame.image.load(path.join(img_dir, "arrowkeys.png")).convert_alpha()
    arrow_keys = pygame.transform.scale(arrow_keys, (166, 113))
    spacebar = pygame.image.load(path.join(img_dir, "spacebar.png")).convert_alpha()
    spacebar = pygame.transform.scale(spacebar, (330, 53))

    screen.blit(background, background_rect)
    screen.blit(title, (40, 20))
    screen.blit(arrow_keys, (WIDTH / 2 - 50, HEIGHT / 2))
    screen.blit(spacebar, (WIDTH / 2 - 50, HEIGHT / 2 + 160))
    draw_text(screen, "PRESS [ENTER] TO START", 35, WIDTH / 2, HEIGHT / 4 + 40)
    draw_text(screen, "PRESS [E] TO EXIT", 35, WIDTH / 2, HEIGHT / 4 + 80)

    # game instructions
    draw_text(screen, "MOVE:", 35, WIDTH / 2 - 150, HEIGHT / 2 + 90)
    draw_text(screen, "SHOOT:", 35, WIDTH / 2 - 150, HEIGHT / 2 + 190)

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == K_RETURN:
                break
            elif event.key == K_e:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


def WinningScreen():
    title = pygame.image.load(path.join(img_dir, "BSP-Asteroids-Game.png")).convert_alpha()
    title = pygame.transform.scale(title, (900, 100))
    background = pygame.image.load(path.join(img_dir, "background.png")).convert()
    background_rect = background.get_rect()

    screen.blit(background, background_rect)
    screen.blit(title, (40, 20))
    draw_text(screen, "PRESS [ENTER] TO RESTART", 35, WIDTH / 2, HEIGHT / 4 + 40)
    draw_text(screen, "PRESS [E] TO EXIT", 35, WIDTH / 2, HEIGHT / 4 + 80)
    draw_text(screen, "YOU WON THE GAME!", 120, WIDTH / 2, HEIGHT / 2 + 100)

    s.reset()
    e.reset()

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == K_RETURN:
                break
            elif event.key == K_e:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


def LosingScreen():
    title = pygame.image.load(path.join(img_dir, "BSP-Asteroids-Game.png")).convert_alpha()
    title = pygame.transform.scale(title, (900, 100))
    background = pygame.image.load(path.join(img_dir, "background.png")).convert()
    background_rect = background.get_rect()

    screen.blit(background, background_rect)
    screen.blit(title, (40, 20))
    draw_text(screen, "PRESS [ENTER] TO RESTART", 35, WIDTH / 2, HEIGHT / 4 + 40)
    draw_text(screen, "PRESS [E] TO EXIT", 35, WIDTH / 2, HEIGHT / 4 + 80)
    draw_text(screen, "GAME OVER!", 150, WIDTH / 2, HEIGHT / 2 + 100)

    s.reset()
    e.reset()

    pygame.display.update()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            if event.key == K_RETURN:
                break
            elif event.key == K_e:
                pygame.quit()
                sys.exit()
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()


# ----------------------------------------- CONTROLLER ----------------------------------------------------------------

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

spaceship_life = 200
enemy_life = 200
score = 0

# main loop
show_menu = True
running = True
while running:
    if show_menu:
        GameMenu()
        show_menu = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        keystate = pygame.key.get_pressed()
        if keystate[K_SPACE]:
            s.shoot()

    # random shooting rate of enemy
        enemy_event = USEREVENT + 1
        enemy_shoot_rate = randint(80, 200)
        if e.rect.x == s.rect.x:                        # shoot rate is very high when the enemy is above the player
            enemy_shoot_rate = 50                       # to prevent that the player easily wins the game
        pygame.time.set_timer(enemy_event, enemy_shoot_rate)
        if event.type == enemy_event:
            e.shoot()

    if spaceship_life > 0 and enemy_life > 0:
        e.move(s)
        all_sprites.update()

    # check collision between bullets and meteorites (every bullet and meteorite hit gets deleted (-> "True"))
    hits = pygame.sprite.groupcollide(meteorites, spaceship_bullets, True, True, pygame.sprite.collide_circle)
    for hit in hits:
        score += 10
        m = Meteorite()
        all_sprites.add(m)
        meteorites.add(m)

    # check collision between spaceship and meteorites ("pygame.sprite.collide_circle" improves the collision)
    if pygame.sprite.spritecollide(s, meteorites, True, pygame.sprite.collide_circle):
        spaceship_life -= 40

    # check collision between spaceship and EnemyBullets
    if pygame.sprite.spritecollide(s, enemy_bullets, True, pygame.sprite.collide_circle):
        spaceship_life -= 40

    # check collision between enemy and SpaceshipBullets
    if pygame.sprite.spritecollide(e, spaceship_bullets, True, pygame.sprite.collide_circle):
        score += 50
        enemy_life -= 20

    # check collision between enemy bullet and spaceship bullet
    pygame.sprite.groupcollide(enemy_bullets, spaceship_bullets, True, True)

    screen.blit(background_img, background_img_rect)
    all_sprites.draw(screen)

    draw_text(screen, "Score: "+str(score), 20, WIDTH/2, 20)

    # life bar of spaceship
    if spaceship_life >= 0:
        pygame.draw.rect(screen, Color("green"), (WIDTH - 210, 10, spaceship_life, 20))
        pygame.draw.rect(screen, Color("white"), (WIDTH - 210, 10, 200, 20), 1)

    if spaceship_life == 0:
        LosingScreen()
        spaceship_life = 200
        enemy_life = 200
        score = 0

    # life bar of enemy
    if enemy_life >= 0:
        pygame.draw.rect(screen, Color("red"), (10, 10, enemy_life, 20))
        pygame.draw.rect(screen, Color("white"), (10, 10, 200, 20), 1)

    if enemy_life == 0 or score == 10000:
        WinningScreen()
        spaceship_life = 200
        enemy_life = 200
        score = 0

    pygame.display.update()
    fpsClock.tick(FPS)

pygame.quit()
sys.exit()
