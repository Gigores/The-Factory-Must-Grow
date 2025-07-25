from scripts.constants import *
from PgHelp import *
from math import sin, pi
from random import randint
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Managers.GameAssets import items
import time
from scripts.Entities.ABC.Building import Building


def shear_surface_up(surface, shear_pixels):
    width, height = surface.get_size()

    new_surface = pg.Surface((width + abs(shear_pixels), height), pg.SRCALPHA)
    new_surface.fill((0, 0, 0, 0))

    for y in range(height):
        shear_x = int(shear_pixels * (y / height))
        for x in range(width):
            new_x = x - shear_x + abs(shear_pixels)
            if 0 <= new_x < new_surface.get_width():
                new_surface.set_at((int(new_x), y), surface.get_at((x, y)))

    return new_surface


cashed_sin = [sin(i/10)*2 for i in range(0, int(pi*20))]
TREE_TEXTURES = [
    load_texture("assets/entities/tree.png", TREE_SIZE),
    load_texture("assets/entities/tree_2.png", TREE_SIZE),
    load_texture("assets/entities/tree_3.png", TREE_SIZE),
]
SOUND = pg.mixer.Sound("sound/axe.mp3")
SOUND.set_volume(0.5)
min_s = min(cashed_sin)
correction = abs(min_s * 2)
cashed_textures = [
    [shear_surface_up(TREE_TEXTURES[0], s * 2 + correction * 1.5) for s in cashed_sin],
    [shear_surface_up(TREE_TEXTURES[1], s * 2 + correction * 1.5) for s in cashed_sin],
    [shear_surface_up(TREE_TEXTURES[2], s * 2 + correction * 1.5) for s in cashed_sin],
]
TEXTURE_OFFSET = TREE_SIZE * Vector(-0.5, -0.95)

"""
class Tree(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TREE_TEXTURES[0], 100, TEXTURE_OFFSET, "tree_sapling", "axe", punch_sound=SOUND, use_hibox=False)

        self.texture_id = randint(0, 2)
        self.do_dead_animation = False
        self.angle = 0

    def aftergen(self):

        if self.parent.world.data[self.pos.x // TILE_SIZE.x][self.pos.y // TILE_SIZE.y] in [3, 4, 5, 6]:
            self.tobeddeleted = True

    def draw(self) :

        # print(self.pos)
        if all(self.do_draw) :
            if self.do_dead_animation :
                i = 0
            else :
                i = int(self.parent.animation_counter / 2 % int(pi * 20))
            # texture_height = TREE_SIZE.y + s
            # texture = pg.transform.scale(TREE_TEXTURE, (TREE_SIZE.x, texture_height))
            texture = pg.transform.rotate(cashed_textures[self.texture_id][int((i + (self.pos.x // TILE_SIZE.x) % len(
                cashed_textures[self.texture_id])) % len(cashed_textures[self.texture_id]))], self.angle)
            self.parent.screen.blit(texture, (self.screen_pos + Vector(0, TREE_TEXTURES[self.texture_id].get_height() -
                                                                       cashed_textures[self.texture_id][
                                                                           i].get_height() + (
                                                                           1 if i > 0 else 0))).as_tuple())

            if self.touching :
                draw_brackets(self.parent.screen, self.rect)

                if self.parent.show_secret_data :
                    pg.draw.circle(screen, "#ff00ff", (self.pos + self.parent.offset).as_tuple(), 5)
                # pg.draw.circle(screen, "#ff00ff", (self.pos + self.parent.offset + self.__texture_offset).as_tuple(), 5)

    def drop_items(self):

        self.parent.drop_items(self.pos, "log", 4)
        self.parent.drop_items(self.pos, "tree_sapling", randint(1, 2))
        self.parent.drop_items(self.pos, "actual_apple", randint(0, 1))
        self.parent.drop_items(self.pos, "stick", randint(1, 2))
"""


