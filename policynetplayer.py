from player import Player
from board import Board

import os
import random
import numpy as np

from keras.models import load_model
from keras.layers import Activation, Dense
from keras.models import Sequential
from keras.utils import multi_gpu_model

from utils import no_interrupt


class PolicyNetPlayer(Player):

    # shared neural network
    _cached_net = None

    # all possible plays, combined with all valid positions, and the count
    # of the pieces for each player
    INPUT_SIZE = len(Board.POSSIBLE_PLAYS) + len(Board.VALID_POSITIONS) + 2

    
    CURRENT_PIECE_COUNT_INDEX = 0

    OTHER_PIECE_COUNT_INDEX = 1

    PLAY_LOOKUP = {
        ('A1', 'B2'): 2,
        ('A1', 'C3'): 3,
        ('A3', 'B2'): 4,
        ('A3', 'B4'): 5,
        ('A3', 'C5'): 6,
        ('A3', 'C1'): 7,
        ('A5', 'B4'): 8,
        ('A5', 'B6'): 9,
        ('A5', 'C7'): 10,
        ('A5', 'C3'): 11,
        ('A7', 'B6'): 12,
        ('A7', 'B8'): 13,
        ('A7', 'C5'): 14,
        ('B2', 'A1'): 15,
        ('B2', 'A3'): 16,
        ('B2', 'C1'): 17,
        ('B2', 'C3'): 18,
        ('B2', 'D4'): 19,
        ('B4', 'A3'): 20,
        ('B4', 'A5'): 21,
        ('B4', 'C3'): 22,
        ('B4', 'C5'): 23,
        ('B4', 'D6'): 24,
        ('B4', 'D2'): 25,
        ('B6', 'A5'): 26,
        ('B6', 'A7'): 27,
        ('B6', 'C5'): 28,
        ('B6', 'C7'): 29,
        ('B6', 'D8'): 30,
        ('B6', 'D4'): 31,
        ('B8', 'A7'): 32,
        ('B8', 'C7'): 33,
        ('B8', 'D6'): 34,
        ('C1', 'B2'): 35,
        ('C1', 'D2'): 36,
        ('C1', 'A3'): 37,
        ('C1', 'E3'): 38,
        ('C3', 'B2'): 39,
        ('C3', 'B4'): 40,
        ('C3', 'D2'): 41,
        ('C3', 'D4'): 42,
        ('C3', 'A5'): 43,
        ('C3', 'E5'): 44,
        ('C3', 'A1'): 45,
        ('C3', 'E1'): 46,
        ('C5', 'B4'): 47,
        ('C5', 'B6'): 48,
        ('C5', 'D4'): 49,
        ('C5', 'D6'): 50,
        ('C5', 'A7'): 51,
        ('C5', 'E7'): 52,
        ('C5', 'A3'): 53,
        ('C5', 'E3'): 54,
        ('C7', 'B6'): 55,
        ('C7', 'B8'): 56,
        ('C7', 'D6'): 57,
        ('C7', 'D8'): 58,
        ('C7', 'A5'): 59,
        ('C7', 'E5'): 60,
        ('D2', 'C1'): 61,
        ('D2', 'C3'): 62,
        ('D2', 'E1'): 63,
        ('D2', 'E3'): 64,
        ('D2', 'B4'): 65,
        ('D2', 'F4'): 66,
        ('D4', 'C3'): 67,
        ('D4', 'C5'): 68,
        ('D4', 'E3'): 69,
        ('D4', 'E5'): 70,
        ('D4', 'B6'): 71,
        ('D4', 'F6'): 72,
        ('D4', 'B2'): 73,
        ('D4', 'F2'): 74,
        ('D6', 'C5'): 75,
        ('D6', 'C7'): 76,
        ('D6', 'E5'): 77,
        ('D6', 'E7'): 78,
        ('D6', 'B8'): 79,
        ('D6', 'F8'): 80,
        ('D6', 'B4'): 81,
        ('D6', 'F4'): 82,
        ('D8', 'C7'): 83,
        ('D8', 'E7'): 84,
        ('D8', 'B6'): 85,
        ('D8', 'F6'): 86,
        ('E1', 'D2'): 87,
        ('E1', 'F2'): 88,
        ('E1', 'C3'): 89,
        ('E1', 'G3'): 90,
        ('E3', 'D2'): 91,
        ('E3', 'D4'): 92,
        ('E3', 'F2'): 93,
        ('E3', 'F4'): 94,
        ('E3', 'C5'): 95,
        ('E3', 'G5'): 96,
        ('E3', 'C1'): 97,
        ('E3', 'G1'): 98,
        ('E5', 'D4'): 99,
        ('E5', 'D6'): 100,
        ('E5', 'F4'): 101,
        ('E5', 'F6'): 102,
        ('E5', 'C7'): 103,
        ('E5', 'G7'): 104,
        ('E5', 'C3'): 105,
        ('E5', 'G3'): 106,
        ('E7', 'D6'): 107,
        ('E7', 'D8'): 108,
        ('E7', 'F6'): 109,
        ('E7', 'F8'): 110,
        ('E7', 'C5'): 111,
        ('E7', 'G5'): 112,
        ('F2', 'E1'): 113,
        ('F2', 'E3'): 114,
        ('F2', 'G1'): 115,
        ('F2', 'G3'): 116,
        ('F2', 'D4'): 117,
        ('F2', 'H4'): 118,
        ('F4', 'E3'): 119,
        ('F4', 'E5'): 120,
        ('F4', 'G3'): 121,
        ('F4', 'G5'): 122,
        ('F4', 'D6'): 123,
        ('F4', 'H6'): 124,
        ('F4', 'D2'): 125,
        ('F4', 'H2'): 126,
        ('F6', 'E5'): 127,
        ('F6', 'E7'): 128,
        ('F6', 'G5'): 129,
        ('F6', 'G7'): 130,
        ('F6', 'D8'): 131,
        ('F6', 'H8'): 132,
        ('F6', 'D4'): 133,
        ('F6', 'H4'): 134,
        ('F8', 'E7'): 135,
        ('F8', 'G7'): 136,
        ('F8', 'D6'): 137,
        ('F8', 'H6'): 138,
        ('G1', 'F2'): 139,
        ('G1', 'H2'): 140,
        ('G1', 'E3'): 141,
        ('G3', 'F2'): 142,
        ('G3', 'F4'): 143,
        ('G3', 'H2'): 144,
        ('G3', 'H4'): 145,
        ('G3', 'E5'): 146,
        ('G3', 'E1'): 147,
        ('G5', 'F4'): 148,
        ('G5', 'F6'): 149,
        ('G5', 'H4'): 150,
        ('G5', 'H6'): 151,
        ('G5', 'E7'): 152,
        ('G5', 'E3'): 153,
        ('G7', 'F6'): 154,
        ('G7', 'F8'): 155,
        ('G7', 'H6'): 156,
        ('G7', 'H8'): 157,
        ('G7', 'E5'): 158,
        ('H2', 'G1'): 159,
        ('H2', 'G3'): 160,
        ('H2', 'F4'): 161,
        ('H4', 'G3'): 162,
        ('H4', 'G5'): 163,
        ('H4', 'F6'): 164,
        ('H4', 'F2'): 165,
        ('H6', 'G5'): 166,
        ('H6', 'G7'): 167,
        ('H6', 'F8'): 168,
        ('H6', 'F4'): 169,
        ('H8', 'G7'): 170,
        ('H8', 'F6'): 171,
    }

    POSITION_LOOKUP = {
        'A1': 172,
        'C1': 173,
        'E1': 174,
        'G1': 175,
        'B2': 176,
        'D2': 177,
        'F2': 178,
        'H2': 179,
        'A3': 180,
        'C3': 181,
        'E3': 182,
        'G3': 183,
        'B4': 184,
        'D4': 185,
        'F4': 186,
        'H4': 187,
        'A5': 188,
        'C5': 189,
        'E5': 190,
        'G5': 191,
        'B6': 192,
        'D6': 193,
        'F6': 194,
        'H6': 195,
        'A7': 196,
        'C7': 197,
        'E7': 198,
        'G7': 199,
        'B8': 200,
        'D8': 201,
        'F8': 202,
        'H8': 203,
    }
    
    def __init__(self, 
            file_name='./policynet.h5', 
            reward_discount_rate=.90,
            win_reward=10,
            loss_reward=-10,
            draw_reward=-10,
            losses_file=None,
            load_file=None,
            save_file=None,
            hidden_layers=30,
            hidden_layer_size=500):
        self._file_name = file_name
        self._reward_discount_rate = reward_discount_rate
        self._win_reward = win_reward
        self._loss_reward = loss_reward
        self._draw_reward = draw_reward
        self._losses_file = losses_file
        self._load_file = load_file
        self._save_file = save_file
        self._history = []
        self._net = None
        self._hidden_layer_size = hidden_layer_size
        self._hidden_layers = hidden_layers


    def get_move(self, player_number, board, previous_capture_position):
        available_plays = board.get_all_plays_for(player_number, previous_capture_position)

        # normalized value predictions
        values = np.array([self._predict(player_number, board, play) for play in available_plays])
        min_value = min(values)
        values -= min_value
        # small epsilon value added to ensure that everything has some probability
        values += 1e-8
        sum_values = sum(values)
        values /= sum_values

        # weighted sampling
        index = np.random.choice(len(available_plays), p=values)
        play = available_plays[index]

        return play


    def ok_move(self, player_number, board, previous_capture_position, from_move, to_move):
        serialized_input = self._serialize(
            player_number, board, (from_move, to_move))
        self._history.append(serialized_input)


    def bad_move(self, player_number, board, previous_capture_position, from_move, to_move):
        raise Exception('This should not happen')


    def start(self):
        self._history = []

        with no_interrupt:
            if PolicyNetPlayer._cached_net is not None:
                self._net = PolicyNetPlayer._cached_net
                return

            if os.path.exists(self._file_name):
                self._net = self._load()
            else:
                self._net = self._create()

            PolicyNetPlayer._cached_net = self._net


    def end(self):
        with no_interrupt:
            self._save()


    def win(self):
        self._train_with_reward(self._win_reward)


    def lose(self):
        self._train_with_reward(self._loss_reward)


    def draw(self):
        self._train_with_reward(self._draw_reward)


    def _predict(self, player_number, board, play):
        serialized = self._serialize(player_number, board, play)
        return self._pred(serialized)[0, 0]


    def _serialize(self, player_number, board, play):

        X = np.zeros([1, PolicyNetPlayer.INPUT_SIZE])
        
        # 2 = our king checker
        # 1 = our normal checker
        # 0 = blank space
        # -1 = their checker
        # -2 = their king checker

        # using relative positioning and the following scheme,
        # serialize the values of the board
        for position in Board.VALID_POSITIONS:
            value_at_position = board.get(position)
            if value_at_position != 0:
                # some checker
                value = 1
                # some king
                if value_at_position < 0:
                    value += 1
                # other persons checker
                if abs(value_at_position) != player_number:
                    value *= -1
                value_at_position = value
            relative_position = board.absolute_to_relative_position(
                player_number, position)
            position_index = PolicyNetPlayer.POSITION_LOOKUP[relative_position]
            X[0, position_index] = value_at_position
        
        # serialize the value of the play
        from_move = board.absolute_to_relative_position(
            player_number, play[0])
        to_move = board.absolute_to_relative_position(
            player_number, play[1])
        relative_play = from_move, to_move
        action_index = PolicyNetPlayer.PLAY_LOOKUP[relative_play]
        X[0, action_index] = 1

        # serialize the values of the piece counts
        our_pieces = None
        their_pieces = None
        if player_number == 1:
            our_pieces = board.player_1_pieces()
            their_pieces = board.player_2_pieces()
        else:
            our_pieces = board.player_2_pieces()
            their_pieces = board.player_1_pieces()
        X[0, PolicyNetPlayer.CURRENT_PIECE_COUNT_INDEX] = our_pieces
        X[0, PolicyNetPlayer.OTHER_PIECE_COUNT_INDEX] = their_pieces

        return X


    def _discount_reward_and_serialize(self, value):
        X = []
        y = []

        # applies reward to history items
        for history_element in reversed(self._history):
            X.append(history_element)
            y.append(value)
            value *= self._reward_discount_rate
            
        # train on the history items
        X = np.vstack(X)
        y = np.array(y)

        return X, y


    def _train_with_reward(self, value):
        X, y = self._discount_reward_and_serialize(value)

        with no_interrupt:
            self._train(X, y)

    
    def _create(self):
        hidden_layers = self._hidden_layers
        hidden_layer_size = self._hidden_layer_size
        activations = 'relu'

        model = Sequential()
        model.add(Dense(hidden_layer_size, input_dim=PolicyNetPlayer.INPUT_SIZE))
        model.add(Activation(activations))

        for _ in range(hidden_layers - 1):
            model.add(Dense(hidden_layer_size))
            model.add(Activation(activations))

        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mse')

        return model


    def _load(self):
        file_name = self._load_file if self._load_file is not None else self._file_name
        model = load_model(file_name)
        return model


    def _train(self, X, y, verbose=0):
        history = self._net.fit(X, y, epochs=1, verbose=verbose)
        loss = history.history['loss'][0]
        if self._losses_file is not None:
            if type(self._losses_file) is not str:
                self._losses_file.write('{}\n'.format(loss))
            else:
                with open(self._losses_file, mode='a') as f:
                    f.write('{}\n'.format(loss))
        return loss


    def _pred(self, X):
        return self._net.predict(X)


    def _save(self):
        file_name = self._save_file if self._save_file is not None else self._file_name
        self._net.save(file_name)

