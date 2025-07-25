from scripts.constants import *
from PgHelp import *
from random import randint
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Managers.GameAssets import items


SIZE = Vector(TILE_SIZE.x / 2, TILE_SIZE.y / 2)
TEXTURES = [load_texture(os.path.join("assets/entities/pebbles", file), SIZE) for file in os.listdir("assets/entities/pebbles")]


class Pebble(metaclass=EntityRegistry):

    def __init__(self, code: any, pos: Vector, parent, _type: str = "classic"):

        self.code = code
        self.parent = parent
        self.pos = pos
        self.tobeddeleted = False

        self.angle = randint(-180, 180)
        self.texture_id = randint(0, 4) + 5 * int(_type == "sand")
        self.texture = pg.transform.rotate(TEXTURES[self.texture_id], self.angle)
        self.screen_pos = Vector(0, 0)
        self.__texture_offset = Vector(self.texture.get_width() / 2, self.texture.get_height() / 2)
        self.do_draw = ()
        self.rect = self.texture.get_rect()
        self.touching = False

    def update(self):

        self.screen_pos = self.pos + self.parent.offset - self.__texture_offset
        self.do_draw = (
            self.screen_pos.x < RESOLUTION.x,
            self.screen_pos.x - TREE_SIZE.x > -TREE_SIZE.x * 2,
            self.screen_pos.y < RESOLUTION.y,
            self.screen_pos.y - TREE_SIZE.y > -TREE_SIZE.y * 2,
        )
        if any(self.do_draw):

            self.rect.x = self.screen_pos.x
            self.rect.y = self.screen_pos.y
            self.touching = self.rect.collidepoint(get_mouse_pos()) and self.parent.active_ui_id is None

            player_item_name = self.parent.inventory.n[self.parent.player.inventory_cursor]
            player_item = items.setdefault(player_item_name, None)

            if self.touching and pg.mouse.get_pressed()[0] and (player_item is None or player_item_name == "stone"):

                self.parent.inventory.append("stone")
                self.tobeddeleted = True

    def draw(self):

        if any(self.do_draw):

            screen.blit(self.texture, self.screen_pos.as_tuple())

            if self.touching:
                draw_brackets(screen, self.rect)

    def dumb(self):

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "texture_id": self.texture_id,
            "texture_angle": self.angle
        }

    def load(self, data: dict):

        self.pos = Vector(data["pos"][0], data["pos"][1])
        self.angle = data["texture_angle"]
        self.texture_id = data["texture_id"]
        self.texture = pg.transform.rotate(TEXTURES[self.texture_id], self.angle)
        self.__texture_offset = Vector(self.texture.get_width() / 2, self.texture.get_height() / 2)
