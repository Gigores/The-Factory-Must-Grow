import pygame as pg
from scripts.Classes.Registry.EntityRegistry import EntityRegistry
from scripts.constants import *


class Wire(metaclass=EntityRegistry):

    def __init__(self, code, pos, parent, a: int = None, b: int = None):

        self.code = code
        self.parent = parent

        self.a = a
        self.b = b

        if not (a is None) and not (b is None):

            self.entity_a = self.parent.entity_manager.get_building_by_code(self.a)
            self.entity_b = self.parent.entity_manager.get_building_by_code(self.b)

            self.pos_a = self.entity_a.pos + self.entity_a.texture_offset - self.entity_a.wire_connection_offset
            self.pos_b = self.entity_b.pos + self.entity_b.texture_offset - self.entity_b.wire_connection_offset

        self.do_draw = False
        self.tobedeleted = False

    def update(self, preview_mode: bool = False):

        if not (self.entity_a is None) and not (self.entity_a is None):
            self.do_draw = self.entity_a.do_draw or self.entity_b.do_draw
            if self.parent.animation_counter % 3 == 0:
                self.entity_a = self.parent.entity_manager.get_building_by_code(self.a)
                self.entity_b = self.parent.entity_manager.get_building_by_code(self.b)
                if self.entity_a is None or self.entity_b is None:
                    self.tobedeleted = True
        else:
            self.do_draw = False

    def draw(self):
        if self.do_draw:
            screen_pos_a = self.parent.offset + self.pos_a
            screen_pos_b = self.parent.offset + self.pos_b

            draw_wire(screen_pos_a, screen_pos_b)

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "a": self.a,
            "b": self.b
        }

    def load(self, data):

        self.a = data["a"]
        self.b = data["b"]

    def post_init(self):

        self.entity_a = self.parent.entity_manager.get_building_by_code(self.a)
        self.entity_b = self.parent.entity_manager.get_building_by_code(self.b)

        if self.entity_a is None or self.entity_b is None:
            self.tobedeleted = True

        self.pos_a = self.entity_a.pos + self.entity_a.texture_offset - self.entity_a.wire_connection_offset
        self.pos_b = self.entity_b.pos + self.entity_b.texture_offset - self.entity_b.wire_connection_offset

