import os
import random

import cherrypy

from environment import *
from astar import *


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when we register our Battlesnake on play.battlesnake.com
        return {
            "apiversion": "1",
            "author": "finleymcilwaine",
            "color": "#000000",
            "head": "silly",
            "tail": "fat-rattle",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called every time our snake is entered into a game.
        data = cherrypy.request.json

        print("STARTING NEW GAME")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # LGTB
        data = cherrypy.request.json
        env = Environment(data["board"])
        my_head = tuple(data["board"]["you"]["head"].values())
        close_food = env.get_closest_food(my_head)

        pq = PriorityQueue()
        enemy_path = pq.enemy_paths(my_head, close_food, env)
        env.add_walls(enemy_path)

        if len(env.board["food"]) > 1:
            other_foods = []
            for f in env.board["food"]:
                if tuple(f.values()) != close_food:
                    other_foods.append(tuple(f.values()))
            random_food = random.choice(other_foods)

            between_foods_path = pq.a_star_search(close_food, random_food, env)
            env.add_walls(between_foods_path)

        start = my_head
        goal = self.change_targets(nearest_food, all_food_locations, snakes, head, length, height, width, snake_locations)

        best_path = pq.a_star_search(start, goal, env)

        move = convert_xy_to_direction(best_path)

        print(f"MOVE: {move}")
        return {
            "move": move,
            "shout": "YOU HAVE NO CHANCE, SURRENDER!"
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"

def convert_xy_to_direction(best_path):
        print(f"Best path: {best_path}")
        (x1, y1) = best_path[0]
        print(f"Best path [0]: {best_path[0]}")
        (x2, y2) = best_path[1]
        print(f"Best path [1]: {best_path[1]}")
        if x1 - x2 > 0:
          return "left"
        if x1 - x2 < 0:
          return "right"
        if y1 - y2 < 0:
          return "up"
        if y1 - y2 > 0:
          return "down"

if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")), }
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
