from scripts.constants import *
from scripts.Entities.ABC.Building import Building
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


class Stool(Building, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        texture_size = TILE_SIZE
        texture = load_texture("assets/entities/stool.png", texture_size)
        texture_offset = texture_size * Vector(-0.5, -0.75)
        hitbox_size = texture_size * Vector(0.6, 0.6)
        hitbox_offset = texture_size * Vector(0.2, 0.4)
        touch_hitbox_size = texture_size * Vector(0.6, 0.4)
        touch_hitbox_offset = texture_size * Vector(0.2, 0.6)

        sound = pg.mixer.Sound("sound/axe.mp3")
        sound.set_volume(0.5)

        super().__init__(code, pos, parent, texture, 10, texture_offset, "stool", "axe", 11,
                         punch_sound=sound, collider_hitbox_size=touch_hitbox_size, collider_hitbox_offset=touch_hitbox_offset,
                         hitbox_size=hitbox_size, hitbox_offset=hitbox_offset)
