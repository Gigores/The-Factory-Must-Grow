import pygame as pg
from scripts.UI.MainMenuScreen.Submenu import Submenu
from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import TextButton, CLICK_SOUND, Scrollable, SaveButton, ENTER_SOUND
import os
from scripts.Classes.Registry.SubmenuRegistry import SubmenuRegistry


class LoadWorld(Submenu, metaclass=SubmenuRegistry):

    def __init__(self, parent, rect_width):

        super().__init__(parent, "load")

        self.rect_width = rect_width

        self.return_btn = TextButton(Vector(0, RESOLUTION.y - HUGE_FONT.get_height() * 2), rect_width, "Back")
        self.scroll1 = Scrollable(Vector(0, HUGE_FONT.get_height() * 2), Vector(rect_width, HUGE_FONT.get_height() * 5.5))
        self.selected_save = None
        self.play_btn = TextButton(Vector(0, self.scroll1.pos.y + self.scroll1.size.y + 5), rect_width, "Play", fixed_text_pos=True)
        self.rename_btn = TextButton(Vector(0, self.play_btn.pos.y + self.play_btn.rect.height), rect_width / 3, "Rename", fixed_text_pos=True, font=BIG_FONT)
        self.delete_btn = TextButton(Vector(0, self.play_btn.pos.y + self.play_btn.rect.height), rect_width, "Delete", fixed_text_pos=True, font=HUGEISH_FONT)
        self.dublicate_btn = TextButton(Vector(rect_width / 3 * 2, self.play_btn.pos.y + self.play_btn.rect.height), rect_width / 3, "Dublicat", fixed_text_pos=True, font=BIG_FONT)

    def update_saves(self):

        self.scroll1.clear()
        for i, file in enumerate(os.listdir(str(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER)))):
            try: screenshot = pg.image.load(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER, file, "screenshot.png"))
            except FileNotFoundError: screenshot = pg.image.load("assets/default_screenshot.png")
            self.scroll1.append_element(i, SaveButton(Vector(0, 200 * i), file.split(".")[0], self.rect_width, screenshot, selected=(i == self.selected_save)))

    def events(self, events: list):

        self.scroll1.events(events)

    def update(self):

        self.return_btn.update()

        self.scroll1.update()

        for i, (name, btn) in enumerate(self.scroll1.get_elements()) :
            if btn.just_pressed :
                CLICK_SOUND.stop()
                CLICK_SOUND.play()
                self.selected_save = i
                self.update_saves()

        if self.selected_save is not None :
            self.play_btn.update()
            self.delete_btn.update()
            # self.rename_btn.update()
            # self.dublicate_btn.update()

            if self.play_btn.just_pressed :
                ENTER_SOUND.play()
                file_name = os.listdir(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER))[self.selected_save]
                self.parent.parent.saves_manager.load_game(file_name)
                self.parent.parent.current_scene = "GameScene"
                self.parent.parent.entity_manager.update_active_chunks()
            if self.delete_btn.just_pressed :
                CLICK_SOUND.stop()
                CLICK_SOUND.play()
                file_name = os.listdir(os.path.join(APPDATA_FOLDER_PATH, SAVES_FOLDER))[self.selected_save]
                path = os.path.join(APPDATA_PATH, APPDATA_FOLDER, SAVES_FOLDER, file_name)
                for root, dirs, files in os.walk(path, topdown=False) :
                    for name in files :
                        os.remove(os.path.join(root, name))
                    for name in dirs :
                        os.rmdir(os.path.join(root, name))
                os.rmdir(path)
                self.update_saves()

        if self.return_btn.just_pressed :
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.set_submenu("hub")

    def draw(self):

        screen.blit(HUGE_FONT.render("Load game", True, "#ffffff"), (0, 60))

        self.return_btn.draw()
        self.scroll1.draw()
        if self.selected_save is not None :
            self.play_btn.draw()
            self.delete_btn.draw()
            # self.rename_btn.draw()
            # self.dublicate_btn.draw()
