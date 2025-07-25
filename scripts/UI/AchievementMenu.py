from scripts.UI.Components.BaseUIComponents import *
from scripts.Managers.GameAssets import *
from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Components.Bg import Bg
from scripts.UI.Achievements import Achievements
from scripts.UI.Entities.BaseUI import BaseUI


class AchivemenMenu(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)

        self.main_ui_size = from_iterable(BLANK.get_size()) * Vector(2, 2)
        self.main_ui_texture = pg.transform.scale(BLANK, self.main_ui_size.as_tuple())
        self.main_ui_pos = RESOLUTION / Vector(2, 2) - Vector(self.main_ui_size.x, self.main_ui_size.y) / Vector(2, 2)

        self.scrollbar_padding = 40
        self.scrollbar_pos = self.main_ui_pos + Vector(self.scrollbar_padding, self.scrollbar_padding)
        self.scrollbar_size = from_iterable(self.main_ui_texture.get_size()) - Vector(self.scrollbar_padding * 2,
                                                                                      self.scrollbar_padding * 2)
        self.scrollbar = Achievements(self.parent, self.scrollbar_pos, self.scrollbar_size)

        # self.scrollbar.add_obj("a1", Arrow(self.parent, self.scrollbar.objects["ach0"].pos, self.scrollbar.objects["ach3"].pos))
        # self.scrollbar.add_obj("a2", Arrow(self.parent, self.scrollbar.objects["ach0"].pos, self.scrollbar.objects["ach2"].pos, True))
        # self.scrollbar.add_obj("a3", Arrow(self.parent, self.scrollbar.objects["ach0"], self.scrollbar.objects["ach4"]))

        self.achievement_list: tuple[tuple[str, Vector], ...] = ()

        self.bg = Bg()
        self.bg.blit(self.main_ui_texture, self.main_ui_pos.as_tuple())

    def draw(self, display):

        self.bg.draw()
        self.scrollbar.draw()

    def update(self, obj):

        self.scrollbar.update()
        pass

    def events(self, events):

        self.scrollbar.events(events)
        pass
