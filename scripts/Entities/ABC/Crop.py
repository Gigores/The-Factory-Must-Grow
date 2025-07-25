from scripts.Entities.ABC.Building import Building
from scripts.constants import *
from random import randint


class Crop(Building):

    def __init__(self, code, pos, parent, textures: tuple[pg.Surface, pg.Surface, pg.Surface, pg.Surface], growth_time: int, seed_item: str, crop_item: str, class_id: int = 0):

        texture_offset = TILE_SIZE * Vector(-0.5, -1)
        hitbox_size = TILE_SIZE
        hitbox_offset = TILE_SIZE * Vector(0, 0.5)
        touch_hitbox_size = TILE_SIZE
        touch_hitbox_offset = TILE_SIZE * Vector(0, 0.5)

        rpos = Vector(pos.x // TILE_SIZE.x * TILE_SIZE.x + TILE_SIZE.x / 2,
                      pos.y // TILE_SIZE.y * TILE_SIZE.y + TILE_SIZE.y / 2)

        super().__init__(code, rpos, parent, textures, 1, texture_offset, seed_item, "hoe", class_id, use_hibox=False, collider_hitbox_size=touch_hitbox_size, collider_hitbox_offset=touch_hitbox_offset,
                         hitbox_size=hitbox_size, hitbox_offset=hitbox_offset)

        self.crop_item = crop_item
        self.growth_time = growth_time
        self.growth_level = 0
        self.timer = 0

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)
        if not preview_mode:
            self.timer += 1
            if self.timer >= self.growth_time / len(self.texture) and self.growth_level < len(self.texture) - 1:
                self.timer = 0
                self.growth_level += 1

    def select_texture(self) -> pg.Surface:

        return self.texture[self.growth_level]

    def drop_items(self):

        if self.growth_level >= len(self.texture) - 1:
            self.parent.drop_items(self.pos, self.item, randint(1, 2))
            self.parent.drop_items(self.pos, self.crop_item, randint(2, 3))
        else:
            super().drop_items()

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "growth_level": self.growth_level,
            "timer": self.timer,
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.growth_level = data["growth_level"]
        self.timer = data["timer"]
