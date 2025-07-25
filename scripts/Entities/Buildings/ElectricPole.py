from scripts.constants import *
from PgHelp import *
from scripts.Entities.ABC.ElectricNode import ElectricNode
from scripts.Managers.IngameManagers.Inventory import Slot
from scripts.Classes.Registry.EntityRegistry import EntityRegistry


TEXTURE_SIZE = TILE_SIZE * Vector(2, 4)
TEXTURE_OFFSET = TEXTURE_SIZE * Vector(-0.5, -1)
CONNECTION_OFFSET = TEXTURE_OFFSET * Vector(1, 0.39)
TEXTURE = load_texture("assets/entities/electric_pole.png", TEXTURE_SIZE)
HITBOX_SIZE = TEXTURE_SIZE * Vector(0.5, 0.2)
HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.25, 0.8)
COLLIDER_HITBOX_SIZE = TEXTURE_SIZE * Vector(0.5, 0.2)
COLLIDER_HITBOX_OFFSET = TEXTURE_SIZE * Vector(0.25, 0.8)

SOUND = pg.mixer.Sound("sound/axe.mp3")
SOUND.set_volume(0.5)


class ElectricPole(ElectricNode, metaclass=EntityRegistry):

    def __init__(self, code, pos, parent):

        super().__init__(code, pos, parent, TEXTURE, 50, TEXTURE_OFFSET,
                         "electric_pole", "axe", hitbox_size=HITBOX_SIZE,
                         hitbox_offset=HITBOX_OFFSET, use_hibox=False, wire_connection_offset=CONNECTION_OFFSET,
                         collider_hitbox_size=COLLIDER_HITBOX_SIZE, collider_hitbox_offset=COLLIDER_HITBOX_OFFSET,
                         max_connections=6, ui_id="ElectricalNetwork", requires_network_info=True, punch_sound=SOUND)
