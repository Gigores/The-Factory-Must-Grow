from scripts.constants import *
from scripts.Entities.ABC.Building import Building
from random import randint
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class Bed(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(1, 1.5)
        textures = [
            load_texture("assets/entities/bed_red.png", texture_size),
            load_texture("assets/entities/bed_blue.png", texture_size),
            load_texture("assets/entities/bed_green.png", texture_size),
            load_texture("assets/entities/bed_yellow.png", texture_size),
        ]
        texture_offset = texture_size * Vector(-0.5, -0.5)

        sound = pg.mixer.Sound("sound/axe.mp3")
        sound.set_volume(0.5)
        touch_hitbox_size = texture_size * Vector(1, 0.8)
        touch_hitbox_offset = texture_size * Vector(0, 0.2)

        super().__init__(code, pos, parent, textures, 10, texture_offset, "bed",
                         "axe", 12, punch_sound=sound,
                         collider_hitbox_size=touch_hitbox_size, collider_hitbox_offset=touch_hitbox_offset)
        self.texture_id = randint(0, 3)

    def select_texture(self) -> pg.Surface:

        return self.texture[self.texture_id]

    def dumb(self) -> dict:
        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_list(),
            "texture": self.texture_id,
        }

    def load(self, data: dict):
        self.pos = from_iterable(data["pos"])
        self.texture_id = data["texture"]
