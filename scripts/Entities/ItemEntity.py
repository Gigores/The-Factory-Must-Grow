from scripts.constants import *
from PgHelp import *
from math import sin
from scripts.Managers.GameAssets import items


ITEM_SIZE = TILE_SIZE / Vector(2, 2)


class ItemEntity:

    def __init__(self, code, pos: Vector, parent, item_name: str = "apple", velocity: Vector = Vector(0, 0), animation_time: int = 0):

        self.code = code
        self.pos = pos
        self.parent = parent
        self.item_name = item_name
        self.texture = pg.transform.scale(items[self.item_name].texture, ITEM_SIZE.as_tuple())
        self.screen_pos = Vector(0, 0)
        self.__texture_offset = Vector(ITEM_SIZE.x / 2, ITEM_SIZE.y)
        self.rect = self.texture.get_rect()
        self.do_draw = ()
        self.tobeddeleted = False
        self.animation_offset = Vector(0, 0)
        self.velocity = velocity
        self.animation_time = animation_time
        self.done = False
        self.anpos = Vector(0, 0)

    def draw(self):

        if all(self.do_draw):

            screen.blit(self.texture, self.screen_pos.as_tuple())

    def update(self):

        if not self.done: self.anpos += self.velocity
        if not self.done: self.velocity.y += 0.5
        self.animation_time -= 1
        if self.animation_time <= 0 and not self.done:
            self.done = True
            self.pos += self.anpos

        self.screen_pos = self.pos + self.parent.offset - self.__texture_offset - (self.animation_offset if self.done else Vector(0, 0)) + (self.anpos if not self.done else Vector(0, 0))
        self.do_draw = (
            self.screen_pos.x < RESOLUTION.x,
            self.screen_pos.x - ITEM_SIZE.x > -ITEM_SIZE.x * 2,
            self.screen_pos.y < RESOLUTION.y,
            self.screen_pos.y - ITEM_SIZE.y > -ITEM_SIZE.y * 2,
        )
        if all(self.do_draw):
            self.animation_offset.y = sin(self.parent.animation_counter / 10) * percent(TILE_SIZE.x, 10)
            self.rect.x = self.screen_pos.x
            self.rect.y = self.screen_pos.y

            if self.rect.colliderect(self.parent.player.rect) and not self.parent.player.dying:
                if self.parent.inventory.can_fit(self.item_name, 1):
                    self.parent.inventory.append(self.item_name)
                    self.tobeddeleted = True

    def dumb(self) -> dict:

        return {
            "class": 0,
            "pos": self.pos.as_tuple(),
            "item_name": self.item_name,
            "velocity": self.velocity.as_tuple(),
            "time": self.animation_time,
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.item_name = data["item_name"]
        self.velocity = from_iterable(data["velocity"])
        self.animation_time = data["time"]
        self.texture = pg.transform.scale(items[self.item_name].texture, ITEM_SIZE.as_tuple())
