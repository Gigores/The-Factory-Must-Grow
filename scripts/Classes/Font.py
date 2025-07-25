from pygame import font


class Font(font.Font):

    def get_height(self):

        return super().get_height() * 1.4
