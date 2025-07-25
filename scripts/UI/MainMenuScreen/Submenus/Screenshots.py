import pygame as pg
from scripts.UI.MainMenuScreen.Submenu import Submenu
from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import TextButton, CLICK_SOUND, Scrollable, ImageButton
import os
from scripts.Classes.Registry.SubmenuRegistry import SubmenuRegistry

import win32clipboard
from io import BytesIO
from PIL import Image
import win32con


def send_image_to_clipboard(image_path):

    image = Image.open(image_path)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_DIB, data)
    win32clipboard.CloseClipboard()


class Screenshots(Submenu, metaclass=SubmenuRegistry):

    def __init__(self, parent, rect_width):

        super().__init__(parent, "screenshots")

        self.rect_width = rect_width

        self.return_btn = TextButton(Vector(0, RESOLUTION.y - HUGE_FONT.get_height() * 2), rect_width, "Back")
        self.screenshots_scroll = Scrollable(Vector(0, HUGE_FONT.get_height() * 2), Vector(rect_width, HUGE_FONT.get_height() * 6))
        self.selected_screenshot = None
        self.copy_screenshot_btn = TextButton(Vector(0, self.screenshots_scroll.pos.y + self.screenshots_scroll.size.y + 5), rect_width, "copy", fixed_text_pos=True)

    def update_screenshots(self):

        self.screenshots_scroll.clear()
        element_size = Vector(self.rect_width, (self.rect_width * RESOLUTION.y) // RESOLUTION.x)
        image_size = element_size - Vector(ImageButton.BORDER_WIDTH * 2, ImageButton.BORDER_WIDTH * 2)
        for i, file in enumerate(reversed(os.listdir(str(os.path.join(APPDATA_FOLDER_PATH, SCREENSHOT_FOLDER))))):
            self.screenshots_scroll.append_element(i, ImageButton(Vector(0, element_size.y * i), element_size, load_texture(os.path.join(APPDATA_FOLDER_PATH, SCREENSHOT_FOLDER, file), image_size), (i == self.selected_screenshot)))

    def events(self, events: list):

        self.screenshots_scroll.events(events)

    def update(self):

        self.return_btn.update()
        self.copy_screenshot_btn.update()

        if self.return_btn.just_pressed :
            CLICK_SOUND.stop()
            CLICK_SOUND.play()
            self.parent.set_submenu("hub")
        self.screenshots_scroll.update()

        if self.copy_screenshot_btn.just_pressed and self.selected_screenshot is not None :
            send_image_to_clipboard(os.path.join(APPDATA_FOLDER_PATH, SCREENSHOT_FOLDER, list(
                reversed(os.listdir(os.path.join(APPDATA_FOLDER_PATH, SCREENSHOT_FOLDER))))[self.selected_screenshot]))
            CLICK_SOUND.stop()
            CLICK_SOUND.play()

        for i, (name, btn) in enumerate(self.screenshots_scroll.get_elements()) :
            if btn.just_pressed :
                CLICK_SOUND.stop()
                CLICK_SOUND.play()
                self.selected_screenshot = i
                for i2, (name2, btn2) in enumerate(self.screenshots_scroll.get_elements()) :
                    btn2.selected = i2 == self.selected_screenshot
                break

    def draw(self):

        screen.blit(HUGE_FONT.render("Screenshots", True, "#ffffff"), (0, 60))

        self.return_btn.draw()
        self.screenshots_scroll.draw()
        if self.selected_screenshot is not None:
            self.copy_screenshot_btn.draw()
