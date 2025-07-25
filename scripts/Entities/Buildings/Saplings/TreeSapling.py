from scripts.constants import *
from scripts.Entities.ABC.Sapling import Sapling
from scripts.Entities.Natural.Tree import Tree
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class TreeSapling(Sapling, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(0.5, 0.5)
        texture = load_texture("assets/entities/tree_sapling.png", texture_size)

        super().__init__(code, pos, parent, texture, Tree, 18, "tree_sapling")
