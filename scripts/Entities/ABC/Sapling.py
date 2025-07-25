from scripts.constants import *
from scripts.Entities.ABC.Building import Building


class Sapling(Building):

    def __init__(self, code, pos, parent, texture, entity_class, class_id, item_name):

        texture_offset = from_iterable(texture.get_size()) * Vector(-0.5, -0.9)

        super().__init__(code, pos, parent, texture, 1, texture_offset, item_name, "axe", class_id, use_hibox=False)

        self.counter = 0
        self.entity_class = entity_class

    def update(self, preview_mode: bool = False):

        super().update(preview_mode)

        self.counter += 1

        if self.counter >= 60 * 60:

            self.tobeddeleted = True
            self.parent.trees.append(self.entity_class(self.parent.generate_id(), self.pos, self.parent))
            self.parent.entity_manager.update_entities_by_chunks()

    def dumb(self) -> dict:

        return {
            "class": self.__class__.__name__,
            "pos": self.pos.as_tuple(),
            "counter": self.counter,
        }

    def load(self, data: dict):

        self.pos = from_iterable(data["pos"])
        self.counter = data["counter"]
