from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.constants import *
from PgHelp import *
from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry

TEXTURE_SIZE = Vector(TILE_SIZE.x * 1, TILE_SIZE.y * 1)
TEXTURE = load_texture("assets/entities/workbench.png", TEXTURE_SIZE)
TEXTURE_OFFSET = Vector(-(TEXTURE_SIZE.x / 2), -(TEXTURE_SIZE.y / 6 * 5))
SOUND = pg.mixer.Sound("sound/axe.mp3")
SOUND.set_volume(0.5)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.9, 0.5)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.05, 0.5)


class Workbench(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 200, TEXTURE_OFFSET, "workbench", "axe", 0, SOUND, ui_id="WorkbenchUI",
                         collider_hitbox_size=HITBOX_SIZE, collider_hitbox_offset=HITBOX_OFFSET)

        self.ing1_slot = Slot()
        self.ing2_slot = Slot()
        self.res_slot = Slot()

    def drop_items(self):

        super().drop_items()
        self.parent.drop_items(self.pos, self.ing1_slot.item_name, self.ing1_slot.item_amount)
        self.parent.drop_items(self.pos, self.ing2_slot.item_name, self.ing2_slot.item_amount)
        self.parent.drop_items(self.pos, self.res_slot.item_name, self.res_slot.item_amount)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "ing1_slot": self.ing1_slot.dumb(),
            "ing2_slot": self.ing2_slot.dumb(),
            "res_slot": self.res_slot.dumb(),
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.ing1_slot.load(data["ing1_slot"])
        self.ing2_slot.load(data["ing2_slot"])
        self.res_slot.load(data["res_slot"])

#
# class Workbench:
#
#     def __init__(self, code: any, pos: Vector, parent):
#
#         self.code = code
#         self.tobeddeleted = False
#         self.pos = pos
#         self.parent = parent
#         self.screen_pos = Vector(0, 0)
#         self.do_draw = False
#         self.rect = pg.Rect((0, 0, TEXTURE_SIZE.x, TEXTURE_SIZE.y))
#         self.touching = False
#         self.just_pressed = False
#         self.hp = 200
#         self.animation = False
#         self.animation_counter = 0
#
#     def draw(self):
#
#         if self.do_draw:
#             self.parent.screen.blit(TEXTURE, self.screen_pos.as_tuple())
#             if self.touching: draw_brackets(self.parent.screen, self.rect)
#             # pg.draw.circle(screen, "#ff00ff", (self.pos+self.parent.offset).as_tuple(), 5)
#
#     def update(self):
#
#         self.screen_pos = self.pos + self.parent.offset + TEXTURE_OFFSET + (pg.Vector2(0, 0) if not self.animation else pg.Vector2(randint(-2, 2), randint(-2, 2)))
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
#             if self.touching and pg.mouse.get_pressed()[2] and not self.just_pressed:
#                 self.just_pressed = True
#                 self.parent.active_ui_id = 0
#                 self.parent.active_object_ui = self
#
#             player_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)
#             try: type_match = player_item.type_ == "axe"
#             except: type_match = False
#             if self.touching and pg.mouse.get_pressed()[0] and not self.just_pressed and player_item and type_match:
#                 self.just_pressed = True
#                 self.hp -= player_item.damage
#                 self.animation = True
#                 SOUND.stop()
#                 SOUND.play()
#                 if self.hp <= 0:
#                     self.parent.drop_items(self.pos, "workbench", 1)
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
#             "class": 0,
#             "pos": self.pos.as_tuple()
#         }
#
#     def load(self, data: dict):
#
#         self.pos = from_iterable(data["pos"])
#
#     def __repr__(self):
#
#         return f"Workbench at {self.pos}"
