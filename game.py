import time
import random
from board import Board
from humanplayer import HumanPlayer

from utils import clear

class Game(object):

    def __init__(self, player1, player2, player1_name='Player', player2_name='Player', 
            display=True, moves=100, delay=None, extra=False):
        self.player1 = player1
        self.player1_name = player1_name
        self.player2 = player2
        self.player2_name = player2_name
        self.display_game = display
        self.delay = delay
        # dont bother delaying the game if we cannot see it
        if not display:
            self.delay = None
        self.board = None
        self.moves = moves
        self.current_player = None
        self.num_moves_left = 0
        self.winning_player = None
        self.losing_player = None
        self._extra = extra

        if player1 is player2:
            raise Exception('Separate player instances required')


    def extra(self, msg):
        if self._extra:
            print(msg)


    def get_move(self, capture, prev_capture_location):
        player_number = self.get_number(self.current_player)

        capture_message = ''
        if capture:
            capture_message = 'Cap@{} '.format(prev_capture_location)

        self.prompt('{}Player {} Move!'.format(capture_message, player_number))

        if self.delay is not None:
            time.sleep(self.delay)

        from_move, to_move = self.current_player.get_move(
            player_number, self.board, prev_capture_location)

        while True:
            if from_move == '' and to_move == '':
                return '', ''

            if self.board.is_valid_move(from_move, to_move):
                from_player = abs(self.board.get(from_move))
                if from_player == player_number:
                    if not capture:
                        break

                    if prev_capture_location == from_move:
                        break

            self.prompt('Player {} Bad Move!'.format(player_number))
            
            self.current_player.bad_move(
                player_number, self.board, prev_capture_location, from_move, to_move)

            from_move, to_move = self.current_player.get_move(
                player_number, self.board, prev_capture_location)

        self.current_player.ok_move(
                player_number, self.board, 
                prev_capture_location, from_move, to_move)


        return from_move, to_move


    def run(self):
        self.extra('')
        self.player1.start()
        self.player2.start()

        self.board = Board(player_1_name=self.player1_name, player_2_name=self.player2_name)
        self.num_moves_left = self.moves
        self.current_player = self.random_player()
        self.extra('Player {} goes first'.format(self.get_number(self.current_player)))
        self.winning_player = None
        self.losing_player = None

        capture = False
        to_move = None
        
        # main game loop
        while self.num_moves_left > 0:
            if not self.current_can_make_move():
                self.losing_player = self.current_player
                self.swap_players()
                self.winning_player = self.current_player
                self.extra('Player {} won due to Player {} not being able to make a move'.format(
                    self.get_number(self.winning_player), self.get_number(self.losing_player)))
                break

            from_move, to_move = self.get_move(capture, to_move)
            if from_move == '':
                break

            board, capture, win = self.board.move(from_move, to_move)
            self.board = board

            if win:
                self.winning_player = self.current_player
                self.swap_players()
                self.losing_player = self.current_player
                self.extra('Player {} won due to move'.format(
                    self.get_number(self.winning_player)))
                break

            if capture:
                self.extra('Player {} made capture'.format(self.get_number(self.current_player)))

            if not capture or (capture and not self.board.jump_possible(to_move)):
                self.swap_players()
                capture = False
                to_move = None
            else:
                self.extra('Another jump possible for Player {}'.format(self.get_number(self.current_player)))

            self.num_moves_left -= 1
        
        if self.winning_player is None:
            self.extra('Draw')
            self.display('Draw!')
            self.player1.draw()
            self.player2.draw()
        else:
            self.display('Player {} Won!'.format(
                self.get_number(self.winning_player)))
            self.extra('Player {} Won!'.format(
                self.get_number(self.winning_player)))
            self.extra('Player {} Lost!'.format(
                self.get_number(self.losing_player)))
            self.winning_player.win()
            self.losing_player.lose()

        self.player1.end()
        self.player2.end()

        return self.winning_player


    def current_can_make_move(self):
        player_number = self.get_number(self.current_player)
        moves = self.board.get_all_moves_for(player_number)
        if len(moves) > 0:
            return True
        jumps = self.board.get_all_jumps_for(player_number)
        return len(jumps) > 0 


    def display(self, message):
        if self.display_game:
            clear()
            self.board.display(message, self.num_moves_left)


    def prompt(self, message):
        self.display(message)
        if self.display_game and type(self.current_player) is HumanPlayer:
            print('>>> ', end='')


    def random_player(self):
        if random.random() < .5:
            return self.player1
        else:
            return self.player2


    def get_number(self, player):
        if player is self.player1:
            return 1
        else:
            return 2


    def swap_players(self):
        if self.current_player is self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
