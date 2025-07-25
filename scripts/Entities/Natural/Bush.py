from random import randint
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Managers.GameAssets import *


SIZE = TILE_SIZE * Vector(1, 1)
TEXTURE = load_texture("assets/entities/bush_empty.png", SIZE)
TEXTURE2 = load_texture("assets/entities/bush_berries.png", SIZE)


class Bush(metaclass=EntityRegistry):

    def __init__(self, code: any, pos: Vector, parent):

        self.code = code
        self.parent = parent
        self.pos = pos
        self.tobeddeleted = False
        self.__texture_offset = Vector(TEXTURE.get_width() / 2, TEXTURE.get_height() * 0.7)

        self.texture = TEXTURE
        self.texture2 = TEXTURE2
        self.screen_pos = Vector(0, 0)
        self.animation = False
        self.animation_counter = 0
        self.touching = False
        self.do_draw = ()
        self.rect = self.texture.get_rect()
        self.just_pressed = False
        self.hp = 50
        self.have_berries = bool(randint(0, 1)) if self.parent.settings_manager.settings["survival_mode"] else False

    def update(self):

        self.screen_pos = self.pos + self.parent.offset - self.__texture_offset + (
            Vector(0, 0) if not self.animation else Vector(randint(-3, 3), randint(-3, 3)))
        self.do_draw = (
            self.screen_pos.x < RESOLUTION.x,
            self.screen_pos.x - TREE_SIZE.x > -TREE_SIZE.x * 2,
            self.screen_pos.y < RESOLUTION.y,
            self.screen_pos.y - TREE_SIZE.y > -TREE_SIZE.y * 2,
        )
        player_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)
        if any(self.do_draw):
            self.rect.x = self.screen_pos.x
            self.rect.y = self.screen_pos.y
            try:
                self.touching = self.rect.collidepoint(
                    get_mouse_pos()) and ((player_item and player_item.type_ == "axe" and self.parent.active_ui_id is None) or self.have_berries)
            except:
                self.touching = False
        else:
            self.touching = False

        if self.touching and pg.mouse.get_pressed()[0] and (not self.just_pressed) and player_item and player_item.type_ == "axe":

            if player_item.dont_need_clicking:

                self.hp -= player_item.damage
                self.animation = True
                if self.hp <= 0:
                    self.parent.drop_items(self.pos, "log", 1)
                    self.parent.drop_items(self.pos, "berries", 3 if self.have_berries else 0)
                    self.parent.drop_items(self.pos, "stick", randint(3, 4))
                    self.tobeddeleted = True

            else:

                if not self.just_pressed:

                    self.just_pressed = True
                    self.hp -= player_item.damage
                    self.animation = True
                    if self.hp <= 0:
                        self.parent.drop_items(self.pos, "log", 1)
                        self.parent.drop_items(self.pos, "berries", 3 if self.have_berries else 0)
                        self.parent.drop_items(self.pos, "stick", randint(3, 4))
                        self.tobeddeleted = True

        if self.touching and pg.mouse.get_pressed()[2] and self.have_berries:
            self.have_berries = False
            self.parent.drop_items(self.pos, "berries", 3)

        if self.just_pressed and not pg.mouse.get_pressed()[0]:
            self.just_pressed = False

        if self.animation:
            self.animation_counter += 1

        if self.animation_counter >= 10:
            self.animation_counter = 0
            self.animation = False

    def draw(self):

        if all(self.do_draw):

            screen.blit(self.texture2 if self.have_berries else self.texture, self.screen_pos.as_tuple())

            if self.touching:

                draw_brackets(self.parent.screen, self.rect)

                #pg.draw.circle(screen, "#ff00ff", (self.pos+self.parent.offset).as_tuple(), 5)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "hp": self.hp
        }

    def load(self, data: dict):

        self.pos = Vector(data["pos"][0], data["pos"][1])
        self.hp = data["hp"]
