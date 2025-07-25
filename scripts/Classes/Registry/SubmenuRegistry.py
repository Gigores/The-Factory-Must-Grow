from scripts.constants import *


class SubmenuRegistry(type):

    def __new__(cls, name, bases, namespace):

        new_class = super().__new__(cls, name, bases, namespace)
        SUBMENUS.append(new_class)
        return new_class
