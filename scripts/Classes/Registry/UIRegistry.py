from scripts.constants import *


class UIRegistry(type):

    def __new__(cls, name, bases, namespace):

        new_class = super().__new__(cls, name, bases, namespace)
        ENTITY_UI.append(new_class)
        return new_class
