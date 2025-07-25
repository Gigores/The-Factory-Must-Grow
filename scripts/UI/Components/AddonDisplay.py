from scripts.UI.Components.BaseUIComponents import Text
from scripts.constants import *


ICON_SIZE = Vector(100, 100)
ELEMENT_SPACING = 10


class AddonDisplay:

    def __init__(self, pos, addon: dict, rect_width):

        self.pos = pos
        self.description_text = addon["description"]
        self.icon = pg.transform.scale(addon["icon"], ICON_SIZE.as_tuple())
        self.name = Text(Vector(1, 1), addon["name"], max_size=Vector(rect_width - ELEMENT_SPACING * 3 - ICON_SIZE.x, ICON_SIZE.y - ELEMENT_SPACING * 2))
        self.description = Text(Vector(1, 1), self.description_text, font=SMALL_FONT, max_size=Vector(rect_width - ELEMENT_SPACING * 3 - ICON_SIZE.x, ICON_SIZE.y - ELEMENT_SPACING * 2 - FONT.get_height()))
        self.offset = (0, 0)
        self.rect_width = rect_width

    def update(self, offset=(0, 0), get_mouse_position=get_mouse_pos):

        self.offset = offset

    def events(self, events):

        pass

    def draw(self, dest=screen):

        dest.blit(self.icon, (self.pos[0] + ELEMENT_SPACING, self.pos[1] + self.offset[1] + ELEMENT_SPACING))
        self.name.draw(dest, Vector(self.pos[0] + ELEMENT_SPACING * 2 + ICON_SIZE.x, self.pos[1] + self.offset[1] + ELEMENT_SPACING * 2))
        self.description.draw(dest, Vector(self.pos[0] + ELEMENT_SPACING * 2 + ICON_SIZE.x, self.pos[1] + self.offset[1] + ELEMENT_SPACING * 3 + FONT.get_height()))
        pg.draw.rect(dest, "#333333", (self.pos[0] + ELEMENT_SPACING, self.pos[1] + ELEMENT_SPACING * 2 + ICON_SIZE.y - 2 + self.offset[1], self.rect_width - ELEMENT_SPACING * 2, 2))
