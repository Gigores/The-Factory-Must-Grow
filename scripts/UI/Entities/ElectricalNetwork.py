from scripts.Classes.Registry.UIRegistry import UIRegistry
from scripts.UI.Entities.BaseUI import BaseUI
import pygame as pg
from scripts.constants import *
from scripts.UI.Components.BaseUIComponents import *
from scripts.UI.Components.Bg import Bg


def format_power(watts):
    units = ["W", "kW", "MW", "GW", "TW", "PW", "EW", "ZW", "YW"]
    index = 0

    while abs(watts) >= 1000 and index < len(units) - 1:
        watts /= 1000
        index += 1

    formatted_power = f"{watts:.2f}".rstrip('0').rstrip('.')
    return f"{formatted_power} {units[index]}"


class ElectricalNetwork(BaseUI, metaclass=UIRegistry):

    def __init__(self, parent):

        super().__init__(parent)
        self.obj = None

        main_ui_texture_size = from_iterable(BLANK.get_size()) * Vector(2, 2)
        main_ui_texture = load_texture("assets/ingame_UI/empty_screen.png", main_ui_texture_size)
        main_ui_pos = RESOLUTION / Vector(2, 2) - main_ui_texture_size / Vector(2, 2)

        self.display_pos = main_ui_pos + main_ui_texture_size / Vector(12.857142857142857142857142857143, 9.7142857142857142857142857142857)
        display_spacing = main_ui_texture_size / Vector(9, 6.8) - main_ui_texture_size / Vector(12.857142857142857142857142857143, 9.7142857142857142857142857142857)
        display_size = main_ui_texture_size / Vector(1.1842105263157894736842105263158, 1.5454545454545454545454545454545)

        self.WHITE_NOISE = [load_texture(f"assets/ingame_UI/white_noise/white_noise-{i}.png", display_size) for i in range(6)]
        for texture in self.WHITE_NOISE:
            texture.set_alpha(32)

        caption_pos = self.display_pos + display_spacing
        caption_text = "Electric Network Status"
        caption_surf = BIG_FONT.render(caption_text, True, "#00ff00")

        network_balance_pos = caption_pos + Vector(0, BIG_FONT.get_height() * 2)
        network_balance_text = "Network balance:          "
        network_balance_surf = FONT.render(network_balance_text, True, "#00FF00")
        self.network_balance_pos_dynamic = network_balance_pos + Vector(network_balance_surf.get_width(), 0)

        consumers_amount_pos = network_balance_pos + Vector(0, FONT.get_height() * 2)
        consumers_amount_text = "Active consumers amount:  "
        consumers_amount_surf = FONT.render(consumers_amount_text, True, "#00FF00")
        self.consumers_amount_pos_dynamic = consumers_amount_pos + Vector(consumers_amount_surf.get_width(), 0)

        consumption_amount_pos = consumers_amount_pos + Vector(0, FONT.get_height())
        consumption_amount_text = "Total consumption:        "
        consumption_amount_surf = FONT.render(consumption_amount_text, True, "#00FF00")
        self.consumption_amount_pos_dynamic = consumption_amount_pos + Vector(consumption_amount_surf.get_width(), 0)

        generators_amount_pos = consumption_amount_pos + Vector(0, FONT.get_height() * 2)
        generators_amount_text = "Active genrators amount:  "
        generators_amount_surf = FONT.render(generators_amount_text, True, "#00FF00")
        self.generators_amount_pos_dynamic = generators_amount_pos + Vector(generators_amount_surf.get_width(), 0)

        generation_amount_pos = generators_amount_pos + Vector(0, FONT.get_height())
        generation_amount_text = "Total generation:         "
        generation_amount_surf = FONT.render(generation_amount_text, True, "#00FF00")
        self.generation_amount_pos_dynamic = generation_amount_pos + Vector(generation_amount_surf.get_width(), 0)

        self.bg = Bg()
        self.bg.fill("#784345")
        self.bg.set_colorkey("#784345")
        self.bg.blit(main_ui_texture, main_ui_pos.as_tuple())
        self.bg.blit(caption_surf, caption_pos.as_tuple())
        self.bg.blit(network_balance_surf, network_balance_pos.as_tuple())
        self.bg.blit(consumers_amount_surf, consumers_amount_pos.as_tuple())
        self.bg.blit(consumption_amount_surf, consumption_amount_pos.as_tuple())
        self.bg.blit(generators_amount_surf, generators_amount_pos.as_tuple())
        self.bg.blit(generation_amount_surf, generation_amount_pos.as_tuple())

    def draw(self, display):

        self.bg.draw()

        if self.obj and self.obj.network_info:

            screen.blit(FONT.render(f"{format_power(self.obj.network_info['balance'])}", True, "#00ff00"), self.network_balance_pos_dynamic.as_tuple())
            screen.blit(FONT.render(f"{len(self.obj.network_info['consumers'])}", True, "#00ff00"), self.consumers_amount_pos_dynamic.as_tuple())
            screen.blit(FONT.render(f"{format_power(self.obj.network_info['total_demand'])}", True, "#00ff00"), self.consumption_amount_pos_dynamic.as_tuple())
            screen.blit(FONT.render(f"{len(self.obj.network_info['generators'])}", True, "#00ff00"), self.generators_amount_pos_dynamic.as_tuple())
            screen.blit(FONT.render(f"{format_power(self.obj.network_info['total_generation'])}", True, "#00ff00"), self.generation_amount_pos_dynamic.as_tuple())

        screen.blit(self.WHITE_NOISE[self.parent.animation_counter // 5 % len(self.WHITE_NOISE)], self.display_pos.as_tuple())

    def update(self, obj):

        self.obj = obj

    def events(self, events):

        pass
