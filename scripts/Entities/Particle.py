import pygame as pg
from scripts.constants import *
from PgHelp import *


class Particle:

    def __init__(self, code, pos, parent, start_vel: Vector, lifetime: int, texture: pg.Surface, gravity: bool = True,
                 rotation_per_update: int = 0, size_factor: Vector = Vector(0, 0), delta_transparency: float = 0,
                 delta_size_per_update: Vector = Vector(0, 0)):

        self.code = code
        self.pos = pos
        self.parent = parent
        self.velocity = start_vel
        self.time_left = lifetime
        self.texture = texture
        self.gravity = gravity
        self.rotation_per_update = rotation_per_update
        self.delta_size_per_update = delta_size_per_update
        self.size = from_iterable(texture.get_size()) + size_factor
        self.delta_trancparency = delta_transparency
        self.angle = 0
        self.ydelta = 0
        self.tobeddeleted = False
        self.screen_pos = Vector(0, 0)

    def update(self):

        self.time_left -= 1
        if self.time_left <= 0:
            self.tobeddeleted = True
            return

        self.pos += self.velocity
        self.ydelta += 0.05
        if self.gravity: self.velocity.y += self.ydelta

        self.angle += self.rotation_per_update
        self.size += self.delta_size_per_update
        self.texture.set_alpha(self.texture.get_alpha() + self.delta_trancparency)

        self.screen_pos = self.pos + self.parent.offset + from_iterable(self.texture.get_size()) * Vector(0.5, 0.5)

    def draw(self):

        texture = pg.transform.rotate(pg.transform.scale(self.texture, self.size.as_tuple()), self.angle)
        screen.blit(texture, self.screen_pos.as_tuple())
