from PgHelp import Vector
from scripts.constants import *
from scripts.Managers.GameAssets import ENTITIES, tiles, items
import os, json
import re


class Enterpreter :

    def __init__(self, parent) :

        self.parent = parent
        self.variables = None

        self.reset()

    def reset(self):

        self.variables = dict()

    def get_argunent(self, args, argument_id, argument_name, required=True, default_value=None):

        try:
            arg = args[argument_id]
            if arg.startswith('$'):
                var_name = arg[1:]
                if var_name in self.variables.keys():
                    return self.variables[var_name]
                else:
                    raise NameError(f"name {var_name} is not defined")
            else:
                return arg
        except:
            if required:
                raise IndexError(f"Expected argument '{argument_name}' at position {argument_id}")
            else:
                return default_value

    def execute_input(self, input):

        parts = input.split()

        if not parts :
            return

        try:
            string_id, command_name, *args = parts
            string_id = int(string_id)
        except ValueError:
            string_id = None
            command_name, *args = parts

        try:

            if string_id is None:
                self.execute_input_command(command_name, args)
            else:
                self.parent.current_program[string_id] = [command_name, args]
                print(self.parent.current_program)

        except Exception as e:
            self.parent.throw_error(e)
        else:
            self.parent.print("Success")

    def execute_command(self, game, command, args, running_script=False):

        if command == "set_player_speed":
            speed = int(self.get_argunent(args, 0, "speed as integer"))
            game.player.speed = speed
        elif command == "teleport":
            x = int(self.get_argunent(args, 0, "x as integer"))
            y = int(self.get_argunent(args, 1, "y as integer"))
            game.player.pos.x = x
            game.player.pos.y = y
        elif command == "set_health":
            health = int(self.get_argunent(args, 0, "health points as integer"))
            game.player.health = health
        elif command == "set_hunger":
            hunger = int(self.get_argunent(args, 0, "hunger points as integer"))
            game.player.hunger = hunger
        elif command == "kill":
            game.player.damage(10000)
        elif command == "get_item":
            item_name = self.get_argunent(args, 0, "item name")
            item_amount = int(self.get_argunent(args, 1, "item amount as integer", False, 1))
            if item_name in items:
                game.inventory.append(item_name, item_amount)
            else:
                raise KeyError(f"There is no item '{item_name}'")
        elif command == "save_as":
            file_name = self.get_argunent(args, 0, "file name")
            game.saves_manager.save(file_name)
        elif command == "spawn":
            entity_name = self.get_argunent(args, 0, "entity name")
            x = int(self.get_argunent(args, 1, "x as integer", False, game.player.pos.x))
            y = int(self.get_argunent(args, 2, "y as integer", False, game.player.pos.y))
            game.spawn(entity_name, Vector(x, y))
            game.entity_manager.update_entities_by_chunks()
        elif command == "use_collisions":
            value = {"true": True, "false": False}[self.get_argunent(args, 0, "value as boolean")]
            game.player.use_collisions = value
        elif command == "set_tile":
            tile_id = int(self.get_argunent(args, 0, "tile id as integer"))
            x = int(self.get_argunent(args, 1, "tile x as integer", False, game.player.pos.x // TILE_SIZE.x))
            y = int(self.get_argunent(args, 2, "tile y as integer", False, game.player.pos.y // TILE_SIZE.y))
            game.world.data[x][y] = tile_id
            game.world.update_chunks()
        elif command == "set":
            var_name = self.get_argunent(args, 0, "variable_name")
            new_value = self.get_argunent(args, 1, "value")
            self.variables[var_name] = new_value
        elif command == "log":
            var_name = self.get_argunent(args, 0, "variable_name")
            self.parent.print(f"{var_name}: {self.variables[var_name]}")

        else:

            if running_script:
                raise SyntaxError(f"There is no command '{command}'")
            else:
                raise SyntaxError(f"There is no command '{command}'")

    def execute_input_command(self, command, args):

        game = self.parent.parent
        if command == "help":
            theme = self.get_argunent(args, 0, "theme", False, "main")
            if theme == "main":
                with open("assets/terminal_help.txt", "r") as f:
                    self.parent.print(f.read())
            elif theme == "tiles":
                for tile_id, tile in tiles.items():
                    self.parent.print(f"{tile_id} - {tile.name}")
            elif theme == "entities":
                for entity_class in ENTITIES:
                    self.parent.print(entity_class.__name__)
            elif theme == "items":
                for item_name, item_data in items.items():
                    self.parent.print(f"{item_name} - {item_data.__class__.__name__}")
            elif theme == "scripts":
                with open("assets/terminal_help2.txt", "r") as f:
                    self.parent.print(f.read())
        elif command == "list":
            theme = self.get_argunent(args, 0, "theme", False, "program")
            if theme == "program":
                for string_id, (command_name, command_args) in sorted(self.parent.current_program.items(), key=lambda e: e[0]):
                    string = f"{string_id}  {command_name} "
                    for arg in command_args:
                        string += arg + " "
                    self.parent.print(string)
            elif theme == "files":
                for file_name in os.listdir(os.path.join(APPDATA_FOLDER_PATH, PROGRAMS_FOLDER)):
                    self.parent.print(file_name.split('.')[0])
        elif command == "run":
            self.run(game)
        elif command == "save":
            file_name = self.get_argunent(args, 0, "file_name")
            with open(os.path.join(APPDATA_FOLDER_PATH, PROGRAMS_FOLDER, file_name+".json"), "w+") as f:
                json.dump(self.parent.current_program, f)
        elif command == "load":
            file_name = self.get_argunent(args, 0, "file_name")
            with open(os.path.join(APPDATA_FOLDER_PATH, PROGRAMS_FOLDER, file_name+".json"), "r") as f:
                self.parent.current_program = json.load(f)
        else:
            self.execute_command(game, command, args)

    def run(self, game):

        self.reset()
        for string_id, (command_name, command_args) in sorted(self.parent.current_program.items(), key=lambda e : e[0]):
            self.execute_command(game, command_name, command_args, True)
        self.reset()
