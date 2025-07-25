from scripts.Entities.ABC.Building import Building
from scripts.Managers.GameAssets import *


class ElectricNode(Building):

    def __init__(self, code, pos: Vector, parent, texture, hp, texture_offset: Vector, item_name, instrument_type,
                 class_id=0, punch_sound=None, break_sound=None, ui_id=None, hitbox_size=None, hitbox_offset=None,
                 collider_hitbox_size=None, collider_hitbox_offset=None, texture_size=Vector(1, 1),
                 use_hibox: bool = True, max_connections: int = 2, wire_connection_offset: Vector = Vector(0, 0),
                 network_weight: int = 0, requires_network_info=False, connection_size=Vector(10, 3)):

        super().__init__(code, pos, parent, texture, hp, texture_offset,
                         item_name, instrument_type, class_id, punch_sound,
                         break_sound, ui_id, hitbox_size, hitbox_offset,
                         collider_hitbox_size, collider_hitbox_offset,
                         texture_size, use_hibox, forced_updating=True)

        self.max_connections = max_connections
        self.wire_connection_offset = wire_connection_offset
        self.network_weight = network_weight
        self.requires_network_info = requires_network_info
        self.connection_size = connection_size

        self.network_info = None

    def distribute(self, energy: int):

        pass

    def distribute_network_info(self, info: dict):

        self.network_info = info

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "code": self.code,
            "pos": self.pos.as_tuple()
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.code = data["code"]
