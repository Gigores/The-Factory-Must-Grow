import os.path
from scripts.UI.Components.DarkThemeComponents import *
from random import randint
from math import sin, ceil
import win32clipboard
from io import BytesIO
from PIL import Image
import win32con
import threading
import scripts.UI.MainMenuScreen.Submenus


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


class MainMenu:

    def __init__(self, parent):

        self.parent = parent
        self.submenu_id = 0

        self.rect_line_width = 8
        self.rect_width = RESOLUTION.x / 12 * 5
        self.main_rect = pg.Rect(-self.rect_line_width, -self.rect_line_width, self.rect_width + self.rect_line_width * 2, RESOLUTION.y + self.rect_line_width * 2)
        self.thread = None
        self.message = ""

        self.bg_image_size = TILE_SIZE * Vector(7, 7)
        self.bg_image = load_texture("assets/itch_io_bg.png", self.bg_image_size)

        self.submenus = [submenu_class(self, self.rect_width) for submenu_class in SUBMENUS]

    def set_submenu(self, unique_code: any):

        for i, submenu in enumerate(self.submenus):
            if submenu.unique_code == unique_code:
                self.submenu_id = i
                break

    def get_submenu(self, unique_code: any):

        for i, submenu in enumerate(self.submenus):
            if submenu.unique_code == unique_code:
                return submenu

    def events(self, events):

        self.submenus[self.submenu_id].events(events)

    def loading_menu(self, text: str, target_function: callable, args: tuple):

        self.submenu_id = 6
        self.message = text

        self.thread = threading.Thread(target=target_function, args=args)
        self.thread.start()

    def update(self):

        self.submenus[self.submenu_id].update()

    def draw(self):

        for y in range(ceil(RESOLUTION.y / self.bg_image_size.y) + 1):
            for x in range(ceil(RESOLUTION.x / self.bg_image_size.x) + 1):
                dpos = Vector(self.parent.animation_counter % self.bg_image_size.x, self.parent.animation_counter % self.bg_image_size.y)
                screen.blit(self.bg_image, ((x - 1) * self.bg_image_size.x + dpos.x, (y - 1) * self.bg_image_size.y + dpos.y))

        pg.draw.rect(screen, "#000000", self.main_rect)
        pg.draw.rect(screen, "#ffffff", self.main_rect, self.rect_line_width)

        self.submenus[self.submenu_id].draw()
