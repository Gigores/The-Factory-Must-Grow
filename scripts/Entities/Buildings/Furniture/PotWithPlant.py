from scripts.constants import *
from scripts.Entities.ABC.Building import Building
from random import randint
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class PotWithPlant(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE * Vector(1.5, 1.5)
        textures = [
            load_texture("assets/entities/pot_with_plant_tree.png", texture_size),
            load_texture("assets/entities/pot_with_plant_empty.png", texture_size),
            load_texture("assets/entities/pot_with_plant_cactus.png", texture_size),
            load_texture("assets/entities/pot_with_plant_fungus.png", texture_size),
        ]
        sound = pg.mixer.Sound("sound/axe.mp3")
        sound.set_volume(0.5)
        texture_offset = texture_size * Vector(-0.5, -0.8)
        self.texture_id = randint(0, 3)
        hitbox_size = texture_size * Vector(0.6, 1)
        hitbox_offset = texture_size * Vector(0.15, 0)
        touch_hitbox_size = texture_size * Vector(0.3, 0.2)
        touch_hitbox_offset = texture_size * Vector(0.35, 0.8)
        super().__init__(code, pos, parent, textures, 10, texture_offset, "pot", "axe",
                         13, punch_sound=sound, hitbox_size=hitbox_size, hitbox_offset=hitbox_offset,
                         collider_hitbox_size=touch_hitbox_size, collider_hitbox_offset=touch_hitbox_offset)

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
