from scripts.constants import *
from PgHelp import *
from math import sin, pi
from random import randint
from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry

TEXTURE_SIZE = TILE_SIZE * Vector(2, 3)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.9)
cashed_sin = [sin(i/10)*2 for i in range(0, int(pi*2*10))]
TREE_TEXTURES = [
    load_texture("assets/entities/fungus1.png", TEXTURE_SIZE),
    load_texture("assets/entities/fungus2.png", TEXTURE_SIZE),
    load_texture("assets/entities/fungus3.png", TEXTURE_SIZE),
]
cashed_textures = [
    [pg.transform.scale(TREE_TEXTURES[0], (TEXTURE_SIZE.x, TEXTURE_SIZE.y + s * 2)) for s in cashed_sin],
    [pg.transform.scale(TREE_TEXTURES[1], (TEXTURE_SIZE.x, TEXTURE_SIZE.y + s * 2)) for s in cashed_sin],
    [pg.transform.scale(TREE_TEXTURES[2], (TEXTURE_SIZE.x, TEXTURE_SIZE.y + s * 2)) for s in cashed_sin],
]


class Fungus(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, cashed_textures, 100, TEXTURE_OFFSET, "log", "axe", 3, hitbox_size=TEXTURE_SIZE,
                         #touching_hitbox_size=HITBOX_SIZE, touching_hitbox_offset=HITBOX_OFFSET
                         texture_size=from_iterable(TREE_TEXTURES[0].get_size()), use_hibox=False)
        self.texture_id = randint(0, 2)

    def drop_items(self):

        self.parent.drop_items(self.pos, self.item, 2)
        self.parent.drop_items(self.pos, "mushroom_sapling", randint(1, 2))

    def draw(self):

        if all(self.do_draw):
            i = 0  # self.parent.animation_counter % int(pi*2*10)
            s = 0  # cashed_sin[i] * 2
            texture = cashed_textures[self.texture_id][i]
            self.parent.screen.blit(texture, (self.screen_pos + Vector(0, -s)).as_tuple())
            self.draw_secret_data()

            if self.touching:
                draw_brackets(self.parent.screen, self.rect)

