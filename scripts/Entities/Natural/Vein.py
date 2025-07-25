from scripts.constants import *
from PgHelp import *
from random import randint, choice
import os
from scripts.Entities.Particle import Particle
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.Managers.GameAssets import *


folder = "assets/entities/veins"
#TEXTURES = {file.split('.')[0]: load_texture(os.path.join(folder, file), VEIN_SIZE) for file in os.listdir(folder)}
SOUND1 = pg.mixer.Sound("sound/pickaxe_1.mp3")
SOUND1.set_volume(0.5)
SOUND2 = pg.mixer.Sound("sound/ore_done.mp3")
SOUND2.set_volume(0.5)
#PARTICLES = {
#    "stone": load_texture("assets/particles/deposits.png", PARTICLE_SIZE),
#    "coal": load_texture("assets/particles/coal.png", PARTICLE_SIZE),
#    "copper": load_texture("assets/particles/copper.png", PARTICLE_SIZE),
#    "iron": load_texture("assets/particles/iron.png", PARTICLE_SIZE),
#    "zinc": load_texture("assets/particles/zinc.png", PARTICLE_SIZE),
#    "gold": load_texture("assets/particles/deposits.png", PARTICLE_SIZE),
#}


class Vein(metaclass=EntityRegistry):

    def __init__(self, code: any, pos: Vector, parent, ore_type: str = "stone"):

        self.code = code
        self.parent = parent
        self.pos = pos
        self.tobeddeleted = False
        self.texture = ORE_TEXTURES.get(ore_type, pg.transform.scale(TEXTUTURE_NULL, VEIN_SIZE.as_tuple()))["vein"]
        self.do_draw = ()
        self.__texture_offset = Vector(-(VEIN_SIZE.x / 2), -(VEIN_SIZE.y / 8 * 7))
        self.ore_type = ore_type
        self.hp = ORE_TYPE_TO_HP[self.ore_type]
        self.total_hp = items[ORE_TYPE_TO_ITEM[self.ore_type]].stack_size * 2
        self.animation = False
        self.animation_counter = 0
        self.screen_pos = Vector(0, 0)
        self.rect = pg.Rect((0, 0, VEIN_SIZE.x, VEIN_SIZE.y))
        self.touching = False
        self.just_pressed = False
        self.hitbox = pg.Rect(0, 0, self.texture.get_width() * 0.8, self.texture.get_height() * 0.4)

    def update(self):

        self.screen_pos = self.pos + self.parent.offset + (
            pg.math.Vector2(0, 0) if not self.animation else pg.math.Vector2(randint(-2, 2), randint(-2, 2)))
        self.do_draw = (
            self.screen_pos.x + self.__texture_offset.x < RESOLUTION.x,
            self.screen_pos.x - self.__texture_offset.x > -DEPOSIT_SIZE.x,
            self.screen_pos.y + self.__texture_offset.y < RESOLUTION.y,
            self.screen_pos.y - self.__texture_offset.y > -DEPOSIT_SIZE.y,
        )
        if any(self.do_draw):
            player_item = items.setdefault(self.parent.inventory.n[self.parent.player.inventory_cursor], None)
            self.rect.x = self.screen_pos.x + self.__texture_offset.x
            self.rect.y = self.screen_pos.y + self.__texture_offset.y
            self.hitbox.x = self.screen_pos.x + self.__texture_offset.x + self.texture.get_width() * 0.1
            self.hitbox.y = self.screen_pos.y + self.__texture_offset.y + self.texture.get_height() * 0.6
            try:
                item_type = player_item.type_
            except AttributeError:
                item_type = "null"
            self.touching = self.rect.collidepoint(
                get_mouse_pos()) and player_item and item_type == "pickaxe" and self.parent.active_ui_id is None
        else:
            player_item = 0
            self.touching = False

        if self.touching and pg.mouse.get_pressed()[0] and not self.just_pressed:

            if player_item.dont_need_clicking:

                if self.parent.animation_counter % 15 == 0:
                    SOUND1.stop()
                    SOUND1.play()

                self.hp -= player_item.damage
                self.animation = True
                for i in range(1):
                    particle_pos = from_iterable(get_mouse_pos()) - self.parent.offset
                    particle_velocity = Vector(randint(-5, 5), randint(-7, -3))
                    particle_texture = PARTICLE_TEXTURES.get(self.ore_type, PARTICLE_TEXTURES["stone"])
                    lifetime = randint(30, 40)
                    obj = Particle(self.parent.generate_id(), particle_pos, self.parent, particle_velocity, lifetime, particle_texture)
                    self.parent.particles.append(obj)
                if self.hp <= 0:
                    self.total_hp -= 1
                    item = ORE_TYPE_TO_ITEM[self.ore_type]
                    xvel = choice((TILE_SIZE.x / 16, -(TILE_SIZE.x / 16))) + randint(round(-(TILE_SIZE.x / 32)),
                                                                                     int(TILE_SIZE.x / 32))
                    self.parent.drop_items(self.pos, item, 1, Vector(xvel, - TILE_SIZE.y / 8), randint(25, 35))
                    SOUND2.play()
                    self.hp = ORE_TYPE_TO_HP[self.ore_type]
                    if self.total_hp <= 0:
                        self.tobeddeleted = True
                    return

            else:

                if not self.just_pressed:

                    self.just_pressed = True
                    self.hp -= player_item.damage
                    self.animation = True
                    SOUND1.stop()
                    SOUND1.play()
                    for i in range(10):
                        particle_pos = from_iterable(get_mouse_pos()) - self.parent.offset
                        particle_velocity = Vector(randint(-5, 5), randint(-7, -3))
                        particle_texture = PARTICLE_TEXTURES.get(self.ore_type, PARTICLE_TEXTURES["stone"])
                        lifetime = randint(30, 40)
                        obj = Particle(self.parent.generate_id(), particle_pos, self.parent, particle_velocity,
                                       lifetime, particle_texture)
                        self.parent.particles.append(obj)
                    if self.hp <= 0:
                        self.total_hp -= 1
                        item = ORE_TYPE_TO_ITEM[self.ore_type]
                        xvel = choice((TILE_SIZE.x / 16, -(TILE_SIZE.x / 16))) + randint(round(-(TILE_SIZE.x / 32)),
                                                                                         int(TILE_SIZE.x / 32))
                        self.parent.drop_items(self.pos, item, 1, Vector(xvel, - TILE_SIZE.y / 8), randint(25, 35))
                        self.hp = ORE_TYPE_TO_HP[self.ore_type]
                        SOUND2.play()
                        if self.total_hp <= 0:
                            self.tobeddeleted = True
                        return

        if self.just_pressed and not pg.mouse.get_pressed()[0]:
            self.just_pressed = False

        if self.animation:
            self.animation_counter += 1

        if self.animation_counter >= 10:
            self.animation_counter = 0
            self.animation = False

    def draw(self):

        if all(self.do_draw):
            self.parent.screen.blit(self.texture, (self.screen_pos + self.__texture_offset).as_tuple())
            #pg.draw.circle(screen, "#ff0000", (self.pos + self.__texture_offset).as_tuple(), 10)

            if self.touching:
                draw_brackets(self.parent.screen, self.rect)

            if self.parent.show_secret_data:
                pg.draw.circle(screen, "#ff00ff", (self.pos+self.parent.offset).as_tuple(), 5)
                pg.draw.rect(screen, "#ff0000", self.hitbox, 3)

    def dumb(self):

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "type": self.ore_type,
            "hp": self.total_hp
        }

    def load(self, data: dict):

        self.pos = Vector(data["pos"][0], data["pos"][1])
        self.ore_type = data["type"]
        self.total_hp = data["hp"]
        self.texture = ORE_TEXTURES.get(self.ore_type, pg.transform.scale(TEXTUTURE_NULL, VEIN_SIZE.as_tuple()))["vein"]
