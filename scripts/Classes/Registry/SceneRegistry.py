from scripts.constants import *


class SceneRegistry(type):

    def __new__(cls, name, bases, namespace):

        new_class = super().__new__(cls, name, bases, namespace)
        SCENES.append(new_class)
        return new_class
    