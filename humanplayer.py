from moveonlyplayer import MoveOnlyPlayer

class HumanPlayer(MoveOnlyPlayer):

    def __init__(self):
        super().__init__()

    def get_move(self, player_number, board, previous_capture_position):
        raw = input('')
        if len(raw) == 0:
            return '', ''
        string = '{:5}'.format(raw.upper())
        from_move = string[0:2]
        to_move = string[3:5]
        return from_move, to_move
        