import pygame as pg
from scripts.UI.MainMenuScreen.Submenu import Submenu
from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import TextButton, CLICK_SOUND
from math import sin
from random import randint
from scripts.Classes.Registry.SubmenuRegistry import SubmenuRegistry
from scripts.Managers.GameAssets import addons


class HubMenu(Submenu, metaclass=SubmenuRegistry):

    def __init__(self, parent, rect_width):

        super().__init__(parent, "hub")

        self.new_game_btn = TextButton(Vector(0, HUGE_FONT.get_height() * 4), rect_width, "New Game", font=HUGEISH_FONT)
        self.load_game_btn = TextButton(Vector(0, HUGE_FONT.get_height() * 5), rect_width, "Load Game", font=HUGEISH_FONT)
        self.settings_btn = TextButton(Vector(0, HUGE_FONT.get_height() * 6), rect_width, "Settings", font=HUGEISH_FONT)
        self.credit_btn = TextButton(Vector(0, HUGE_FONT.get_height() * 7), rect_width, "Credits", font=HUGEISH_FONT)
        self.screenshots_btn = TextButton(Vector(0, HUGE_FONT.get_height() * 8), rect_width, "Screenshots", font=HUGEISH_FONT)
        self.addons_btn = TextButton(Vector(0, HUGE_FONT.get_height() * 9), rect_width, "Addons", font=HUGEISH_FONT)
        self.quit_btn = TextButton(Vector(0, HUGE_FONT.get_height() * 10), rect_width, "Quit", font=HUGEISH_FONT)
        self.splash_texture = pg.Surface((1, 1))

        with open("assets/splashes.txt", "r", encoding="utf-8") as f:
            fd = f.read()
        self.splashes = [str_ for str_ in fd.split("\n")]

        self.update_splash()

    def update_splash(self):

        self.splash_texture = pg.transform.rotate(FONT.render(self.splashes[randint(0, len(self.splashes)-1)], True, "#ffff00"), 25)

    def update(self):

        self.new_game_btn.update()
        self.load_game_btn.update()
        self.settings_btn.update()
        self.credit_btn.update()
        self.screenshots_btn.update()
        self.quit_btn.update()
        self.addons_btn.update()

        if self.new_game_btn.just_pressed:
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.get_submenu("new_world").name_input.reset()
            self.parent.get_submenu("new_world").seed_input.reset()
            self.parent.get_submenu("new_world").world_type.reset()
            self.parent.set_submenu("new_world")

        if self.load_game_btn.just_pressed :
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            # self.parent.load_game()
            # self.parent.current_scene = 1
            self.parent.get_submenu("load").selected_save = None
            self.parent.get_submenu("load").update_saves()
            self.parent.set_submenu("load")

        if self.settings_btn.just_pressed :
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.get_submenu("settings").load_settings()
            self.parent.set_submenu("settings")

        if self.credit_btn.just_pressed :
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.set_submenu("credits")

        if self.addons_btn.just_pressed :
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.set_submenu("addons")

        if self.quit_btn.just_pressed :
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.parent.running = False

        if self.screenshots_btn.just_pressed:
            def load_screenshots():
                try:
                    self.parent.get_submenu("screenshots").update_screenshots()
                    self.parent.set_submenu("screenshots")
                except Exception as e:
                    self.parent.set_game_scene("MainMenuScene")
                    logging.exception("Error Accured!")
                    self.parent.main_menu.submenu_id = 7

            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.selected_screenshot = None
            self.parent.loading_menu("Loading...", load_screenshots, ())

    def draw(self):

        screen.blit(LOGO_FONT.render("The Factory", True, "#ffffff"), (0, 60))
        screen.blit(LOGO_FONT.render("Must Grow", True, "#ffffff"), (0, 60 + LOGO_FONT.get_height()))
        # screen.blit(BIG_FONT.render("A Game By Gigores", True, "#505050"), (0, 60 + HUGE_FONT.get_height() * 2))
        screen.blit(BIG_FONT.render(f"{GAME_VERSION}", True, "#505050"), (0, RESOLUTION.y - BIG_FONT.get_height()))

        self.new_game_btn.draw()
        self.load_game_btn.draw()
        self.settings_btn.draw()
        self.credit_btn.draw()
        self.quit_btn.draw()
        self.screenshots_btn.draw()
        self.addons_btn.draw()

        texture_size = from_iterable(self.splash_texture.get_size()) + Vector(
            sin(self.parent.parent.animation_counter / 10) * 10, sin(self.parent.parent.animation_counter / 10) * 10)
        texture = pg.transform.scale(self.splash_texture, texture_size.as_tuple())
        splash_pos = Vector(500, 250) - Vector(texture.get_width() / 2, texture.get_height() / 2)
        screen.blit(texture, splash_pos.as_tuple())
