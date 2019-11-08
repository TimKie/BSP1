import unittest
import pygame
from pygame.locals import *

WIDTH = 1000
HEIGHT = 500

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.set_colorkey(Color("white"))             # so there is no white rectangle around the image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 5
        self.speedx = 0


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.set_colorkey(Color("white"))             # so there is no white rectangle around the image
        self.rect = self.image.get_rect()
        self.rect.centerx = 100
        self.rect.top = 40
        self.speedx = 0

    def move(self, spaceship):
        self.speedx = 0
        if self.rect.x > spaceship.rect.x:              # "artificial intelligence"
            self.speedx -= 2
            return self.speedx
        if self.rect.x < spaceship.rect.x:
            self.speedx += 2
            return self.speedx
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


class Test(unittest.TestCase):
    def test_move(self):
        s = Spaceship()
        e = Enemy()
        self.assertEqual(e.move(s), 2, f'Enemy moved {e.move(s)} rather than 2')    # message if test fails


if __name__ == '__main__':
    unittest.main()
