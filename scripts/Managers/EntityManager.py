from scripts.constants import *
from scripts.Entities.Natural.Tree import Tree
from collections import defaultdict, deque
from scripts.Entities.ABC.ElectricNode import ElectricNode
from scripts.Entities.ABC.Building import Building
from scripts.Entities.Buildings.Workbench import Workbench


class EntityManager:

    def __init__(self, parent):

        self.parent = parent
        self.chunks = []

    def update_entities_by_chunks(self):

        # self.parent.entities_by_chunks = [[list() for _ in range(MAP_SIZE.y)] for _ in range(MAP_SIZE.x)]

        # entities = self.parent.trees + self.parent.ores + self.parent.buildings + self.parent.pebbles + \
        #            self.parent.bushes + self.parent.items

        # for entity in set(entities):
        #     chunk_x = (int(entity.pos.x) // TILE_SIZE.x) // CHUNK_SIZE.x
        #     chunk_y = (int(entity.pos.y) // TILE_SIZE.y) // CHUNK_SIZE.y
        #     self.parent.entities_by_chunks[chunk_x][chunk_y].append(entity)

        parent = self.parent
        entities = parent.trees + parent.ores + parent.buildings + parent.pebbles + parent.bushes + parent.items

        chunk_size_x = CHUNK_SIZE.x * TILE_SIZE.x
        chunk_size_y = CHUNK_SIZE.y * TILE_SIZE.y

        parent.entities_by_chunks = [[list() for _ in range(MAP_SIZE.y)] for _ in range(MAP_SIZE.x)]
        parent.forced_entities = list()

        for entity in set(entities):

            chunk_x = int(entity.pos.x) // chunk_size_x
            chunk_y = int(entity.pos.y) // chunk_size_y
            parent.entities_by_chunks[chunk_x][chunk_y].append(entity)

            if getattr(entity, 'forced_updating', False):
                self.parent.forced_entities.append(entity)

    def delete_entity_by_code(self, code):

        entities = [self.parent.trees, self.parent.ores, self.parent.buildings, self.parent.pebbles, self.parent.bushes,
                    self.parent.items, self.parent.particles + self.parent.wires]

        for lst in entities:
            for entity_id, entity in enumerate(lst):
                if entity.code == code:
                    lst.pop(entity_id)
                    break

    def delete_particle(self, code):

        for n, particle in enumerate(self.parent.particles):
            if particle.code == code:
                self.parent.particles.pop(n)
                break

    def delete_wire_by_code(self, code):

        for n, wire in enumerate(self.parent.wires):
            if wire.code == code:
                self.parent.wires.pop(n)
                break

    def get_building_by_code(self, code, only_electric_node: bool = False):

        if only_electric_node:
            lst = sorted(self.parent.buildings, key=lambda e: isinstance(e, ElectricNode))
        else:
            lst = self.parent.buildings
        for entity in lst:
            if entity.code == code:
                return entity
        return None

    def get_building_connections_amount(self, code) -> int:

        result = 0
        # print("searching", code)
        for wire in self.parent.wires:
            # print(wire.a, ":", wire.b)
            if wire.a == code or wire.b == code:
                result += 1
        # print(result)
        return result

    def get_wire_by_connections(self, code_a, code_b):

        for wire in self.parent.wires:
            if (wire.a == code_a and wire.b == code_b) or (wire.a == code_b and wire.b == code_a):
                return wire
        return None

    def update_active_chunks(self):

        self.parent.entities = list()
        self.chunks = list()

        entities = self.parent.trees + self.parent.ores + self.parent.buildings + self.parent.pebbles + self.parent.bushes + self.parent.items + self.parent.particles

        window_rect = pg.Rect(0, 0, RESOLUTION.x, RESOLUTION.y)

        chunk_size_x = CHUNK_SIZE.x * TILE_SIZE.x
        chunk_size_y = CHUNK_SIZE.y * TILE_SIZE.y

        for chunk_x in range(0, MAP_SIZE.x):
            for chunk_y in range(0, MAP_SIZE.y):

                chunk_pos = Vector(chunk_x, chunk_y)
                global_chunk_pos = chunk_pos * CHUNK_SIZE * TILE_SIZE + self.parent.offset

                chunk_rect = pg.Rect((global_chunk_pos.x, global_chunk_pos.y, chunk_size_x, chunk_size_y))

                rect_in_window = window_rect.colliderect(chunk_rect) or window_rect.contains(chunk_rect)

                if rect_in_window: self.chunks.append(chunk_pos)

        for chunk in self.chunks:
            try:
                self.parent.entities += self.parent.entities_by_chunks[chunk.x][chunk.y]
            except Exception as e:
                print(e)

    def update_entities(self):

        self.parent.entities_to_draw = list()

        self.parent.player.update()

        for entity in set(self.parent.entities + self.parent.forced_entities) :

            if entity.tobeddeleted:
                self.delete_entity_by_code(entity.code)
                continue

            entity.update()

            if entity.do_draw:
                self.parent.entities_to_draw.append(entity)

        self.parent.entities_to_draw.append(self.parent.player)
        self.parent.entities_to_draw.sort(key=lambda e: e.pos.y)

        for particle in set(self.parent.particles):
            particle.update()
            if particle.tobeddeleted:
                self.delete_particle(particle.code)
                continue
            self.parent.entities_to_draw.append(particle)

        for entity in set(self.parent.wires):
            if entity.tobedeleted:
                self.delete_wire_by_code(entity.code)
                continue
            entity.update()

    def calculate_subnetworks(self):

        all_ids = {obj.code for obj in self.parent.buildings if isinstance(obj, ElectricNode)}

        graph = defaultdict(list)
        for wire in self.parent.wires:
            graph[wire.a].append(wire.b)
            graph[wire.b].append(wire.a)

        visited = set()
        subnetworks = []

        def dfs(node, current_subnet):
            stack = [node]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    current_subnet.append(current)
                    stack.extend(graph[current])

        for node in graph.keys():
            if node not in visited:
                current_subnet = []
                dfs(node, current_subnet)
                subnetworks.append(current_subnet)

        connected_ids = {node for subnet in subnetworks for node in subnet}
        isolated_ids = all_ids - connected_ids
        for isolated_id in isolated_ids:
            subnetworks.append([isolated_id])

        self.parent.subnetworks = subnetworks

    def calculate_subnetworks_balances_and_distribute(self):

        for subnetwork in self.parent.subnetworks:

            balance = sum(self.get_building_by_code(obj_id, True).network_weight for obj_id in subnetwork)
            consumers = [obj_id for obj_id in subnetwork if self.get_building_by_code(obj_id, True).network_weight < 0]
            total_demand = -sum(self.get_building_by_code(obj_id, True).network_weight for obj_id in consumers)
            generators = [obj_id for obj_id in subnetwork if self.get_building_by_code(obj_id, True).network_weight > 0]
            total_generation = sum(self.get_building_by_code(obj_id, True).network_weight for obj_id in generators)
            info_needies = [obj_id for obj_id in subnetwork if self.get_building_by_code(obj_id, True).requires_network_info]

            if balance >= 0:
                for obj_id in consumers:
                    building = self.get_building_by_code(obj_id, True)
                    building.distribute(-building.network_weight)
            else:
                available_energy = balance + total_demand
                for obj_id in consumers:
                    building = self.get_building_by_code(obj_id, True)
                    consumer_demand = -building.network_weight
                    share = consumer_demand / total_demand
                    distributed_energy = int(available_energy * share)
                    building.distribute(distributed_energy)

            subnetwork_info = \
                {
                    "balance": balance,

                    "consumers": consumers,
                    "total_demand": total_demand,

                    "generators": generators,
                    "total_generation": total_generation
                }

            for obj_id in info_needies:
                building = self.get_building_by_code(obj_id, True)
                building.distribute_network_info(subnetwork_info)
