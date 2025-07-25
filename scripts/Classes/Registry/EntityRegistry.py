from scripts.constants import *


class EntityRegistry(type):

    def __new__(cls, name, bases, namespace):

        new_class = super().__new__(cls, name, bases, namespace)
        if name != "Building" and not (name in ENTITIES):
            ENTITIES.append(new_class)
        return new_class
