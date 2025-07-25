import pygame as pg
from scripts.UI.MainMenuScreen.Submenu import Submenu
from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import TextButton, CLICK_SOUND
from scripts.Classes.Registry.SubmenuRegistry import SubmenuRegistry


class Error(Submenu, metaclass=SubmenuRegistry):

    def __init__(self, parent, rect_width):

        super().__init__(parent, "error")

        self.exception: Exception = None
        self.quit_btn = TextButton(Vector(0, HUGE_FONT.get_height() * 10), rect_width, "ok", font=HUGEISH_FONT)

    def update(self):

        self.quit_btn.update()

        if self.quit_btn.just_pressed:
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.submenu_id = 0

    def draw(self):

        screen.blit(HUGEISH_FONT.render("unexpected ERROR", True, "#FF2222"), (10, 100))
        screen.blit(HUGEISH_FONT.render("occured!", True, "#FF2222"), (10, 150))
        # screen.blit(FONT.render(self.exception.__repr__(), True, "#FFFFFF"), (10, 300))
        # for i, arg in enumerate(self.exception.args) :
        #     screen.blit(FONT.render(str(arg), True, "#FFFFFF"), (10, 400 + i * FONT.get_height()))
        screen.blit(BIG_FONT.render("Please, send a post about", True, "#FFFFFF"), (10, 600))
        screen.blit(BIG_FONT.render("this error with log.log", True, "#FFFFFF"), (10, 650))
        screen.blit(BIG_FONT.render("file to #fmg-bug-report", True, "#FFFFFF"), (10, 700))
        screen.blit(BIG_FONT.render("in the discord server!", True, "#FFFFFF"), (10, 750))
        self.quit_btn.draw()
