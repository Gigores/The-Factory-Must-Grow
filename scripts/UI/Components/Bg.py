from pygame import Surface
from scripts.constants import RESOLUTION, screen


class Bg(Surface):

    def __init__(self):

        super().__init__(RESOLUTION.as_tuple())
        self.set_colorkey("#000000")

    def draw(self):

        screen.blit(self, (0, 0))
