from player import Player, ni

class MoveOnlyPlayer(Player):

    def get_move(self, player_number, board, previous_capture_position):
        ni()

    def ok_move(self, player_number, board, previous_capture_position, from_move, to_move):
        pass

    def bad_move(self, player_number, board, previous_capture_position, from_move, to_move):
        pass
        
    def start(self):
        pass

    def end(self):
        pass

    def win(self):
        pass

    def lose(self):
        pass

    def draw(self):
        pass
        