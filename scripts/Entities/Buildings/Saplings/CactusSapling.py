from scripts.constants import *
from scripts.Entities.ABC.Sapling import Sapling
from scripts.Entities.Natural.Cactus import Cactus
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class CactusSapling(Sapling, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(0.5, 0.5)
        texture = load_texture("assets/entities/cactus_sapling.png", texture_size)

        super().__init__(code, pos, parent, texture, Cactus, 19, "cactus_sapling")