class Tree(metaclass=EntityRegistry):

    def __init__(self, code: any, pos: Vector, parent):

        self.code = code
        self.parent = parent
        self.pos = pos
        self.screen_pos = Vector(0, 0)
        self.__texture_offset = Vector(TREE_SIZE.x / 2, TREE_SIZE.y / 16 * 15)
        self.do_draw = ()
        self.rect = pg.Rect((0, 0, TREE_SIZE.x, TREE_SIZE.y))
        self.touching = False
        self.just_pressed = False
        self.hp = 100
        self.tobeddeleted = False
        self.animation = False
        self.animation_counter = 0
        self.texture_id = randint(0, 2)
        self.do_dead_animation = False
        self.angle = 0
        self.angle_v = 0
        self.rotation_offset = 0

    def aftergen(self):

        try:
            if self.parent.world.data[self.pos.x // TILE_SIZE.x][self.pos.y // TILE_SIZE.y] in [3, 4, 5, 6]:
                self.tobeddeleted = True
        except IndexError:
            self.tobeddeleted = True

    def update(self):

        self.screen_pos = self.pos + self.parent.offset - self.__texture_offset + (Vector(0, 0) if not self.animation else Vector(randint(-3, 3), randint(-3, 3)))
        self.do_draw = (
            self.screen_pos.x < RESOLUTION.x,
            self.screen_pos.x - TREE_SIZE.x > -TREE_SIZE.x * 2,
            self.screen_pos.y < RESOLUTION.y,
            self.screen_pos.y - TREE_SIZE.y > -TREE_SIZE.y * 2,
        )
        if any(self.do_draw):
            player_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)
            self.rect.x = self.screen_pos.x
            self.rect.y = self.screen_pos.y
            try:
                self.touching = self.rect.collidepoint(get_mouse_pos()) and player_item and player_item.type_ == "axe" and self.parent.active_ui_id is None
            except:
                self.touching = False
        else:
            self.touching = False

        if self.touching and pg.mouse.get_pressed()[0] and not self.do_dead_animation:

            if player_item.dont_need_clicking:

                if self.parent.animation_counter % 15 == 0:
                    SOUND.stop()
                    SOUND.play()

                self.hp -= player_item.damage
                self.animation = True
                if self.hp <= 0:
                    self.parent.drop_items(self.pos, "log", 4)
                    self.parent.drop_items(self.pos, "tree_sapling", randint(1, 2))
                    self.parent.drop_items(self.pos, "actual_apple", randint(0, 1))
                    self.parent.drop_items(self.pos, "stick", randint(1, 2))
                    self.tobeddeleted = True

            else:

                if not self.just_pressed:

                    self.just_pressed = True
                    self.hp -= player_item.damage
                    self.animation = True
                    SOUND.stop()
                    SOUND.play()
                    if self.hp <= 0:
                        self.parent.drop_items(self.pos, "log", 4)
                        self.parent.drop_items(self.pos, "tree_sapling", randint(1, 2))
                        self.parent.drop_items(self.pos, "actual_apple", randint(0, 1))
                        self.parent.drop_items(self.pos, "stick", randint(1, 2))
                        self.tobeddeleted = True

        if self.just_pressed and not pg.mouse.get_pressed()[0]:

            self.just_pressed = False

        if self.animation:
            self.animation_counter += 1

        if self.animation_counter >= 10:
            self.animation_counter = 0
            self.animation = False

        if self.do_dead_animation:
            self.angle += self.angle_v
            self.angle_v += 0.05

            if self.angle >= 90:
                self.angle = 90

        #self.rotation_offset = pg.Vector2(self.__texture_offset.x, 0) - pg.Vector2(self.__texture_offset.x, 0).rotate(-self.angle)
        #print(self.rotation_offset)

        # if self.touching:
        #     print(self.just_pressed)

    def draw(self):

        # print(self.pos)
        if all(self.do_draw):
            if self.do_dead_animation: i = 0
            else: i = int(self.parent.animation_counter / 2 % int(pi*20))
            #texture_height = TREE_SIZE.y + s
            #texture = pg.transform.scale(TREE_TEXTURE, (TREE_SIZE.x, texture_height))
            texture = pg.transform.rotate(cashed_textures[self.texture_id][int((i + (self.pos.x // TILE_SIZE.x) % len(cashed_textures[self.texture_id])) % len(cashed_textures[self.texture_id]))], self.angle)
            self.parent.screen.blit(texture, (self.screen_pos + Vector(0, TREE_TEXTURES[self.texture_id].get_height() - cashed_textures[self.texture_id][i].get_height() + (1 if i>0 else 0))).as_tuple())
            
            if self.touching:
                draw_brackets(self.parent.screen, self.rect)

                if self.parent.show_secret_data:
                    pg.draw.circle(screen, "#ff00ff", (self.pos+self.parent.offset).as_tuple(), 5)
                # pg.draw.circle(screen, "#ff00ff", (self.pos + self.parent.offset + self.__texture_offset).as_tuple(), 5)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "texture_id": self.texture_id,
            "hp": self.hp
        }

    def load(self, data: dict):

        self.pos = Vector(data["pos"][0], data["pos"][1])
        self.texture_id = data["texture_id"]
        self.hp = data["hp"]

    def __repr__(self):

        return f"tree at {self.pos.as_tuple()}"

