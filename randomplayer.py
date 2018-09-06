from moveonlyplayer import MoveOnlyPlayer

import random

class RandomPlayer(MoveOnlyPlayer):

    def get_move(self, player_number, board, previous_capture_position):
        plays = board.get_all_plays_for(player_number, previous_capture_position)
        return random.choice(plays)
        