import pygame as pg
from scripts.UI.MainMenuScreen.Submenu import Submenu
from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import TextButton, CLICK_SOUND, Scrollable
from scripts.UI.Components.BaseUIComponents import Scrollbar
from scripts.UI.Components.KeyBinding import KeyBinding
from scripts.UI.Components.Checkbox import CheckBox
from scripts.Classes.Registry.SubmenuRegistry import SubmenuRegistry


class Settings(Submenu, metaclass=SubmenuRegistry):

    def __init__(self, parent, rect_width):

        super().__init__(parent, "settings")

        self.return_btn = TextButton(Vector(0, RESOLUTION.y - HUGE_FONT.get_height() * 2), rect_width, "Back")
        self.scrollbar = Scrollable(Vector(0, 180), Vector(rect_width, 600), constant_offset=Vector(20, 20))
        self.scrollbar.append_element("key_bind_0", KeyBinding("Go Up", pg.K_w, rect_width, FONT.get_height() * 0))
        self.scrollbar.append_element("key_bind_1", KeyBinding("Go Left", pg.K_a, rect_width, FONT.get_height() * 1))
        self.scrollbar.append_element("key_bind_2", KeyBinding("Go Down", pg.K_s, rect_width, FONT.get_height() * 2))
        self.scrollbar.append_element("key_bind_3", KeyBinding("Go Right", pg.K_d, rect_width, FONT.get_height() * 3))

        self.scrollbar.append_element("key_bind_4", KeyBinding("Open Backpack", pg.K_e, rect_width, FONT.get_height() * 4.5))
        self.scrollbar.append_element("key_bind_5", KeyBinding("Open Achievements", pg.K_l, rect_width, FONT.get_height() * 5.5))
        self.scrollbar.append_element("key_bind_11", KeyBinding("Open World Map", pg.K_l, rect_width, FONT.get_height() * 6.5))
        # self.scrollbar.append_element("key_bind_6", KeyBinding("Open ESC menu", pg.K_ESCAPE, rect_width, BIG_FONT.get_height() * 7.5))
        self.scrollbar.append_element("key_bind_7", KeyBinding("Drop Item", pg.K_z, rect_width, FONT.get_height() * 7.5))

        self.scrollbar.append_element("key_bind_8", KeyBinding("Hide UI", pg.K_F1, rect_width, FONT.get_height() * 9))
        self.scrollbar.append_element("key_bind_9", KeyBinding("Screenshot", pg.K_F2, rect_width, FONT.get_height() * 10))
        self.scrollbar.append_element("key_bind_10", KeyBinding("Open Terminal", pg.K_F12, rect_width, FONT.get_height() * 11))

        self.scrollbar.append_element("checkbox_1", CheckBox("Ingame Terminal", rect_width, FONT.get_height() * 13, font=FONT))
        self.scrollbar.append_element("checkbox_2", CheckBox("Survival Mode", rect_width, FONT.get_height() * 14, font=FONT))

        self.save_btn = TextButton(Vector(0, RESOLUTION.y - HUGE_FONT.get_height() * 3), rect_width, "Save")
        self.default_btn = TextButton(Vector(0, RESOLUTION.y - HUGE_FONT.get_height() * 4), rect_width, "Default")

    def save_settings(self):

        settings = {
            "go_up": self.scrollbar.get_element("key_bind_0").get_key(),
            "go_left": self.scrollbar.get_element("key_bind_1").get_key(),
            "go_down": self.scrollbar.get_element("key_bind_2").get_key(),
            "go_right": self.scrollbar.get_element("key_bind_3").get_key(),

            "backpack": self.scrollbar.get_element("key_bind_4").get_key(),
            "achievements": self.scrollbar.get_element("key_bind_5").get_key(),
            "map": self.scrollbar.get_element("key_bind_11").get_key(),
            #"esc_menu": self.scrollbar.get_element("key_bind_6").get_key(),
            "drop_item": self.scrollbar.get_element("key_bind_7").get_key(),

            "hide_ui": self.scrollbar.get_element("key_bind_8").get_key(),
            "screenshot": self.scrollbar.get_element("key_bind_9").get_key(),
            "terminal": self.scrollbar.get_element("key_bind_10").get_key(),

            "enable_terminal": self.scrollbar.get_element("checkbox_1").get(),
            "survival_mode": self.scrollbar.get_element("checkbox_2").get(),
        }
        self.parent.parent.settings_manager.save_settings(settings)

    def load_settings(self):

        settings = self.parent.parent.settings_manager.settings

        self.scrollbar.get_element("key_bind_0").update_key(settings["go_up"])
        self.scrollbar.get_element("key_bind_1").update_key(settings["go_left"])
        self.scrollbar.get_element("key_bind_2").update_key(settings["go_down"])
        self.scrollbar.get_element("key_bind_3").update_key(settings["go_right"])

        self.scrollbar.get_element("key_bind_4").update_key(settings["backpack"])
        self.scrollbar.get_element("key_bind_5").update_key(settings["achievements"])
        self.scrollbar.get_element("key_bind_11").update_key(settings["map"])
        #self.scrollbar.get_element("key_bind_6").update_key(settings["esc_menu"])
        self.scrollbar.get_element("key_bind_7").update_key(settings["drop_item"])

        self.scrollbar.get_element("key_bind_8").update_key(settings["hide_ui"])
        self.scrollbar.get_element("key_bind_9").update_key(settings["screenshot"])
        self.scrollbar.get_element("key_bind_10").update_key(settings["terminal"])

        self.scrollbar.get_element("checkbox_1").set(settings["enable_terminal"])
        self.scrollbar.get_element("checkbox_2").set(settings["survival_mode"])

    def events(self, events: list):
        self.scrollbar.events(events)

    def update(self):

        self.return_btn.update()
        if self.return_btn.just_pressed:
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.set_submenu("hub")

        self.save_btn.update()
        if self.save_btn.just_pressed:
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.save_settings()

        self.default_btn.update()
        if self.default_btn.just_pressed:
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.parent.settings_manager.set_default_settings()
            self.load_settings()

        self.scrollbar.update()

    def draw(self):

        screen.blit(HUGE_FONT.render("Settings", True, "#ffffff"), (0, 60))

        self.scrollbar.draw()

        self.return_btn.draw()
        self.save_btn.draw()
        self.default_btn.draw()
