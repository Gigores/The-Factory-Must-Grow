from scripts.Entities.Buildings.Furniture.Stool import Stool
from scripts.Entities.Buildings.Workbench import Workbench
from scripts.constants import *
from random import randint, choice
from random import seed as random_seed
from perlin_noise import PerlinNoise
from fractal_noise import get_fractal_noise
from math import sin, cos
from scripts.Managers.GameAssets import ORE_TYPES, ORE_TYPE_TO_TILE, tiles
from scripts.Entities.Buildings.Walls.BrickWall import BrickWall
from scripts.Entities.Buildings.WoodenChest import WoodenChest
from scripts.Managers.GameAssets import starting_items
import logging


class WorldGenerator:

    def __init__(self, parent):

        self.parent = parent
        self.ruins_size = None
        self.ruins_pos = None

    @staticmethod
    def generate_perlin_noise(size: Vector, octaves, seed):

        perlin = PerlinNoise(octaves, seed)
        return [[perlin([i / size.x, j / size.y]) for j in range(size.x)] for i in range(size.y)]

    @staticmethod
    def generate_fractal_noise(size: Vector, octaves, seed):

        return get_fractal_noise(size.x, size.y, 0.1, octaves)

    def generate_flat(self):

        for x in range(len(self.parent.world.data)):
            for y in range(len(self.parent.world.data[x])):
                self.parent.world.data[x][y] = 7
                self.parent.biome_map[x][y] = 6

    @staticmethod
    def get_rectangle_border_pixels(center_x, center_y, width, height):
        half_width = width // 2
        half_height = height // 2

        left = center_x - half_width
        right = center_x + half_width
        top = center_y - half_height
        bottom = center_y + half_height

        border_pixels = []

        for x in range(left, right + 1) :
            border_pixels.append((x, top))
            border_pixels.append((x, bottom))

        for y in range(top + 1, bottom) :
            border_pixels.append((left, y))
            border_pixels.append((right, y))

        return border_pixels

    @staticmethod
    def get_inner_rectangle_pixels(center_x, center_y, width, height):
        half_width = width // 2
        half_height = height // 2

        left = center_x - half_width
        right = center_x + half_width
        top = center_y - half_height
        bottom = center_y + half_height

        if width <= 2 or height <= 2 :
            return []

        inner_pixels = [
            (x, y)
            for x in range(left + 1, right)
            for y in range(top + 1, bottom)
        ]

        return inner_pixels

    def generate_world(self, seed: int, island_type: int):

        random_seed(seed)

        ore_radius = TILE_SIZE.x * 15
        xpix = MAP_SIZE.x * CHUNK_SIZE.x
        ypix = MAP_SIZE.y * CHUNK_SIZE.y
        pix = MAP_SIZE * CHUNK_SIZE

        # drawing landscape
        octaves = 0.384615 * MAP_SIZE.x + 0.384615 * MAP_SIZE.y  # (MAP_SIZE.x + MAP_SIZE.y) / 2 / 1.3
        landscape_perlin = self.generate_perlin_noise(pix, octaves, seed)
        landscape_perlin2 = self.generate_perlin_noise(pix, int(octaves * 2), seed)
        sand_perlin = self.generate_perlin_noise(pix, octaves * 2, seed)
        landscape_factor = [[-(distance(Vector(xpix // 2, ypix // 2), Vector(i, j)) * 2 / xpix - 0.5) for j in range(ypix)] for i in range(xpix)]
        biome_perlin = PerlinNoise(seed=seed)
        biome_float_map = [[biome_perlin([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]

        rivers = None
        rivers2 = None

        if island_type == 1:

            rivers = self.generate_perlin_noise(pix, octaves, seed)
            rivers2 = self.generate_perlin_noise(pix, octaves, seed + 1)

        for x in range(xpix):
            for y in range(ypix):

                if rivers:

                    i = get_average([landscape_perlin[x][y], landscape_perlin2[x][y] / 6]) / 2 + landscape_factor[x][y]
                    rivers_avg = get_average([rivers[x][y], rivers2[x][y]])
                    value = -0.1 + landscape_factor[x][y] / 5 if 0 > rivers_avg > -0.2 and i > -0.15 else i

                else:

                    value = get_average([landscape_perlin[x][y], landscape_perlin2[x][y] / 6]) + landscape_factor[x][y]

                if value > 0:

                    tile = 0

                else:

                    if value > -0.15:
                        tile = 5
                    else:
                        tile = 4

                self.parent.world.data[y][x] = tile

        for x in range(len(self.parent.world.data)):
            for y in range(len(self.parent.world.data[x])):

                current_tiles = self.parent.world.data[x:x+3, y:y+3]
                current_tiles_in_a_row = []

                for a in current_tiles:
                    current_tiles_in_a_row += list(a)

                if 5 in current_tiles_in_a_row and 0 in current_tiles_in_a_row:
                    self.parent.world.data[x:x+3, y:y+3] = [[3, 3, 3], [3, 3, 3], [3, 3, 3]]

        # plt.imshow(landscape_float_map, cmap='gray')
        # plt.show()

        # drawing biome map
        biome_perlin = PerlinNoise(seed=seed)
        biome_float_map = [[biome_perlin([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)]

        # 0 - plains
        # 1 - forest
        # 2 - ocean
        # 3 - rockystuff
        # 4 - desert
        # 5 - beach
        biomes_area = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }

        # mapping biomes
        for x in range(len(biome_float_map)):
            for y, tile in enumerate(biome_float_map[x]):

                value = tile
                tile = self.parent.world.data[x][y]

                if tile not in [0, 7]:

                    if tile == 3:
                        self.parent.biome_map[x][y] = 5
                        biomes_area[5] += 1
                    else:
                        self.parent.biome_map[x][y] = 2
                        biomes_area[2] += 1

                else:

                    if value < 0:
                        self.parent.biome_map[x][y] = 0
                        biomes_area[0] += 1
                    else:
                        self.parent.biome_map[x][y] = 1
                        biomes_area[1] += 1

        self.generate_ruins()

        ores_amount = (biomes_area[0] + biomes_area[1]) // (CHUNK_SIZE.x * CHUNK_SIZE.y)

        # calculating stuff
        trees_amount1 = int(biomes_area[1] / 5)
        trees_amount2 = int(biomes_area[0] / 30)
        bushes_amount = int(biomes_area[0] / 20)
        pebbles_amount = int(biomes_area[1] / 10 + biomes_area[0] / 20)
        wheat_amount = int(biomes_area[0] / 200)
        wild_stuff_amount = int(biomes_area[1] / 200)
        bamboo_amount = int(biomes_area[5] / 100)

        # placing flowers
        for x in range(len(self.parent.world.data)):
            for y, tile in enumerate(self.parent.world.data[x]):

                if self.parent.biome_map[x][y] == 0 and not randint(0, 3):
                    self.parent.world.data[x][y] = 1

        self.parent.world.update_chunks()

        # planting trees
        for _ in range(round(trees_amount1)):

            pos = self.random_position([1])
            obj = self.parent.str_to_entity["Tree"](self.parent.generate_id(), pos, self.parent)
            obj.aftergen()
            self.parent.trees.append(obj)

        # planting a little bit more trees
        for _ in range(round(trees_amount2)):

            pos = self.random_position([0])
            obj = self.parent.str_to_entity["Tree"](self.parent.generate_id(), pos, self.parent)
            self.parent.trees.append(obj)

        # planting bushes
        for _ in range(bushes_amount):

            pos = self.random_position([0])
            obj = self.parent.str_to_entity["Bush"](self.parent.generate_id(), pos, self.parent)
            self.parent.bushes.append(obj)

        # throwing pebbles
        for _ in range(round(pebbles_amount)):

            pos = self.random_position([0, 1])
            obj = self.parent.str_to_entity["Pebble"](self.parent.generate_id(), pos, self.parent)
            self.parent.pebbles.append(obj)

        if self.parent.settings_manager.settings["survival_mode"] is True:

            # throwing wheat
            for _ in range(round(wheat_amount)):

                pos = self.random_position([0])
                for _ in range(randint(3, 5)):
                    obj = self.parent.str_to_entity["WildWheat"](self.parent.generate_id(), pos+Vector(randint(-TILE_SIZE.x * 2, TILE_SIZE.x * 2), randint(-TILE_SIZE.y * 2, TILE_SIZE.y * 2)), self.parent)
                    self.parent.bushes.append(obj)

            # throwing stuff
            for _ in range(round(wild_stuff_amount)):

                pos = self.random_position([1])
                type = choice(["WildTomato", "WildCarrot"])
                for _ in range(randint(3, 5)):

                    while True:

                        entity_pos = pos+Vector(randint(-TILE_SIZE.x * 2, TILE_SIZE.x * 2), randint(-TILE_SIZE.y * 2, TILE_SIZE.y * 2))
                        tile_x = entity_pos.x // TILE_SIZE.x
                        tile_y = entity_pos.y // TILE_SIZE.y

                        if self.parent.world.data[tile_x][tile_y] in [0, 1]: break

                    obj = self.parent.str_to_entity[type](self.parent.generate_id(), entity_pos, self.parent)
                    self.parent.bushes.append(obj)

            for _ in range(round(bamboo_amount)):

                pos = self.random_position([5])

                for _ in range(randint(3, 5)):

                    while True:

                        entity_pos = pos+Vector(randint(-TILE_SIZE.x * 2, TILE_SIZE.x * 2), randint(-TILE_SIZE.y * 2, TILE_SIZE.y * 2))
                        tile_x = entity_pos.x // TILE_SIZE.x
                        tile_y = entity_pos.y // TILE_SIZE.y

                        print(entity_pos)

                        if self.parent.world.data[tile_x][tile_y] in [3]: break

                    obj = self.parent.str_to_entity["WildBamboo"](self.parent.generate_id(), entity_pos, self.parent)
                    self.parent.bushes.append(obj)

        # elif island_type == 1:

        #     cactus_amount = biomes_area[4] // 30
        #     small_cactus_amount = cactus_amount // 10
        #     pebbles_amount = int(biomes_area[4] / 10)

        #     for i in range(cactus_amount):
        #         pos = self.random_position([4])
        #         obj = self.parent.str_to_entity["Cactus"](self.parent.generate_id(), pos, self.parent)
        #         self.parent.trees.append(obj)

        #     for i in range(small_cactus_amount):
        #         pos = self.random_position([4])
        #         obj = self.parent.str_to_entity["SmallCactus"](self.parent.generate_id(), pos, self.parent)
        #         self.parent.trees.append(obj)

        #     for i in range(round(pebbles_amount)):
        #         pos = self.random_position([4])
        #         obj = self.parent.str_to_entity["Pebble"](self.parent.generate_id(), pos, self.parent, "sand")
        #         self.parent.pebbles.append(obj)

        # elif island_type == 2:

        #     rocks_amount = biomes_area[3] / 30
        #     pebbles_amount = int(biomes_area[3] / 10)

        #     for i in range(round(rocks_amount)):
        #         pos = self.random_position([3])
        #         obj = self.parent.str_to_entity["Vein"](self.parent.generate_id(), pos, self.parent)
        #         self.parent.pebbles.append(obj)

        #     for i in range(round(pebbles_amount)):
        #         pos = self.random_position([3])
        #         obj = self.parent.str_to_entity["Pebble"](self.parent.generate_id(), pos, self.parent)
        #         self.parent.pebbles.append(obj)

        # elif island_type == 3:

        #     cactus_amount = biomes_area[1] // 15
        #     small_cactus_amount = cactus_amount // 10
        #     pebbles_amount = int(biomes_area[1] / 10)

        #     for i in range(cactus_amount):
        #         pos = self.random_position([1])
        #         obj = self.parent.str_to_entity["Fungus"](self.parent.generate_id(), pos, self.parent)
        #         self.parent.trees.append(obj)

            # for i in range(small_cactus_amount):
            #     pos = self.random_position([4])
            #     obj = SmallFungus(self.parent.generate_id(), pos, self.parent)
            #     self.parent.trees.append(obj)

        #     for i in range(round(pebbles_amount)):
        #         pos = self.random_position([1])
        #         obj = self.parent.str_to_entity["Pebble"](self.parent.generate_id(), pos, self.parent)
        #         self.parent.pebbles.append(obj)

        # throwing ores
        for i in ORE_TYPES:
            center_pos = self.random_position([0, 1])
            self.generate_ore(center_pos, i)

        for _ in range(ores_amount - len(ORE_TYPES)):
            center_pos = self.random_position([0, 1])
            self.generate_ore(center_pos)

        # throwing more ores
        # ore_types = ("iron", "stone", "copper", "coal", "zinc")
        # ore_radius_factor = ore_radius / 2
        # angle_factor = 20
        # for i, ore_type in enumerate(ore_types):
        #     ore_angle = 360 / len(ore_types) * i + randint(-angle_factor, angle_factor)
        #     ore_distance = ore_radius + randint(-int(ore_radius_factor), ore_radius_factor)

        #     pos = pg.Vector2(ore_distance, 0).rotate(ore_angle) + self.parent.world_center
        #     while not self.parent.world.data[int(pos.x)][int(pos.y)] in [0, 1]:
        #         ore_distance += TILE_SIZE.x
        #         pos = pg.Vector2(ore_distance, 0).rotate(ore_angle) + self.parent.world_center
        #     ore_distance += TILE_SIZE.x * 5

        #     pos = pg.Vector2(ore_distance, 0).rotate(ore_angle) + self.parent.world_center

        #     self.generate_ore(pos, ore_type)

        # self.buildings.append(WoodenChest(self.generate_id(), self.world_center, self))

        # self.draw_circle(self.parent.world.data, self.parent.world_center / TILE_SIZE, 5, 2)

        current_player_tile = (MAP_SIZE * CHUNK_SIZE // Vector(2, 2)).to_int()
        initial_pos = True
        current_degree = 0
        current_distance = 1
        while tiles[self.parent.world.data[current_player_tile.x][current_player_tile.y]].walk_speed < 1:
            initial_pos = False
            current_degree += 45
            if current_degree >= 360:
                current_degree -= 360
                current_distance += 1
            current_player_tile = (MAP_SIZE * CHUNK_SIZE // Vector(2, 2) + pg.Vector2(current_distance, 0).rotate(current_degree)).to_int()
        if not initial_pos:
            current_player_tile = (MAP_SIZE * CHUNK_SIZE // Vector(2, 2) + pg.Vector2(current_distance + 3, 0).rotate(current_degree)).to_int()

        self.parent.player.pos = current_player_tile * TILE_SIZE + TILE_SIZE // 2

    def random_position(self, avilable_biomes: list = [], banned_biomes: list = [], distance_points: list[tuple[Vector, int]] = []) -> Vector:

        tile_pos = Vector(randint(0, (MAP_SIZE * CHUNK_SIZE).x - 1), randint(0, (MAP_SIZE * CHUNK_SIZE).y - 1))
        pos = tile_pos * TILE_SIZE + Vector(randint(0, TILE_SIZE.x), randint(0, TILE_SIZE.y))
        biome = self.parent.biome_map[tile_pos.x][tile_pos.y]
        aprooved_dp = (i[1] <= distance(i[0], pos) for i in distance_points)
        miome_friendly = (biome in avilable_biomes or not len(avilable_biomes) and (biome not in banned_biomes))

        if miome_friendly and (all(aprooved_dp) or not len(distance_points)):

            if tile_pos.as_tuple() in self.get_rectangle_border_pixels(int(self.ruins_pos.x), int(self.ruins_pos.y), self.ruins_size.x, self.ruins_size.y) + self.get_inner_rectangle_pixels(int(self.ruins_pos.x), int(self.ruins_pos.y), self.ruins_size.x, self.ruins_size.y):
                try: return self.random_position(avilable_biomes, distance_points)
                except: return pos
            else:
                return pos

        else:

            try: return self.random_position(avilable_biomes, distance_points)
            except: return pos

    def generate_ore(self, pos, ore_type: str = None):

        deposit_amount = randint(1, 3)
        _type = ore_type if ore_type else choice(ORE_TYPES)
        center_pos = pos
        factor = TILE_SIZE.x * 4
        tile = ORE_TYPE_TO_TILE[_type]
        self.draw_circle(self.parent.world.data, Vector(center_pos.x // TILE_SIZE.x, center_pos.y // TILE_SIZE.y), randint(2, 3), tile)

        if deposit_amount == 1:

            pos = center_pos
            # self.parent.ores.append(self.parent.str_to_entity["Deposit"](self.parent.generate_id(), pos, self.parent, _type))

        else:

            r = 80
            for i in range(deposit_amount):

                iteration = 0
                while True:

                    iteration += 1
                    angle = 360 / deposit_amount * i + randint(-20, 20)
                    pos = center_pos + pg.Vector2(r, 0).rotate(angle) + Vector(randint(-factor, factor),
                                                                               randint(-factor, factor))

                    tile_x = int(pos.x // TILE_SIZE.x)
                    tile_y = int(pos.y // TILE_SIZE.y)

                    if not (self.parent.world.data[tile_x][tile_y] in [4, 5, 3]): break
                    if iteration > 1000: break

                if iteration > 1000: continue

                # self.parent.ores.append(self.parent.str_to_entity["Deposit"](self.parent.generate_id(), pos, self.parent, _type))

        vein_amount = deposit_amount * randint(1, 2)

        r = 80
        for i in range(vein_amount):

            iteration = 0
            while True:

                iteration += 1
                angle = 360 / vein_amount * i + randint(-20, 20)
                pos = center_pos + pg.Vector2(r, 0).rotate(angle) + Vector(randint(-factor, factor),
                                                                           randint(-factor, factor))
                tile_x = int(pos.x // TILE_SIZE.x)
                tile_y = int(pos.y // TILE_SIZE.y)

                if not (self.parent.world.data[tile_x][tile_y] in [4, 5, 3]): break
                if iteration > 1000: break

            if iteration > 1000: continue

            self.parent.ores.append(self.parent.str_to_entity["Vein"](self.parent.generate_id(), pos, self.parent, _type))

    @staticmethod
    def draw_circle(world: list[list[int]], center: Vector, radius: int, tile: int):
        x0, y0 = center.x, center.y
        x, y = radius, 0
        p = 1 - radius

        def set_tile(world, x, y, tile):
            if 0 <= x < len(world) and 0 <= y < len(world[0]):
                world[x][y] = tile

        # Заполняем линию по горизонтали от x1 до x2 на высоте y
        def fill_horizontal_line(x1, x2, y):
            for x in range(x1, x2 + 1):
                set_tile(world, x, y, tile)

        # Симметричные точки круга и заполнение линий между ними
        def plot_filled_circle_points(x0, y0, x, y):
            fill_horizontal_line(x0 - x, x0 + x, y0 + y)  # Верхняя часть
            fill_horizontal_line(x0 - x, x0 + x, y0 - y)  # Нижняя часть

        # Рисование заполненного круга
        while x >= y:
            plot_filled_circle_points(x0, y0, x, y)
            plot_filled_circle_points(x0, y0, y, x)  # Симметрия для вертикальной оси
            y += 1
            if p <= 0:
                p += 2 * y + 1
            else:
                x -= 1
                p += 2 * (y - x) + 1

    def generate_ruins(self):

        random_degree = randint(0, 359)
        radius = randint(5, 10)
        self.ruins_pos = (MAP_SIZE * CHUNK_SIZE / Vector(2, 2) + Vector(sin(random_degree), cos(random_degree)) * Vector(radius, radius))
        self.ruins_size = Vector(randint(4, 7), randint(4, 7))

        for x, y in self.get_rectangle_border_pixels(int(self.ruins_pos.x), int(self.ruins_pos.y), self.ruins_size.x, self.ruins_size.y):

            if randint(1, 3) != 1:
                self.parent.buildings.append(BrickWall(self.parent.generate_id(), Vector(x, y) * TILE_SIZE, self.parent))

        inner_tiles = self.get_inner_rectangle_pixels(int(self.ruins_pos.x), int(self.ruins_pos.y), self.ruins_size.x, self.ruins_size.y)
        for x, y in inner_tiles:

            if randint(1, 3) != 1:
                self.parent.world.data[x][y] = 254

        chest_pos = from_iterable(choice(inner_tiles))
        chest = WoodenChest(self.parent.generate_id(), chest_pos * TILE_SIZE + TILE_SIZE * Vector(0.5, 0.5), self.parent)
        if chest.inventory.can_fit_m(starting_items):
            chest.inventory.append_m(starting_items)
            chest.inventory.sort_by_name()
        else:
            logging.error("Not enough space to fit all starting items")
        self.parent.buildings.append(chest)

        workbench_pos = chest_pos
        while workbench_pos == chest_pos:
            workbench_pos = from_iterable(choice(inner_tiles))
        workbench = Workbench(self.parent.generate_id(), workbench_pos * TILE_SIZE + TILE_SIZE * Vector(0.5, 0.5), self.parent)
        self.parent.buildings.append(workbench)
