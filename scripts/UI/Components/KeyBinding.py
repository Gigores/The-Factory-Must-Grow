import pygame as pg
from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import TextButton
from scripts.UI.Components.DarkThemeComponents import Button
from scripts.UI.Components.BaseUIComponents import CLICK_SOUND

key_abbreviations = {
    'left shift': 'LShift',
    'right shift': 'RShift',
    'left ctrl': 'LCtrl',
    'right ctrl': 'RCtrl',
    'left alt': 'LAlt',
    'right alt': 'RAlt',
    'space': 'Spc',
    'escape': 'Esc',
    'return': 'Enter',
    'backspace': 'Bckspc',
    'tab': 'Tab',
    'caps lock': 'CapsLk',
    'left': 'Left',
    'right': 'Right',
    'up': 'Up',
    'down': 'Down',
    None: "NotBound"
}


def get_short_key_name(key):
    key_name = pg.key.name(key)
    return key_abbreviations.get(key_name, key_name)


class KeyBinding:

    def __init__(self, text: str, key: int, width: int, y_pos: int):

        self.text = text
        self.key = key
        self.y_pos = y_pos
        self.width = width

        self.listening = False
        self.font = FONT
        self.button = None
        self.button2 = None
        self.text_surf = self.font.render(self.text, True, "#ffffff")
        self.update_key(key)
        self.offset = (0, 0)

    def get_key(self) -> int:

        return self.key

    def update_key(self, key):

        self.key = key
        if self.key: key_name = get_short_key_name(self.key).capitalize()
        else: key_name = key_abbreviations[None]
        button_width = self.font.render(f" asdas ", True, "#ffffff").get_width()
        self.button = TextButton(Vector(self.width - button_width - 20, self.y_pos), button_width,
                                 key_name, fixed_text_pos=True, font=self.font,
                                 text_pos="center", text_color=("#AA4444" if self.key else "#333333"))
        self.button2 = Button(pg.Surface((1, 1)), pg.Surface((1, 1)), "",
                             (button_width, self.font.get_height()),
                             (self.width - button_width - 20, self.y_pos), invert_rect=True)

    def update(self, offset=(0, 0), get_mouse_position=get_mouse_pos):

        self.offset = offset
        self.button.update(offset=offset, get_mouse_position=get_mouse_position)
        self.button2.update(offset=offset, get_mouse_position=get_mouse_position)

        if self.button.just_pressed:
            self.listening = not self.listening
            self.button.selected = self.listening
            CLICK_SOUND.stop()
            CLICK_SOUND.play()

        if self.button2.just_pressed:
            self.listening = False
            self.button.selected = self.listening

    def events(self, events):

        if self.listening:

            for event in events:

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE: self.update_key(None)
                    else: self.update_key(event.key)
                    self.listening = False
                    self.button.selected = self.listening
                    CLICK_SOUND.stop()
                    CLICK_SOUND.play()

    def draw(self, dest=screen):

        self.button.draw(dest=dest)
        dest.blit(self.text_surf, (0, self.y_pos + self.offset[1]))
