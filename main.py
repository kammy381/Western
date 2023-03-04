import pygame
import sys
from settings import *
from player import Player
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from sprite import Sprite, Bullet
from monster import Coffin, Cactus


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load('./graphics/other/bg.png').convert()

    def customize_draw(self, player):
        self.offset.x = player.rect.centerx - WINDOW_WIDTH /2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT/2

        self.display_surface.blit(self.bg, (-self.offset))
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center = sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Western')
        self.clock = pygame.time.Clock()
        self.bullet_surf = pygame.image.load("./graphics/other/particle.png").convert_alpha()

        # groups
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.setup()

    def create_bullet(self, pos, direction):
        Bullet(pos, direction, self.bullet_surf, [self.all_sprites, self.bullets])

    def setup(self):
        tmx_map = load_pygame("./data/map.tmx")
        for x, y, surf in tmx_map.get_layer_by_name('Fence').tiles():
            Sprite((64*x, 64*y), surf, [self.all_sprites, self.obstacles])

        # objects
        for obj in tmx_map.get_layer_by_name('Object'):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacles])

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, PATHS['player'], self.obstacles, self.create_bullet)
            if obj.name == 'Coffin':
                self.coffin = Coffin((obj.x, obj.y), self.all_sprites, PATHS['coffin'], self.obstacles)
            if obj.name == 'Cactus':
                self.coffin = Cactus((obj.x, obj.y), self.all_sprites, PATHS['cactus'], self.obstacles)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            # update groups
            self.all_sprites.update(dt)

            # draw
            self.display_surface.fill('black')
            self.all_sprites.customize_draw(self.player)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
