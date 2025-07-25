from scripts.UI.Components.BaseUIComponents import *
from collections import deque
from scripts.Managers.GameAssets import *


SPLASH_SIZE = RESOLUTION / Vector(3, 10)
SPLASH_PADDING = 20
INSIDE_SPLASH_PADDING = 20
ITEM_SIZE = Vector(SPLASH_SIZE.y * 0.85 - INSIDE_SPLASH_PADDING * 2, SPLASH_SIZE.y * 0.85 - INSIDE_SPLASH_PADDING * 2)
BACKGROUND_COLOR = "#faff00"

SPLASH_TEXTURE = pg.transform.scale(pg.image.load("assets/ingame_UI/blank.png"), SPLASH_SIZE.as_tuple())
SOUND = pg.mixer.Sound("sound/achievement.mp3")
SOUND.set_volume(0.5)

TIME = FPS * 6
ENTER_TIME = FPS * 1.5
ESCAPE_TIME = FPS * 1.5


class AchievementsVisualsManager:

    def __init__(self, parent):

        self.parent = parent
        self.queue = deque()
        self.current_achievement_id = None
        self.splash_pos = Vector(0, 0)
        self.animation_counter = 0
        self.splash_texture = pg.Surface((1, 1))

    def render_text(self, text, pos, color="#000000"):
        x, y = pos
        for word in text.split():
            surf = FONT.render(word + ' ', True, color)
            if x + surf.get_width() > SPLASH_SIZE.x:
                x = INSIDE_SPLASH_PADDING + ITEM_SIZE.x + INSIDE_SPLASH_PADDING
                y += FONT.get_height()
            self.splash_texture.blit(surf, (x, y))
            x += surf.get_width()
        return x, y

    def reset(self):

        self.current_achievement_id = None
        self.animation_counter = 0
        SOUND.stop()

    def update_splash_texture(self):
        self.splash_texture = pg.Surface(SPLASH_SIZE.as_tuple())
        self.splash_texture.fill(BACKGROUND_COLOR)
        self.splash_texture.blit(SPLASH_TEXTURE, (0, 0))
        draw_item(self.splash_texture, achievements[self.current_achievement_id].icon, 1,
                  (INSIDE_SPLASH_PADDING, INSIDE_SPLASH_PADDING),
                  ITEM_SIZE.as_tuple())
        self.splash_texture.blit(FONT.render("Achievement Get!", True, "#00ff00"),
                                 (INSIDE_SPLASH_PADDING + ITEM_SIZE.x + INSIDE_SPLASH_PADDING, INSIDE_SPLASH_PADDING))
        self.render_text(achievements[self.current_achievement_id].name,
                         (INSIDE_SPLASH_PADDING + ITEM_SIZE.x + INSIDE_SPLASH_PADDING, INSIDE_SPLASH_PADDING +
                          FONT.get_height()))
        self.splash_texture.set_colorkey(BACKGROUND_COLOR)

    def update(self):

        if self.animation_counter == TIME:
            self.reset()

        if self.queue and self.current_achievement_id is None:
            self.current_achievement_id = self.queue.popleft()
            self.update_splash_texture()
            SOUND.play()

        if self.current_achievement_id is not None:
            self.animation_counter += 1
            if self.animation_counter < ENTER_TIME:
                self.calculate_splash_pos_when_enter()
            elif self.animation_counter > TIME - ESCAPE_TIME:
                self.calculate_splash_pos_when_escape()
            else:
                self.splash_pos = Vector(RESOLUTION.x - (SPLASH_SIZE.x + SPLASH_PADDING), SPLASH_PADDING)

    def calculate_splash_pos_when_enter(self):

        self.splash_pos = Vector(
            RESOLUTION.x - (SPLASH_SIZE.x + SPLASH_PADDING) * (self.animation_counter / ENTER_TIME),
            SPLASH_PADDING)

    def calculate_splash_pos_when_escape(self):

        self.splash_pos = Vector(RESOLUTION.x - (SPLASH_SIZE.x + SPLASH_PADDING),
                                 SPLASH_PADDING - ((SPLASH_SIZE.y + SPLASH_PADDING) * (self.animation_counter - TIME +
                                                                                       ESCAPE_TIME) / ESCAPE_TIME))

    def draw(self):

        if self.current_achievement_id is not None:
            screen.blit(self.splash_texture, self.splash_pos.as_tuple())
