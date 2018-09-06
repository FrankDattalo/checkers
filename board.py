import os

class Board(object):

    VALID_POSITIONS = (
        'A1', 'C1', 'E1', 'G1',
        'B2', 'D2', 'F2', 'H2',
        'A3', 'C3', 'E3', 'G3',
        'B4', 'D4', 'F4', 'H4',
        'A5', 'C5', 'E5', 'G5',
        'B6', 'D6', 'F6', 'H6',
        'A7', 'C7', 'E7', 'G7',
        'B8', 'D8', 'F8', 'H8'
    )

    ONE_SPACE_SET = {
        'A1': ('B2',),
        'A3': ('B2','B4',),
        'A5': ('B4','B6',),
        'A7': ('B6','B8',),
        'B2': ('A1','A3','C1','C3',),
        'B4': ('A3','A5','C3','C5',),
        'B6': ('A5','A7','C5','C7',),
        'B8': ('A7','C7',),
        'C1': ('B2','D2',),
        'C3': ('B2','B4','D2','D4',),
        'C5': ('B4','B6','D4','D6',),
        'C7': ('B6','B8','D6','D8',),
        'D2': ('C1','C3','E1','E3',),
        'D4': ('C3','C5','E3','E5',),
        'D6': ('C5','C7','E5','E7',),
        'D8': ('C7','E7',),
        'E1': ('D2','F2',),
        'E3': ('D2','D4','F2','F4',),
        'E5': ('D4','D6','F4','F6',),
        'E7': ('D6','D8','F6','F8',),
        'F2': ('E1','E3','G1','G3',),
        'F4': ('E3','E5','G3','G5',),
        'F6': ('E5','E7','G5','G7',),
        'F8': ('E7','G7',),
        'G1': ('F2','H2',),
        'G3': ('F2','F4','H2','H4',),
        'G5': ('F4','F6','H4','H6',),
        'G7': ('F6','F8','H6','H8',),
        'H2': ('G1','G3',),
        'H4': ('G3','G5',),
        'H6': ('G5','G7',),
        'H8': ('G7',)
    }

    TWO_SPACE_SET = {
        'A1': ('C3',),
        'A3': ('C5','C1',),
        'A5': ('C7','C3',),
        'A7': ('C5',),
        'B2': ('D4',),
        'B4': ('D6','D2',),
        'B6': ('D8','D4',),
        'B8': ('D6',),
        'C1': ('A3','E3',),
        'C3': ('A5','E5','A1','E1',),
        'C5': ('A7','E7','A3','E3',),
        'C7': ('A5','E5',),
        'D2': ('B4','F4',),
        'D4': ('B6','F6','B2','F2',),
        'D6': ('B8','F8','B4','F4',),
        'D8': ('B6','F6',),
        'E1': ('C3','G3',),
        'E3': ('C5','G5','C1','G1',),
        'E5': ('C7','G7','C3','G3',),
        'E7': ('C5','G5',),
        'F2': ('D4','H4',),
        'F4': ('D6','H6','D2','H2',),
        'F6': ('D8','H8','D4','H4',),
        'F8': ('D6','H6',),
        'G1': ('E3',),
        'G3': ('E5','E1',),
        'G5': ('E7','E3',),
        'G7': ('E5',),
        'H2': ('F4',),
        'H4': ('F6','F2',),
        'H6': ('F8','F4',),
        'H8': ('F6',)
    }

    MIDDLE_SET = {
        'A1C3': 'B2',
        'A3C1': 'B2',
        'A3C5': 'B4',
        'A5C3': 'B4',
        'A5C7': 'B6',
        'A7C5': 'B6',
        'B2D4': 'C3',
        'B4D2': 'C3',
        'B4D6': 'C5',
        'B6D4': 'C5',
        'B6D8': 'C7',
        'B8D6': 'C7',
        'C1A3': 'B2',
        'C1E3': 'D2',
        'C3A1': 'B2',
        'C3A5': 'B4',
        'C3E1': 'D2',
        'C3E5': 'D4',
        'C5A3': 'B4',
        'C5A7': 'B6',
        'C5E3': 'D4',
        'C5E7': 'D6',
        'C7A5': 'B6',
        'C7E5': 'D6',
        'D2B4': 'C3',
        'D2F4': 'E3',
        'D4B2': 'C3',
        'D4B6': 'C5',
        'D4F2': 'E3',
        'D4F6': 'E5',
        'D6B4': 'C5',
        'D6B8': 'C7',
        'D6F4': 'E5',
        'D6F8': 'E7',
        'D8B6': 'C7',
        'D8F6': 'E7',
        'E1C3': 'D2',
        'E1G3': 'F2',
        'E3C1': 'D2',
        'E3C5': 'D4',
        'E3G1': 'F2',
        'E3G5': 'F4',
        'E5C3': 'D4',
        'E5C7': 'D6',
        'E5G3': 'F4',
        'E5G7': 'F6',
        'E7C5': 'D6',
        'E7G5': 'F6',
        'F2D4': 'E3',
        'F2H4': 'G3',
        'F4D2': 'E3',
        'F4D6': 'E5',
        'F4H2': 'G3',
        'F4H6': 'G5',
        'F6D4': 'E5',
        'F6D8': 'E7',
        'F6H4': 'G5',
        'F6H8': 'G7',
        'F8D6': 'E7',
        'F8H6': 'G7',
        'G1E3': 'F2',
        'G3E1': 'F2',
        'G3E5': 'F4',
        'G5E3': 'F4',
        'G5E7': 'F6',
        'G7E5': 'F6',
        'H2F4': 'G3',
        'H4F2': 'G3',
        'H4F6': 'G5',
        'H6F4': 'G5',
        'H6F8': 'G7',
        'H8F6': 'G7'
    }

    ABSOLUTE_TO_RELATIVE = {
        'H8': 'A1',
        'H6': 'A3',
        'H4': 'A5',
        'H2': 'A7',
        'G7': 'B2',
        'G5': 'B4',
        'G3': 'B6',
        'G1': 'B8',
        'F8': 'C1',
        'F6': 'C3',
        'F4': 'C5',
        'F2': 'C7',
        'E7': 'D2',
        'E5': 'D4',
        'E3': 'D6',
        'E1': 'D8',
        'D8': 'E1',
        'D6': 'E3',
        'D4': 'E5',
        'D2': 'E7',
        'C7': 'F2',
        'C5': 'F4',
        'C3': 'F6',
        'C1': 'F8',
        'B8': 'G1',
        'B6': 'G3',
        'B4': 'G5',
        'B2': 'G7',
        'A7': 'H2',
        'A5': 'H4',
        'A3': 'H6',
        'A1': 'H8'
    }

    RELATIVE_TO_ABSOLUTE = {
        'A1': 'H8',
        'A3': 'H6',
        'A5': 'H4',
        'A7': 'H2',
        'B2': 'G7',
        'B4': 'G5',
        'B6': 'G3',
        'B8': 'G1',
        'C1': 'F8',
        'C3': 'F6',
        'C5': 'F4',
        'C7': 'F2',
        'D2': 'E7',
        'D4': 'E5',
        'D6': 'E3',
        'D8': 'E1',
        'E1': 'D8',
        'E3': 'D6',
        'E5': 'D4',
        'E7': 'D2',
        'F2': 'C7',
        'F4': 'C5',
        'F6': 'C3',
        'F8': 'C1',
        'G1': 'B8',
        'G3': 'B6',
        'G5': 'B4',
        'G7': 'B2',
        'H2': 'A7',
        'H4': 'A5',
        'H6': 'A3',
        'H8': 'A1'
    }

    POSSIBLE_PLAYS = (
        ('A1', 'B2'),
        ('A1', 'C3'),
        ('A3', 'B2'),
        ('A3', 'B4'),
        ('A3', 'C5'),
        ('A3', 'C1'),
        ('A5', 'B4'),
        ('A5', 'B6'),
        ('A5', 'C7'),
        ('A5', 'C3'),
        ('A7', 'B6'),
        ('A7', 'B8'),
        ('A7', 'C5'),
        ('B2', 'A1'),
        ('B2', 'A3'),
        ('B2', 'C1'),
        ('B2', 'C3'),
        ('B2', 'D4'),
        ('B4', 'A3'),
        ('B4', 'A5'),
        ('B4', 'C3'),
        ('B4', 'C5'),
        ('B4', 'D6'),
        ('B4', 'D2'),
        ('B6', 'A5'),
        ('B6', 'A7'),
        ('B6', 'C5'),
        ('B6', 'C7'),
        ('B6', 'D8'),
        ('B6', 'D4'),
        ('B8', 'A7'),
        ('B8', 'C7'),
        ('B8', 'D6'),
        ('C1', 'B2'),
        ('C1', 'D2'),
        ('C1', 'A3'),
        ('C1', 'E3'),
        ('C3', 'B2'),
        ('C3', 'B4'),
        ('C3', 'D2'),
        ('C3', 'D4'),
        ('C3', 'A5'),
        ('C3', 'E5'),
        ('C3', 'A1'),
        ('C3', 'E1'),
        ('C5', 'B4'),
        ('C5', 'B6'),
        ('C5', 'D4'),
        ('C5', 'D6'),
        ('C5', 'A7'),
        ('C5', 'E7'),
        ('C5', 'A3'),
        ('C5', 'E3'),
        ('C7', 'B6'),
        ('C7', 'B8'),
        ('C7', 'D6'),
        ('C7', 'D8'),
        ('C7', 'A5'),
        ('C7', 'E5'),
        ('D2', 'C1'),
        ('D2', 'C3'),
        ('D2', 'E1'),
        ('D2', 'E3'),
        ('D2', 'B4'),
        ('D2', 'F4'),
        ('D4', 'C3'),
        ('D4', 'C5'),
        ('D4', 'E3'),
        ('D4', 'E5'),
        ('D4', 'B6'),
        ('D4', 'F6'),
        ('D4', 'B2'),
        ('D4', 'F2'),
        ('D6', 'C5'),
        ('D6', 'C7'),
        ('D6', 'E5'),
        ('D6', 'E7'),
        ('D6', 'B8'),
        ('D6', 'F8'),
        ('D6', 'B4'),
        ('D6', 'F4'),
        ('D8', 'C7'),
        ('D8', 'E7'),
        ('D8', 'B6'),
        ('D8', 'F6'),
        ('E1', 'D2'),
        ('E1', 'F2'),
        ('E1', 'C3'),
        ('E1', 'G3'),
        ('E3', 'D2'),
        ('E3', 'D4'),
        ('E3', 'F2'),
        ('E3', 'F4'),
        ('E3', 'C5'),
        ('E3', 'G5'),
        ('E3', 'C1'),
        ('E3', 'G1'),
        ('E5', 'D4'),
        ('E5', 'D6'),
        ('E5', 'F4'),
        ('E5', 'F6'),
        ('E5', 'C7'),
        ('E5', 'G7'),
        ('E5', 'C3'),
        ('E5', 'G3'),
        ('E7', 'D6'),
        ('E7', 'D8'),
        ('E7', 'F6'),
        ('E7', 'F8'),
        ('E7', 'C5'),
        ('E7', 'G5'),
        ('F2', 'E1'),
        ('F2', 'E3'),
        ('F2', 'G1'),
        ('F2', 'G3'),
        ('F2', 'D4'),
        ('F2', 'H4'),
        ('F4', 'E3'),
        ('F4', 'E5'),
        ('F4', 'G3'),
        ('F4', 'G5'),
        ('F4', 'D6'),
        ('F4', 'H6'),
        ('F4', 'D2'),
        ('F4', 'H2'),
        ('F6', 'E5'),
        ('F6', 'E7'),
        ('F6', 'G5'),
        ('F6', 'G7'),
        ('F6', 'D8'),
        ('F6', 'H8'),
        ('F6', 'D4'),
        ('F6', 'H4'),
        ('F8', 'E7'),
        ('F8', 'G7'),
        ('F8', 'D6'),
        ('F8', 'H6'),
        ('G1', 'F2'),
        ('G1', 'H2'),
        ('G1', 'E3'),
        ('G3', 'F2'),
        ('G3', 'F4'),
        ('G3', 'H2'),
        ('G3', 'H4'),
        ('G3', 'E5'),
        ('G3', 'E1'),
        ('G5', 'F4'),
        ('G5', 'F6'),
        ('G5', 'H4'),
        ('G5', 'H6'),
        ('G5', 'E7'),
        ('G5', 'E3'),
        ('G7', 'F6'),
        ('G7', 'F8'),
        ('G7', 'H6'),
        ('G7', 'H8'),
        ('G7', 'E5'),
        ('H2', 'G1'),
        ('H2', 'G3'),
        ('H2', 'F4'),
        ('H4', 'G3'),
        ('H4', 'G5'),
        ('H4', 'F6'),
        ('H4', 'F2'),
        ('H6', 'G5'),
        ('H6', 'G7'),
        ('H6', 'F8'),
        ('H6', 'F4'),
        ('H8', 'G7'),
        ('H8', 'F6')
    )

    def __init__(self, 
            line_sep=os.linesep,
            player_1_name='Player',
            player_2_name='Player', 
            player_1_checker='x', 
            player_1_king='X',
            player_2_checker='o',
            player_2_king='O',
            blank_checker='-'):

        self._board = {
            'A1': 2,
            'C1': 2,
            'E1': 2,
            'G1': 2,

            'B2': 2,
            'D2': 2,
            'F2': 2,
            'H2': 2,

            'A3': 2,
            'C3': 2,
            'E3': 2,
            'G3': 2,
            
            'B4': 0,
            'D4': 0,
            'F4': 0,
            'H4': 0,
            
            'A5': 0,
            'C5': 0,
            'E5': 0,
            'G5': 0,

            'B6': 1,
            'D6': 1,
            'F6': 1,
            'H6': 1,

            'A7': 1,
            'C7': 1,
            'E7': 1,
            'G7': 1,

            'B8': 1,
            'D8': 1,
            'F8': 1,
            'H8': 1
        }

        self._line_sep = line_sep
        self._player_1_checker = player_1_checker
        self._player_2_checker = player_2_checker
        self._blank_checker = blank_checker
        self._player_1_king = player_1_king
        self._player_2_king = player_2_king
        self._player_1_name = player_1_name
        self._player_2_name = player_2_name
        self._player_1_pieces = 12
        self._player_2_pieces = 12


    @classmethod
    def is_valid_position(clazz, combined):
        return combined in Board.VALID_POSITIONS

    @classmethod
    def _assert_valid_position(clazz, combined):
        if not Board.is_valid_position(combined):
            raise Exception('Invalid position: {}'.format(
                combined))


    def player_1_pieces(self):
        return self._player_1_pieces


    def player_2_pieces(self):
        return self._player_2_pieces


    def jump_possible(self, from_move):
        Board._assert_valid_position(from_move)

        from_move_value = self._board[from_move]
        if from_move_value == 0:
            return False

        from_player = abs(from_move_value)
        from_is_king = from_move_value < 0

        TWO_SPACE_SET = Board.TWO_SPACE_SET[from_move]
        
        for to_move in TWO_SPACE_SET:
            to_move_value = self._board[to_move]
            
            if to_move_value != 0:
                continue
            
            if not self.middle_is_enemy(from_move, to_move, from_player):
                continue
            
            if from_is_king:
                return True
            
            if Board.proper_direction(from_move, to_move, from_player):
                return True
        
        return False


    def move(self, from_move, to_move):
        if not self.is_valid_move(from_move, to_move):
            raise Exception('Invalid Move Attempted')

        board = self._clone()
        capture = False
        player = abs(self.get(from_move))
        win = False

        if self.middle_is_enemy(from_move, to_move, player):
            capture = True
            if player == 1:
                board._player_2_pieces -= 1
                win = board._player_2_pieces <= 0
            else:
                board._player_1_pieces -= 1
                win = board._player_1_pieces <= 0
            
            middle = Board.MIDDLE_SET[from_move + to_move]
            board._set(middle, 0)

        from_value = self.get(from_move)

        board._set(from_move, 0)
        board._set(to_move, from_value)

        to_move_number = int(to_move[1])
        if (to_move_number == 8 and player == 2) or (
                to_move_number == 1 and player == 1):
            board._king(to_move)

        return board, capture, win


    def is_valid_move(self, from_move, to_move):

        # ensures that the given from move is a valid position
        # on the board
        if not Board.is_valid_position(from_move):
            return False

        # ensures that the given to move is a valid position
        # on the board
        if not Board.is_valid_position(to_move):
            return False
        
        # ensures that there actually is a piece at 
        # the from position
        from_value = self.get(from_move)
        if from_value == 0:
            return False

        # ensures that the peice cannot move 'in place'
        if from_move == to_move:
            return False

        # ensures that the place which the player is moving
        # to is empty
        to_value = self.get(to_move)
        if to_value != 0:
            return False

        is_king = from_value < 0
        player = abs(from_value)
        jump_possible = self.jump_possible_for_player(player)
        is_one_space = Board._only_one_space(from_move, to_move)

        if is_one_space and is_king and not jump_possible:
            return True

        if is_one_space and not is_king and not jump_possible:
            return Board.proper_direction(
                    from_move, to_move, player)

        if not is_one_space and is_king:
            return self.middle_is_enemy(
                    from_move, to_move, player)

        if not is_one_space and not is_king:
            return (
                Board.proper_direction(
                    from_move, to_move, player)
                and self.middle_is_enemy(
                    from_move, to_move, player)
            )

        return False


    def jump_possible_for_player(self, player):
        if player not in (1, 2):
            raise Exception('Invalid player number')

        positions = self.get_all_positions_for(player)
        for position in positions:
            if self.jump_possible(position):
                return True

        return False


    def middle_is_enemy(self, from_move, to_move, player):
        move = from_move + to_move
        if move not in Board.MIDDLE_SET:
            return False
        middle = Board.MIDDLE_SET[move]
        middle = self.get(middle)
        if middle == 0:
            return False
        return abs(middle) != player


    @classmethod
    def proper_direction(clazz, from_move, to_move, player):
        to_number = int(to_move[1])
        from_number = int(from_move[1])
        direction_vector = to_number - from_number

        if player == 1:
            return direction_vector < 0

        if player == 2:
            return direction_vector > 0

        raise Exception('Invalid player number: {}'.format(
            player))


    def _clone(self):
        ret = Board(line_sep=self._line_sep, 
            player_1_checker=self._player_1_checker, 
            player_1_king=self._player_1_king,
            player_2_checker=self._player_2_checker,
            player_2_king=self._player_2_king,
            blank_checker=self._blank_checker,
            player_1_name=self._player_1_name,
            player_2_name=self._player_2_name)
        ret._player_1_pieces = self._player_1_pieces
        ret._player_2_pieces = self._player_2_pieces
        for key in self._board:
            ret._board[key] = self._board[key]
        return ret


    @classmethod
    def _only_one_space(clazz, from_move, to_move): 
        return from_move in Board.ONE_SPACE_SET[to_move]


    def _set(self, position, value):
        Board._assert_valid_position(position)

        if value not in (-2, -1, 0, 1, 2):
            raise Exception('Invalid checker value: ' + str(value))

        self._board[position] = value


    def get(self, position):
        Board._assert_valid_position(position)
        return self._board[position]
    

    def is_king(self, position):
        return self.get(position) < 0


    def _king(self, position):
        value = self.get(position)
        if value == 0:
            raise Exception('Tried _king on empty spot')
        self._set(position, -abs(value))


    def display(self, message, moves_left):
        moves_left = 'Moves Left: {:4}'.format(moves_left)
        st  = '    |------------------------|' + self._line_sep
        st += '    | {:22} |'.format(moves_left) + self._line_sep
        st += str(self)
        st += '    | {:22} |'.format(message) + self._line_sep
        st += '    |------------------------|' + self._line_sep
        
        print(st)


    def get_all_positions_for(self, player):
        ret = []
        for position in Board.VALID_POSITIONS:
            pos_player = abs(self.get(position))
            if pos_player != player:
                continue
            ret.append(position)
        return ret


    def get_all_plays_for(self, player, capture):
        moves = self.get_all_jumps_for(player)
        if capture is not None:
            moves = [move for move in moves
                     if move[0] == capture]
            if len(moves) > 0:
                return moves
        return moves + self.get_all_moves_for(player)
    

    def get_all_jumps_for(self, player):
        return self._get_all_moves_from_set(player, Board.TWO_SPACE_SET)


    def get_all_moves_for(self, player):
        return self._get_all_moves_from_set(player, Board.ONE_SPACE_SET)

    
    def _get_all_moves_from_set(self, player, _set):
        positions = self.get_all_positions_for(player)
        ret = []
        for from_move in positions:
            move_set = _set[from_move]
            for to_move in move_set:
                if self.is_valid_move(from_move, to_move):
                    ret.append((from_move, to_move))
        return ret


    def absolute_to_relative_position(self, player, position):    
        return self._apply_position_mapping(player, position,
            Board.ABSOLUTE_TO_RELATIVE)
    

    def relative_to_absolute_position(self, player, position):
        return self._apply_position_mapping(player, position,
            Board.RELATIVE_TO_ABSOLUTE)


    def _apply_position_mapping(self, player, position, mapping):
        if player not in (1, 2):
            raise Exception('Invalid player number')
        
        # only flip one of the players
        if player == 2:
            return position
        else:
            return mapping[position]


    def absolute_to_relative_board(self, player):
        return self._apply_board_mapping(player, Board.ABSOLUTE_TO_RELATIVE)

    
    def relative_to_absolute_board(self, player):
        return self._apply_board_mapping(player, Board.RELATIVE_TO_ABSOLUTE)


    def _apply_board_mapping(self, player, mapping):
        ret = self._clone()

        for position in ret._board:
            mapped_location = self._apply_position_mapping(
                player, position, mapping)
            ret._board[position] = self._board[mapped_location]

        return ret


    def __str__(self):
        hr = '|------------------------|' + self._line_sep

        string = '    ' + hr
        string += '    | {:22} |'.format(
            '{} 1 ({:2}) {}{}'.format(
                '{:12}'.format(self._player_1_name), self._player_1_pieces, self._player_1_checker, self._player_1_king)
        ) + self._line_sep
       
        string += '    | {:22} |'.format(
            '{} 2 ({:2}) {}{}'.format(
                '{:12}'.format(self._player_2_name), self._player_2_pieces, self._player_2_checker, self._player_2_king)
        ) + self._line_sep

        space_first = True
        string += '|---'
        string += hr

        numbers = ['8', '7', '6', '5', '4', '3', '2', '1']
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        for number in numbers:
            string += '| {} |'.format(number)

            for letter in letters:
                combined = letter + number

                if not Board.is_valid_position(combined):
                    continue

                checker = self.get(combined)
                checker = self._checker_to_string(checker)

                if space_first:
                    string += '    ' + checker + ' '
                else:
                    string += ' ' + checker + '    '

            string += '|' + self._line_sep
            space_first = not space_first

        string += '|---'
        string += hr
        string += '    | A  B  C  D  E  F  G  H |' + self._line_sep
        string += '    |------------------------|' + self._line_sep

        return string


    def __repr__(self):
        return self.__str__()


    def _checker_to_string(self, checker):
        if checker == -2: return self._player_2_king
        if checker == -1: return self._player_1_king
        if checker == 0: return self._blank_checker
        if checker == 1: return self._player_1_checker
        if checker == 2: return self._player_2_checker
        raise Exception('Invalid Checker Type' + str(checker))
