from scripts.constants import *
from scripts.Entities.ABC.Sapling import Sapling
from scripts.Entities.Natural.Fungus import Fungus
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class MushroomSapling(Sapling, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(0.5, 0.5)
        texture = load_texture("assets/entities/mushroom_sapling.png", texture_size)

        super().__init__(code, pos, parent, texture, Fungus, 20, "mushroom_sapling")
