from scripts.constants import *
from PgHelp import *
from math import sin, pi
from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry

TEXTURE_SIZE = TILE_SIZE * Vector(1.5, 1.5)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -0.9)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.8, 0.6)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.1, 0.4)
cashed_sin = [sin(i/10)*2 for i in range(0, int(pi*2*10))]
TEXTURE = load_texture("assets/entities/small_cactus.png", TEXTURE_SIZE)
cashed_texture = [pg.transform.scale(TEXTURE, (TEXTURE_SIZE.x, TEXTURE_SIZE.y + s * 2)) for s in cashed_sin]


class SmallCactus(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, cashed_texture, 100, TEXTURE_OFFSET, "log", "axe", 2, use_hibox=False,
                         hitbox_size=HITBOX_SIZE, hitbox_offset=HITBOX_OFFSET)

    def drop_items(self):

        self.parent.drop_items(self.pos, self.item, 0)

    def draw(self):

        if all(self.do_draw):
            i = 0  # self.parent.animation_counter % int(pi*2*10)
            s = 0  # cashed_sin[i] * 2
            #texture_height = TREE_SIZE.y + s
            #texture = pg.transform.scale(TREE_TEXTURE, (TREE_SIZE.x, texture_height))
            texture = cashed_texture[i]
            self.parent.screen.blit(texture, (self.screen_pos + Vector(0, -s)).as_tuple())
            self.draw_secret_data()

            if self.touching:
                draw_brackets(self.parent.screen, self.rect)
