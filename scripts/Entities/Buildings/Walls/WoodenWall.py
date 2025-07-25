from scripts.constants import *
from scripts.Entities.ABC.Wall import Wall
from scripts.Classes.Registry.EntityRegistry import EntityRegistry

WOOD1 = pg.mixer.Sound("sound/axe.mp3")
WOOD1.set_volume(0.5)


class WoodenWall(Wall, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        textures = (load_texture("assets/entities/walls/wood 1.png", WALL_SIZE),
                    load_texture("assets/entities/walls/wood.png", WALL_SIZE))
        super().__init__(code, pos, parent, textures, 100, ("wooden_wall", 1), "axe", 9,
                         punch_sound=WOOD1)
