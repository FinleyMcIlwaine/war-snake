import heapq
import os
import cherrypy


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self, start, goal, env):
        # Initialize
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        came_from[start] = None
        distance_from_start = {}
        distance_from_start[start] = 0
        explored = []

        print("A*: " + f"goal is {goal} from {start}")

        # A* bb
        while not frontier.empty():
            current_location = frontier.get()
            explored.append(current_location)
            if current_location == goal:
                break
            print("A*: " + f"potential moves: {env.get_potential_moves(current_location)} from {current_location}")
            for next in env.get_potential_moves(current_location):
                new_cost = distance_from_start[current_location] + \
                    self.heuristic(current_location, next)
                # If we haven't been here or we found a cheaper explored here
                if next not in distance_from_start or new_cost < distance_from_start[next]:
                    # Add to frontier with priority
                    distance_from_start[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    print("A*: " + f"Found cell {next} with priority {priority}")
                    frontier.put(next, priority)
                    came_from[next] = current_location
        path = []
        loc = current_location
        while (loc != start):
            path.insert(0, loc)
            loc = came_from[loc]
        path.insert(0, start)
        print("A*: FOUND PATH: " + f"{path}")
        return path

    # Returns the "best" explored of the enemy closest to my goal
    def enemy_path(self, start, goal, env):
        (goal_x, goal_y) = goal
        (my_x, my_y) = start
        my_distance = abs(my_x - goal_x) + abs(my_y - goal_y)

        print("ENEMY PATH: " + f"goal is {goal}, my head is {start}, distance {my_distance} to food.")
        snakes = env.board["snakes"]
        enemy_head = tuple(snakes[0]["head"].values())
        (enemy_x, enemy_y) = enemy_head
        enemy_food_distance = 0
        closest_head_dist = 100
        closest_head = (100,100)

        for snake in snakes:
            if snake["id"] != env.me["id"]:
                (snake_head_x, snake_head_y) = tuple(snake["head"].values())
                snake_food_distance = abs(
                    snake_head_x - goal_x) + abs(snake_head_y - goal_y)
                print("ENEMY PATH: " + f"Enemy snake goal is {goal}, enemy head is {(snake_head_x, snake_head_y)}, distance {snake_food_distance} to food.")
                if snake_food_distance <= my_distance:
                    enemy_head = tuple(snake["head"].values())
                    enemy_food_distance = snake_food_distance
                
                head_dist = abs(
                    snake_head_x - my_x) + abs(snake_head_y - my_y)
                if (head_dist < closest_head_dist):
                    closest_head_dist = head_dist
                    closest_head = (snake_head_x, snake_head_y)

        print(f"ENEMY PATH: " + f"enemy closest to food is at {enemy_head}")
        if (enemy_head == start): 
            enemy_path = []
        else:
            enemy_start, enemy_goal = enemy_head, goal
            enemy_path = self.a_star_search(enemy_start, enemy_goal, env)
        if (closest_head_dist < 3):
            enemy_path.extend(env.get_potential_moves(closest_head))
        print("ENEMY_PATH: " + f"enemy path to food is {enemy_path}")
        return enemy_path
