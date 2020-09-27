import numpy as np

class BattlesnakeGame:
    
    FOOD_INDEX = 0
    YOU_INDEX = 1
    SNAKES_INDEX = 2
    
    def __init__(self, game_state):
        """
        Helper function to keep information about a game
        This is necessary because for layered representation
        We need to know how many snakes there were
        and which channels they were assigned to
        """
        
        self.game_id = game_state['game']['id']+game_state['you']['id']
        self.board_h = game_state['board']['height']
        self.board_w = game_state['board']['width']
        self.num_snakes = len(game_state['board']['snakes'])
        self.snake_to_ids = {game_state['you']['id']: BattlesnakeGame.YOU_INDEX}
        # Get the snake IDs
        k = 2
        for snake in game_state['board']['snakes']:
            if snake['id'] in self.snake_to_ids:
                continue
            self.snake_to_ids[snake['id']] = k
            k += 1
        

class ObservationToStateConverter:
    """
    Convert Battlesnake observation to the states that 
    were trained with
    
    """
    def __init__(self, style="layered", border_option="1"):
        self.games = {}
        self.style = style
        self.border_option = border_option

    def _convert_to_state(self, game_state, game):
        
        # Get the border size
        if self.border_option == "1":
            border_size = 1
        elif self.border_option == "None":
            border_size = 0
        elif self.border_option == "max":
            border_size = int((21 - game.board_h)/2)
        else:
            raise ValueError("Unkown border_option {}".format(self.border_option))
            
        # Get the style of state
        if self.style == 'layered':
            channels = game.num_snakes+1
        elif self.style == 'one_versus_all':
            channels = 3
        else:
            raise ValueError("Unkown style {}".format(self.style))
        
        # Create the base state matrix
        state = np.zeros((game.board_h + 2*border_size, game.board_w + 2*border_size, channels))
        
        # Add the borders
        if self.border_option in ["1", "max"]:
            state = state - 1
            state[border_size:border_size+game.board_h, border_size:border_size+game.board_w,:] = 0
        
        # Put the food on the board
        for coord in game_state['board']['food']:
            state[coord['y']+border_size, coord['x']+border_size, BattlesnakeGame.FOOD_INDEX] = 1
            
        # Add the snakes
        for snake in game_state['board']['snakes']:
            first = True
            
            # Set the snakes channels to 2 if one vs all
            if self.style == 'one_versus_all':
                snake_channel = BattlesnakeGame.SNAKES_INDEX if game.snake_to_ids[snake['id']] != BattlesnakeGame.YOU_INDEX else BattlesnakeGame.YOU_INDEX
            else:
                snake_channel = game.snake_to_ids[snake['id']]
            for coord in snake['body']:
                if state[coord['y']+border_size, coord['x']+border_size, snake_channel] == 0:
                    state[coord['y']+border_size, coord['x']+border_size, snake_channel] = 5 if first else 1
                    first = False
        
        return state
        
    def get_game_state(self, game_state):
        game_id = game_state['game']['id']+game_state['you']['id']
        if game_id not in self.games:
            self.games[game_id]= {'game':BattlesnakeGame(game_state), 'previous_state':None}
            
        game_record = self.games[game_id]
        current_state = self._convert_to_state(game_state, game_record['game'])
        
        if game_record['previous_state'] is None:
            game_record['previous_state'] = current_state
            previous_state = np.zeros(shape=current_state.shape)
            return current_state, previous_state
        
        previous_state = game_record['previous_state']
        game_record['previous_state'] = current_state
        return current_state, previous_state
