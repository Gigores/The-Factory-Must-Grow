from scripts.UI.Components.BaseUIComponents import *
from scripts.Managers.GameAssets import *


BACKGROUND = pg.image.load("assets/achievements_bg.png")


class Achievements(Scrollbar):

    def __init__(self, parent, pos, size):

        super().__init__(parent, pos, size, left_right=True, bg_image=BACKGROUND)

        for i, ach in enumerate(achievements):
            if ach.parent is not None:
                obj = Arrow(self.parent, ach.visual_data.pos, achievements[ach.parent].visual_data.pos, ach.fixed_arrow)
                self.add_obj(f"arr{i}", obj)
        for i, ach in enumerate(achievements):
            split_lines = ""
            curlen = 0
            for word in ach.description.split():
                if curlen + len(word) > 30:
                    split_lines += "<nl>"
                    curlen = 0
                split_lines += word + " "
                curlen += len(word)
            size = ach.visual_data.size
            texture = pg.Surface((size * Vector(1.2, 1.4)).as_tuple())
            texture.blit(pg.transform.scale(BUTTON, (size * Vector(1.2, 1.4)).as_tuple()), (0, 0))
            texture.blit(pg.transform.scale(items[ach.icon].texture, size.as_tuple()),
                         (size * Vector(0.1, 0.1)).as_tuple())
            text = f"<col hex='00FF00'>{ach.name.upper()}<col><nl>{split_lines}"
            obj = AchievementDisplay(self.parent, ach.visual_data.pos, texture, text, i)
            self.add_obj(f"ach{i}", obj)

    def draw(self):

        self._surf.fill("#000000")

        if self.bg_image :
            for y in range(ceil(self.size.y / self.bg_image.get_height()) + 1) :
                for x in range(ceil(self.size.x / self.bg_image.get_width()) + 1) :
                    pos = from_iterable(self.bg_image.get_size()) * Vector(x, y) + \
                          Vector(self._offset.x % self.bg_image.get_width(),
                                 self._offset.y % self.bg_image.get_height()) - \
                          from_iterable(self.bg_image.get_size())
                    self._surf.blit(self.bg_image, pos.as_tuple())

        for obj in self.objects.values() :
            obj.draw(self._surf)

        for obj in self.objects.values():
            if isinstance(obj, AchievementDisplay):
                obj.draw_text(self._surf)

        screen.blit(self._surf, self.pos.as_tuple())
