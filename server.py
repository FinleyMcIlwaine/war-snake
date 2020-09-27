import os
import random

import cherrypy
import numpy as np

from convert_utils import ObservationToStateConverter


converter = ObservationToStateConverter(style='one_versus_all', border_option="1")

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
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
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        current_state, previous_state = converter.get_game_state(data)
    
        # Get the list of possible directions
        i,j = np.unravel_index(np.argmax(current_state[:,:,1], axis=None), current_state[:,:,1].shape)
        snakes = current_state[:,:,1:].sum(axis=2)
        food = current_state[:,:,0]
        possible = []
        food_locations = []
        if snakes[i+1,j] == 0:
            possible.append('down')
        if snakes[i-1,j] == 0:
            possible.append('up')
        if snakes[i,j+1] == 0:
            possible.append('right')
        if snakes[i,j-1] == 0:
            possible.append('left')
        
        # Food locations
        if food[i+1, j] == 1:
            food_locations.append('down')
        if food[i-1,j] == 1:
            food_locations.append('up')
        if food[i,j+1] == 1:
            food_locations.append('right')
        if food[i,j-1] == 1:
            food_locations.append('left')

        move = random.choice(possible)

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


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
