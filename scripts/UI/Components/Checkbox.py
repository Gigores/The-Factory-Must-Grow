from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import Button
from scripts.UI.Components.BaseUIComponents import CLICK_SOUND


class CheckBox:

    def __init__(self, text: str, width: int, y_pos: int, font: pg.font.Font = BIG_FONT):

        self.text = text
        self.width = width
        self.y_pos = y_pos
        self.font = font

        self.offset = None

        button_margin = font.get_height() * 0.3
        button_size = Vector(font.get_height() * 0.8, font.get_height() * 0.8)
        button_pos = Vector(width - button_size.x - button_margin, y_pos)
        textr = pg.Surface(button_size.as_tuple())
        textr.fill("#ff0000")
        self.value = False
        self.button = Button(textr, textr, "", button_size.as_tuple(), (button_pos - Vector(20, 0)).as_tuple())
        self.button_rect = pg.Rect(button_pos.as_tuple(), button_size.as_tuple())
        self.text_surf = self.font.render(self.text, True, "white")

    def update(self, offset=(0, 0), get_mouse_position=get_mouse_pos):

        self.offset = offset

        self.button.update(offset, get_mouse_position)

        if self.button.just_pressed:
            self.value = not self.value
            CLICK_SOUND.stop()
            CLICK_SOUND.play()

    def events(self, events):

        pass

    def draw(self, dest=screen):

        # self.button.draw(dest)

        if self.offset:
            rect = pg.Rect((self.button_rect.x, self.button_rect.y + self.offset[1]), self.button_rect.size)
            pg.draw.rect(dest, "white", rect, 0 if self.value else 2)
            dest.blit(self.text_surf, (0, self.y_pos + self.offset[1]))

    def set(self, value: bool):

        self.value = value

    def get(self):

        return self.value
