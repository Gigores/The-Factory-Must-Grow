from scripts.Classes.Registry.SubmenuRegistry import SubmenuRegistry
from scripts.UI.MainMenuScreen.Submenu import Submenu
import pygame as pg
from scripts.constants import *
import scripts.Managers.GameAssets as ast
from scripts.UI.Components.DarkThemeComponents import TextButton, CLICK_SOUND, Scrollable, SaveButton, ENTER_SOUND
from scripts.UI.Components.AddonDisplay import AddonDisplay, ICON_SIZE, ELEMENT_SPACING
import webbrowser


class Addons(Submenu, metaclass=SubmenuRegistry):

    def __init__(self, parent, rect_width):

        super().__init__(parent, "addons")
        self.rect_width = rect_width

        self.scroll1 = Scrollable(Vector(0, HUGE_FONT.get_height() * 2), Vector(rect_width, HUGE_FONT.get_height() * 5.5))
        self.return_btn = TextButton(Vector(0, RESOLUTION.y - HUGE_FONT.get_height() * 2), rect_width, "Back")
        self.download_btn = TextButton(Vector(0, self.scroll1.pos.y + self.scroll1.size.y), rect_width, "Download", fixed_text_pos=True)

        for i, (addon, info) in enumerate(ast.addons.items()):

            self.scroll1.append_element(addon, AddonDisplay((0, i * (ICON_SIZE.y + ELEMENT_SPACING * 2)), info, rect_width))

    def events(self, events: list):

        self.scroll1.events(events)

    def update(self):

        self.return_btn.update()
        self.download_btn.update()
        self.scroll1.update()

        if self.return_btn.just_pressed:
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.set_submenu("hub")

        if self.download_btn.just_pressed:
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            webbrowser.open("https://discord.gg/DWwFhsEmWH")

    def draw(self):

        screen.blit(HUGE_FONT.render("Addons", True, "#ffffff"), (0, 60))

        self.return_btn.draw()
        self.download_btn.draw()
        self.scroll1.draw()
