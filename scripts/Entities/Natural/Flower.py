import pygame as pg
from scripts.Entities.ABC.Building import Building
from scripts.constants import *
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from random import randint
import os

TEXTURE_SIZE = TILE_SIZE * Vector(0.5, 0.5)
TEXTURES = [pg.transform.scale(pg.image.load(os.path.join("assets", "entities", "flowers", file)), TEXTURE_SIZE.as_tuple()) for file in os.listdir(os.path.join("assets", "entities", "flowers"))]
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -1)


class Flower(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURES[randint(0, len(TEXTURES) - 1)],
                         1, TEXTURE_OFFSET, "flower_seeds", None, use_hibox=False)
