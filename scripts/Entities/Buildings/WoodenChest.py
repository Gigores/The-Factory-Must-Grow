from scripts.constants import *
from PgHelp import *
from scripts.Managers.IngameManagers.Inventory import Inventory
from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


TEXTURE_SIZE = TILE_SIZE
TEXTURE_OFFSET = Vector(-(TEXTURE_SIZE.x / 2), -(TEXTURE_SIZE.y / 4 * 3))
TEXTURE = load_texture("assets/entities/wooden_chest.png", TEXTURE_SIZE)
SOUND = pg.mixer.Sound("sound/axe.mp3")
SOUND.set_volume(0.5)
HITBOX_SIZE = TEXTURE_SIZE * Vector(1, 0.6)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0, 0.4)


class WoodenChest(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 100, TEXTURE_OFFSET, "wooden_chest", "axe", 2, SOUND, ui_id="WoodenChestUI",
                         collider_hitbox_size=HITBOX_SIZE, collider_hitbox_offset=HITBOX_OFFSET)
        self.inventory = Inventory(self, 10)

    def drop_items(self):

        super().drop_items()
        for item, amount in zip(self.inventory.n, self.inventory.a):
            self.parent.drop_items(self.pos, item, amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "inventory": self.inventory.dumb()
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.inventory.load(data["inventory"])


# class WoodenChest:
#
#     def __init__(self, code: any, pos: Vector, parent):
#
#         self.code = code
#         self.pos = pos
#         self.parent = parent
#
#         self.screen_pos = Vector(0, 0)
#         self.rect = pg.Rect((0, 0, TEXTURE_SIZE.x, TEXTURE_SIZE.y))
#
#         self.hp = 100
#         self.animation_counter = 0
#
#         self.animation = False
#         self.touching = False
#         self.do_draw = False
#         self.tobeddeleted = False
#         self.just_pressed = False
#
#         self.inventory = Inventory(self, 10)
#
#     def draw(self):
#
#         if self.do_draw:
#             self.parent.screen.blit(TEXTURE, self.screen_pos.as_tuple())
#             if self.touching: draw_brackets(self.parent.screen, self.rect)
#
#             # pg.draw.circle(screen, "#ff00ff", (self.pos+self.parent.offset).as_tuple(), 5)
#
#     def update(self):
#
#         self.screen_pos = self.pos + self.parent.offset - TEXTURE_OFFSET + \
#                           (Vector(0, 0) if not self.animation else Vector(randint(-3, 3), randint(-3, 3)))
#         self.do_draw = (
#             self.screen_pos.x < RESOLUTION.x,
#             self.screen_pos.x > -TEXTURE_SIZE.x,
#             self.screen_pos.y < RESOLUTION.y,
#             self.screen_pos.y > -TEXTURE_SIZE.y,
#         )
#         if any(self.do_draw):
#
#             self.rect.x = self.screen_pos.x
#             self.rect.y = self.screen_pos.y
#
#             self.touching = self.rect.collidepoint(get_mouse_pos()) and self.parent.active_ui_id is None
#
#             player_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)
#             try: type_match = player_item.type_ == "axe"
#             except: type_match = False
#
#             if self.touching and pg.mouse.get_pressed()[2] and not self.just_pressed:
#                 self.just_pressed = True
#                 self.parent.active_ui_id = 2
#                 self.parent.active_object_ui = self
#
#             if self.touching and pg.mouse.get_pressed()[0] and not self.just_pressed and player_item and type_match:
#                 self.just_pressed = True
#                 self.hp -= player_item.damage
#                 self.animation = True
#                 SOUND.stop()
#                 SOUND.play()
#                 if self.hp <= 0:
#                     self.parent.drop_items(self.pos, "wooden_chest", 1)
#                     for item, amount in zip(self.inventory.n, self.inventory.a):
#                         self.parent.drop_items(self.pos, item, amount)
#                     self.tobeddeleted = True
#                     return
#
#             if self.just_pressed and not (pg.mouse.get_pressed()[0] or pg.mouse.get_pressed()[2]):
#                 self.just_pressed = False
#
#             if self.animation:
#                 self.animation_counter += 1
#
#             if self.animation_counter >= 10:
#                 self.animation_counter = 0
#                 self.animation = False
#
#     def dumb(self) -> dict:
#
#         return {
#             "class": 2,
#             "pos": self.pos.as_tuple(),
#             "inventory": self.inventory.dumb()
#         }
#
#     def load(self, data: dict):
#
#         self.pos = from_iterable(data["pos"])
#         self.inventory.load(data["inventory"])
