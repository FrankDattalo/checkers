import os
import sys

# disables tensorflow debug logging for feature guard
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# hides the keras debugging messages
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

from policynetplayer import PolicyNetPlayer
from game import Game
from multiprocessing import Pool
import numpy as np
from utils import unzip, Timer

sys.stderr = stderr

class MulticorePolicyNetPlayer(PolicyNetPlayer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._total_X = []
        self._total_y = []


    def get_X_y(self):
        return np.vstack(self._total_X), np.vstack(self._total_y)


    def end(self):
        pass

    
    def start(self):
        self._history = []


    def win(self):
        self._record(self._win_reward)


    def lose(self):
        self._record(self._loss_reward)


    def draw(self):
        self._record(self._draw_reward)


    def _record(self, value):
        X, y = self._discount_reward_and_serialize(value)
        self._total_X.append(X)
        self._total_y.append(y.reshape(len(y), 1))


    def super_start(self):
        super().start()


def playing_step(args, load=True):
    epoch, total_epochs, games = args

    p1 = MulticorePolicyNetPlayer()
    if load:
        p1._net = p1._load()
    else:
        p1.super_start()

    p2 = MulticorePolicyNetPlayer()
    if load:
        p2._net = p1._net
    else:
        p2.super_start()

    game = Game(p1, p2, display=False)

    for g in range(games):
        game.run()
        print('Epoch {}/{} Game {}/{}'.format(epoch, total_epochs, g + 1, games))

    p1X, p1y = p1.get_X_y()
    p2X, p2y = p2.get_X_y()

    X = np.vstack([p1X, p2X])
    y = np.vstack([p1y, p2y])

    return X, y


if __name__ == '__main__':

    p = PolicyNetPlayer()
    PolicyNetPlayer._cached_net = None
    p.start()
    p.end()
    p = None
    PolicyNetPlayer._cached_net = None

    num_epochs = 200
    parallelism = 1
    num_games_per_epoch = 25

    if parallelism > 1:
        pool = Pool(parallelism)
    else:
        pool = None

    timer = Timer()
    timer.reset()

    for e in range(num_epochs):
        e += 1
        args = (e, num_epochs, num_games_per_epoch)

        workers = [args] * parallelism

        print('Epoch', e, 'playing starting')
        if parallelism > 1:
            result = pool.map(playing_step, workers)
            X, y = unzip(result)
            X = np.vstack(X)
            y = np.vstack(y)
        else:
            X, y = playing_step(args, load=False)
        print('Epoch', e, 'playing finished')

        print('Epoch', e, 'training starting')
        p = PolicyNetPlayer()
        if parallelism > 1:
            PolicyNetPlayer._cached_net = None
        p.start()
        p.train(X, y, verbose=1)
        p.end()
        print('Epoch', e, 'training finished')

        print(timer.eta(e + 1, num_epochs))
        
        
        
    