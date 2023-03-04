import pygame
from entity import Entity

class Coffin(Entity):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(pos, groups, path, collision_sprites)
        self.direction = pygame.math.Vector2(-1, 0)

    def update(self, dt):
        self.move(dt)
        self.collision('horizontal')

class Cactus(Entity):
    def __init__(self, pos, groups, path, collision_sprites):
        super().__init__(pos, groups, path, collision_sprites)
        self.direction = pygame.math.Vector2(-1, 0)

    def update(self, dt):
        self.move(dt)
        self.collision('horizontal')
