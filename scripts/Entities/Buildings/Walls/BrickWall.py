from scripts.constants import *
from scripts.Entities.ABC.Wall import Wall
from scripts.Classes.Registry.EntityRegistry import EntityRegistry

STONE1 = pg.mixer.Sound("sound/pickaxe_1.mp3")
STONE1.set_volume(0.5)
STONE2 = pg.mixer.Sound("sound/ore_done.mp3")
STONE2.set_volume(0.5)


class BrickWall(Wall, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        textures = (load_texture("assets/entities/walls/brick21.png", WALL_SIZE),
                    load_texture("assets/entities/walls/brick22.png", WALL_SIZE))
        super().__init__(code, pos, parent, textures, 300, ("brick_wall", 1), "pickaxe", 10,
                         punch_sound=STONE1, break_sound=STONE2)
