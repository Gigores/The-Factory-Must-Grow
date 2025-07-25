from scripts.constants import *
from PgHelp import *
from math import sin
from scripts.Managers.GameAssets import tiles, items


class Player:

    def __init__(self, parent):

        self.parent = parent
        self.pos = MAP_SIZE * CHUNK_SIZE * TILE_SIZE / Vector(2, 2)
        self.speed = PLAYER_SPEED
        self.health = MAX_PLAYER_HEALTH
        self.hunger = MAX_PLAYER_HUNGER
        self.__anim_counter = 0
        self.__anim_counter2 = 0
        self.textures = {
            fn.split('.')[0]: pg.transform.scale(pg.image.load("assets/player/" + fn).convert_alpha(), (TILE_SIZE * PLAYER_SIZE).as_tuple()) for fn in os.listdir("assets/player")
        }
        self.__texture_offset = Vector((TILE_SIZE.x * PLAYER_SIZE.x) / 2, TILE_SIZE.y * PLAYER_SIZE.y)
        self.inventory_cursor = 0
        self.tobeddeleted = False
        self.do_draw = (True, True, True, True)
        self.rect = self.textures["adown1"].get_rect()
        self.tile_pos = Vector(0, 0)
        self.tile = 4
        self.damage_sound = pg.mixer.Sound("sound/damage.wav")
        self.y_vel = 0
        self.d_y = 0
        self.show_texture = True
        self.dying = False
        self.death_timer = 0
        self.use_collisions = True
        self.last_pressed = None

    def move(self, direction: Vector):

        if not self.dying:
            speed = self.speed * tiles[self.tile].walk_speed

            if direction.x != 0 and direction.y != 0:
                speed /= (2 ** 0.5)

            self.pos.x += speed * direction.x
            self.pos.y += speed * direction.y

            """
            if (self.pos + self.parent.offset).y <= RESOLUTION.y / 2 - CAMERA_BOX_SIZE.y / 2:
                self.parent.offset.y += speed
                if self.parent.offset.y > 0:
                    self.parent.offset.y = 0
            if (self.pos + self.parent.offset).x <= RESOLUTION.x / 2 - CAMERA_BOX_SIZE.x / 2:
                self.parent.offset.x += speed
                if self.parent.offset.x > 0:
                    self.parent.offset.x = 0
            if (self.pos + self.parent.offset).y >= RESOLUTION.y / 2 + CAMERA_BOX_SIZE.y / 2:
                self.parent.offset.y -= speed
                if self.parent.offset.y < -(MAP_SIZE * CHUNK_SIZE * TILE_SIZE - RESOLUTION).y:
                    self.parent.offset.y = -(MAP_SIZE * CHUNK_SIZE * TILE_SIZE - RESOLUTION).y
            if (self.pos + self.parent.offset).x >= RESOLUTION.x / 2 + CAMERA_BOX_SIZE.x / 2:
                self.parent.offset.x -= speed
                if self.parent.offset.x < -(MAP_SIZE * CHUNK_SIZE * TILE_SIZE - RESOLUTION).x:
                    self.parent.offset.x = -(MAP_SIZE * CHUNK_SIZE * TILE_SIZE - RESOLUTION).x
                if self.parent.offset.x > 0:
                    self.parent.offset.x = 0
            """
            self.update()
            if (not tiles[self.tile].walkable) and self.use_collisions:
                self.pos.x += speed * (direction.x * -1)
                self.pos.y += speed * (direction.y * -1)
            if self.use_collisions:
                for entity in self.parent.entities_to_draw:
                    if "hitbox" in entity.__dict__:
                        if entity.hitbox.collidepoint((self.pos + self.parent.offset).as_tuple()) and entity.__dict__.get("use_hitbox", True):
                            self.pos.x += speed * (direction.x * -1)
                            self.pos.y += speed * (direction.y * -1)
                            break

    def draw(self):

        if self.parent.go_up or self.parent.go_left or self.parent.go_down or self.parent.go_right:
            self.__anim_counter += 0.4; hf = 6; self.__anim_counter2 += 0.01
        else:
            self.__anim_counter += 0.1; hf = 4

        texture_new_size = \
            Vector(
                TILE_SIZE.x * PLAYER_SIZE.x - sin(self.__anim_counter) * hf,
                TILE_SIZE.y * PLAYER_SIZE.y + sin(self.__anim_counter) * hf
            )

        texture_id = int(self.__anim_counter2 * 10 % 2 + 1)

        tile_x = int(self.pos.x // TILE_SIZE.x)
        tile_y = int(self.pos.y // TILE_SIZE.y)

        is_in_water = self.parent.world.data[tile_x][tile_y] in [4, 5]
        s = "" + "_w" * int(is_in_water)

        if self.dying:
            texture_name = "dead"
        elif self.parent.go_up:
            texture_name = f"aup{s}{texture_id}"
        elif self.parent.go_down:
            texture_name = f"adown{s}{texture_id}"
        elif self.parent.go_left:
            texture_name = f"aleft{s}{texture_id}"
        elif self.parent.go_right:
            texture_name = f"aright{s}{texture_id}"
        else:
            texture_name = f"down{s}"

        if self.dying: texture = self.textures[texture_name]
        else: texture = pg.transform.scale(self.textures[texture_name], texture_new_size.as_tuple())
        screen_pos = self.pos + self.parent.offset + Vector(0, -self.d_y)
        size_offset = Vector(
            -(texture_new_size.x - TILE_SIZE.x * PLAYER_SIZE.x) / 2,
            -(texture_new_size.y - TILE_SIZE.y * PLAYER_SIZE.y)
        )
        if self.dying: texture_pos = (screen_pos - self.__texture_offset).as_tuple()
        else: texture_pos = (screen_pos - self.__texture_offset + size_offset).as_tuple()

        if self.show_texture: self.parent.screen.blit(texture, texture_pos)
        item = items.get(self.parent.inventory.n[self.inventory_cursor], None)
        item_pos = list(texture_pos)
        item_pos[0] += TILE_SIZE.x / 3
        item_pos[1] += (TILE_SIZE.y / 8) * int(is_in_water)
        if item and not self.dying: self.parent.screen.blit(pg.transform.scale(item.texture, TILE_SIZE.as_tuple()), item_pos)
        
        #draw_brackets(screen, self.rect)

        # pg.draw.circle(screen, "#ff00ff", (self.pos+offset).as_tuple(), 5)

        # pg.draw.rect(screen, "#ff0000", self.rect, 2)

    def update(self):

        screen_pos = self.pos + self.parent.offset + Vector(0, -self.d_y)
        self.rect.x = (screen_pos - self.__texture_offset).x
        self.rect.y = (screen_pos - self.__texture_offset).y
        self.tile_pos = Vector(int(self.pos.x // TILE_SIZE.x), int(self.pos.y // TILE_SIZE.y))
        self.tile = self.parent.world.data[self.tile_pos.x][self.tile_pos.y]
        self.y_vel += 0.5
        self.d_y -= self.y_vel
        if self.d_y < 1:
            self.d_y = 0
            self.y_vel = 0
            self.show_texture = not (self.dying and self.d_y == 0)
        else:
            self.show_texture = self.parent.animation_counter // 10 % 2 == 0

        if self.parent.settings_manager.settings["survival_mode"]:

            if self.parent.animation_counter % (60 * 8) == 0:
                if self.hunger > 0:
                    self.hunger -= 1
                    if self.hunger > MAX_PLAYER_HUNGER * 0.8:
                        self.health += 2
                        if self.health > MAX_PLAYER_HEALTH:
                            self.health = MAX_PLAYER_HEALTH
                else:
                    self.damage(5)

        if self.death_timer > 0:
            self.death_timer += 1
            if self.death_timer >= 60 * 3:
                self.pos = MAP_SIZE * CHUNK_SIZE * TILE_SIZE / Vector(2, 2)
                self.death_timer = 0
                self.dying = False
                screen_pos = self.pos + self.parent.offset + Vector(0, -self.d_y)
                self.rect.x = (screen_pos - self.__texture_offset).x
                self.rect.y = (screen_pos - self.__texture_offset).y
                self.health = MAX_PLAYER_HEALTH
                self.hunger = MAX_PLAYER_HUNGER

        if self.dying and self.d_y == 0 and not self.death_timer > 0:
            for i, (item_name, item_amount) in enumerate(zip(self.parent.inventory.n, self.parent.inventory.a)):
                self.parent.drop_items(self.pos, item_name, item_amount)
                self.parent.inventory.pop_from_slot(i, item_amount)
            self.death_timer = 1

    def damage(self, value: int):

        if self.health > 0:
            self.health -= value
            self.damage_sound.stop()
            self.damage_sound.play()
            self.y_vel = -10
            if self.health < 1:
                self.dying = True

    def check_is_dead(self):

        self.damage_sound.stop()
        self.damage_sound.play()
        self.y_vel = -10
        if self.health < 1:
            self.dying = True

    def dumb(self) -> dict:

        return {
            "pos": self.pos.as_tuple(),
            "hp": self.health,
            "hunger": self.hunger,
        }

    def load(self, data: dict):

        self.pos = Vector(data["pos"][0], data["pos"][1])
        if "hp" in data: self.health = data["hp"]
        else: self.health = MAX_PLAYER_HEALTH
        if "hunger" in data: self.hunger = data["hunger"]
        else: self.hunger = MAX_PLAYER_HUNGER
