import random

class Environment:
    def __init__(self, board, me):
        self.me = me
        self.board = board
        self.walls = []

    # Returns tuples of snake locations
    def get_snake_locations(self):
        snake_locs = []
        # Snakes including ur boi
        for s in self.board["snakes"]:
            for b in s["body"]:
                snake_locs.append(tuple(b.values()))
        return snake_locs

    # Distance from food given a location and a food index
    def get_distance_from_food_at_index(self, loc, i):
        (x, y) = loc
        if (i + 1 > len(self.board["food"])): return 100
        return abs(x - self.board["food"][i]["x"]) \
            + abs(y - self.board["food"][i]["y"])

    # Tuple of closest food location
    def get_closest_food(self, loc):
        closest_food_dist = 100000
        for i in range(len(self.board["food"])):
            dist = self.get_distance_from_food_at_index(loc, i)
            if(dist <= closest_food_dist):
                closest_food_dist = dist
                closest_food = tuple(self.board["food"][i].values())
        return closest_food


    # Is a location out of bounds
    def get_is_out_of_bounds(self, loc):
        (x, y) = loc
        return (x < 0 or y < 0 or x >= self.board["width"] or y >= self.board["height"])

    # All potential moves from a given location
    def get_potential_moves(self, loc):
        (x, y) = loc
        moves = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        no_collision = [m for m in moves if m not in (
            self.get_snake_locations() + self.walls)]
        potential_moves = [
            m for m in no_collision if not self.get_is_out_of_bounds(m)]
        return potential_moves

    def add_walls(self, w):
        self.walls.extend(w)

    def get_target(self):
        # My location
        my_head = tuple(self.me["head"].values())
        (my_head_x, my_head_y) = my_head
        my_length = self.me["length"]

        # Closest food
        (food_x, food_y) = self.get_closest_food(my_head)

        # Food distance
        my_food_distance = abs(my_head_x - food_x) + abs(my_head_y - food_y)
        my_id = self.me["id"]

        snakes = self.board["snakes"]
        longest_enemy = snakes[0]["length"]
        enemy_tail = snakes[0]["body"][-1]
        enemy_head = tuple(snakes[0]["head"].values())

        # Enemy food distance
        (enemy_head_x, enemy_head_y) = enemy_head
        enemy_food_distance = abs(enemy_head_x - food_x) + abs(enemy_head_y - food_y)

        # Each snake
        for snake in snakes:
            # If not me
            if snake["id"] != my_id:
                (snake_head_x, snake_head_y) = tuple(snake["head"].values())
                # Track longest enemy
                if snake["length"] >= longest_enemy:
                    longest_enemy = snake["length"]
                # Distance to food
                snake_food_distance = abs(snake_head_x - food_x) + abs(snake_head_y - food_y)
                # If their closer than me to the food, track them
                if my_food_distance < snake_food_distance:
                    enemy_head = tuple(snake["head"].values())
                    enemy_food_distance = snake_food_distance
                    enemy_tail = tuple(snake["body"][-1].values())


        current_target = (food_x, food_y)
        nearest_food = current_target
        others = []
        # If I'm longer than any enemy
        if my_length > longest_enemy:
            # If an enemy is closer to my target food, go somewhere else, or just target their head
            if my_food_distance >= enemy_food_distance:
                if len(self.board["food"]) == 1:
                    current_target = enemy_head
                else:
                    # target random food if there is one
                    for other in self.board["food"]:
                        if tuple(other.values()) != nearest_food:
                            selected = tuple(other.values())
                            others.append(selected)
                    current_target = random.choice(others)
            # If I'm closer to target food
            else:
                current_target = nearest_food
        # If I'm not longer than any enemy
        else:
            current_target = nearest_food
            
        print(f"Current target: {current_target}")
        return current_target
