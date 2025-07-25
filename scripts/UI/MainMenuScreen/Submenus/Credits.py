import pygame as pg
from scripts.UI.Components.BaseUIComponents import Text
from scripts.UI.MainMenuScreen.Submenu import Submenu
from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import TextButton, CLICK_SOUND
from scripts.Classes.Registry.SubmenuRegistry import SubmenuRegistry


class Credits(Submenu, metaclass=SubmenuRegistry):

    def __init__(self, parent, rect_width):

        super().__init__(parent, "credits")

        self.return_btn = TextButton(Vector(0, RESOLUTION.y - HUGE_FONT.get_height() * 2), rect_width, "Back")
        with open("assets/Credits.txt", encoding="utf-8") as f :
            controls_text = f.read()
        self.credit_text = Text(Vector(0, 60 + SMALL_FONT.get_height() * 5), controls_text, font=SMALL_FONT)
        self.guys = pg.transform.scale_by(pg.image.load("assets/guys.png"), 2)
        self.guys_pos = (rect_width / 2 - self.guys.get_width() / 2, RESOLUTION.y - self.guys.get_height() - 240)

    def update(self):

        self.return_btn.update()

        if self.return_btn.just_pressed:
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.set_submenu("hub")

    def draw(self):

        screen.blit(HUGE_FONT.render("Credits", True, "#ffffff"), (0, 60))
        screen.blit(self.guys, self.guys_pos)

        self.credit_text.draw()
        self.return_btn.draw()
