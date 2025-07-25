from scripts.constants import *
from pickle import dump, load
import os
import pygame as pg


DEFAULT_SETTINGS = {

    "go_up": pg.K_w,
    "go_left": pg.K_a,
    "go_down": pg.K_s,
    "go_right": pg.K_d,

    "backpack": pg.K_e,
    "achievements": pg.K_l,
    "map": pg.K_m,
    "esc_menu": pg.K_ESCAPE,
    "drop_item": pg.K_z,

    "hide_ui": pg.K_F1,
    "screenshot": pg.K_F2,
    "terminal": pg.K_F12,

    "enable_terminal": True,
    "survival_mode": False
}
FILE_NAME = "settings.pkl"


class SettingsManager:

    def __init__(self, parent):

        self.parent = parent
        self.settings = DEFAULT_SETTINGS

    def set_default_settings(self):

        self.save_settings(DEFAULT_SETTINGS)

    def save_settings(self, settings: dict):

        self.settings = settings

        with open(os.path.join(APPDATA_FOLDER_PATH, FILE_NAME), "wb") as f:
            dump(settings, f)

    def load_settings(self):

        if not os.path.exists(os.path.join(APPDATA_FOLDER_PATH, FILE_NAME)):
            self.set_default_settings()
            return

        self.settings = DEFAULT_SETTINGS.copy()
        with open(os.path.join(APPDATA_FOLDER_PATH, FILE_NAME), "rb") as f:
            file_settings: dict = load(f)

        print("INFO: loading settings: ", file_settings.items())

        for key, item in file_settings.items():
            self.settings[key] = item
