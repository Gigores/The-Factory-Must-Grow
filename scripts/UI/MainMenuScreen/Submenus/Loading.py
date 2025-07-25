import pygame as pg
from scripts.UI.MainMenuScreen.Submenu import Submenu
from scripts.constants import *
from scripts.UI.Components.DarkThemeComponents import TextButton, CLICK_SOUND
from scripts.Classes.Registry.SubmenuRegistry import SubmenuRegistry


class Loading(Submenu, metaclass=SubmenuRegistry):

    def __init__(self, parent, rect_width):

        super().__init__(parent, "loading")

        self.rect_width = rect_width

        self.loading_animation = [pg.transform.scale_by(pg.image.load(f"assets/ingame_UI/loading/loading{i+1}.png"), 14) for i in range(len(os.listdir("assets/ingame_UI/loading"))-1)]
        self.loading_x = rect_width / 2 - self.loading_animation[0].get_width() / 2

    def draw(self):

        text_surf = HUGE_FONT.render(self.parent.message, True, "#ffffff")
        text_x = self.rect_width / 2 - text_surf.get_width() / 2
        screen.blit(text_surf, (text_x, 500))
        screen.blit(self.loading_animation[self.parent.parent.animation_counter // 4 % len(self.loading_animation)],
                    (self.loading_x, 650))
