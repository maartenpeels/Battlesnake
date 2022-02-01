import logging
from collections import defaultdict


log = logging.getLogger("battlesnake")
log.setLevel(logging.INFO)


class Bot:
    possible_directions = None
    walls = defaultdict(bool)
    foods = defaultdict(bool)
    length = 0

    head = None
    body = []
    tail = None

    def __init__(self, width, height):
        self.width = width
        self.height = height
        log.info('Initialized map of size %x%s', width, height)

    def is_out_of_bounds(self, xy):
        x, y = xy
        oob = not (0 <= x < self.width and 0 <= y < self.height)
        # log.debug('Checking if %s is out of bounds, result: %s', xy, oob)
        return oob

    def is_colliding_with_wall(self, xy):
        collided = self.walls[xy]
        # log.debug('Checking if %s is colliding with wall, result: %s', xy, collided)
        return collided

    def flood_fill(self, xy):
        visited = set()
        queue = set()
        queue.add(xy)
        while len(queue) > 0:
            xy = queue.pop()

            for dir, xy2 in self.get_possible_directions_at_loc(xy):
                if xy2 not in visited and xy2 not in queue:
                    visited.add(xy)
                    queue.add(xy2)
        area_size = len(visited)
        log.debug('Flood fill area size of %s: %s', xy, area_size)
        return area_size

    def is_area_big_enough(self, xy):
        area_size = self.flood_fill(xy)
        amount_of_walls = len([x for x in list(self.walls.values()) if x])
        total_empty_cells = (self.width * self.height) - amount_of_walls
        big_enough = (area_size / total_empty_cells) > 0.5 or area_size > self.length + 5
        log.debug('Checking if area size of %s is big enough, result: %s', xy, big_enough)
        return big_enough

    def get_possible_directions_at_loc(self, xy):
        x, y = xy
        directions = [
            ("up", (x, y + 1)),
            ("down", (x, y - 1)),
            ("left", (x - 1, y)),
            ("right", (x + 1, y))
        ]
        for dir, xy in directions.copy():
            if self.is_out_of_bounds(xy) or self.is_colliding_with_wall(xy):
                directions.remove((dir, xy))
        return directions

    def calculate_possible_directions(self):
        for dir, xy in self.possible_directions.copy():
            if (self.is_out_of_bounds(xy) or self.is_colliding_with_wall(xy) or not self.is_area_big_enough(xy)) and len(self.possible_directions) > 1:
                self.possible_directions.remove((dir, xy))
        log.debug('Calculated possible directions: %s', self.possible_directions)

    def get_distance_between_points(self, xy1, xy2):
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

    def get_new_location(self, xy, direction):
        if direction == "up":
            return xy[0], xy[1] + 1
        elif direction == "down":
            return xy[0], xy[1] - 1
        elif direction == "left":
            return xy[0] - 1, xy[1]
        elif direction == "right":
            return xy[0] + 1, xy[1]

    def get_direction_to_point(self, xy):
        best_dir = None
        best_dist = 100_000
        for dir, next_loc in self.possible_directions:
            dist = self.get_distance_between_points(next_loc, xy)
            if dist < best_dist:
                best_dir = dir
                best_dist = dist
        return best_dir

    def find_best_food(self):
        #  TODO find closest food to head which we can reach before the others
        positions = list(self.foods.keys())
        positions.sort(key=lambda x: self.get_distance_between_points(x, self.head))
        return positions[0]

    def get_food_move(self,):
        target = self.find_best_food()
        move = self.get_direction_to_point(target)
        return move

    def move(self, data):
        # Reset before every move
        self.walls = defaultdict(bool)
        self.foods = defaultdict(bool)

        log.debug(data)
        me = data['you']
        foods = data["board"]["food"]
        snakes = data["board"]["snakes"]

        x, y = (me['head']['x'], me['head']['y'])
        self.possible_directions = [
            ("up", (x, y + 1)),
            ("down", (x, y - 1)),
            ("left", (x - 1, y)),
            ("right", (x + 1, y))
        ]

        self.length = me["length"]
        self.body = [(x['x'], x['y']) for x in me['body']]
        self.head = self.body[0]
        self.tail = self.body[-1]

        for snake in snakes:
            coords = snake["body"]
            for index, loc in enumerate(coords):
                self.walls[(loc["x"], loc["y"])] = True

        for loc in foods:
            self.foods[(loc["x"], loc["y"])] = True

        log.debug('Walls: %s', [(xy, is_wall) for xy, is_wall in list(self.walls.items()) if is_wall])
        log.debug('Foods: %s', self.foods)
        log.debug('Me: %s', me['body'])

        self.calculate_possible_directions()

        health = me['health']
        if health < 40:
            move = self.get_food_move()
        else:
            move = self.get_direction_to_point(self.tail)

        log.debug('Move: %s', move)
        return move
