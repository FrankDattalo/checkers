from policynetplayer import PolicyNetPlayer
from game import Game

import sys

if __name__ == '__main__':
    num_generations = 10_000_000_000 # 10 billion
    p1 = PolicyNetPlayer(losses_file=sys.stdout, load_file='./policynet.h5', save_file='/output/policynet.h5')
    p2 = PolicyNetPlayer(losses_file=sys.stdout, load_file='./policynet.h5', save_file='/output/policynet.h5')
    game = Game(p1, 'PolicyNet 1', p2, 'PolicyNet 2', display=None)
    draws = 0
    p1wins = 0
    p2wins = 0
    for gen in range(num_generations):
        gen += 1
        winner = game.run()
        if winner is None:
            draws += 1
        elif winner is p1:
            p1wins += 1
        elif winner is p2:
            p2wins += 1
        else:
            raise Exception('This should not happen')
        print('Complete: {}/{}, P1 Wins: {:5}%, P2 Wins: {:5}%, Draws: {:5}%'.format(
                gen,
                num_generations,
                round(p1wins / gen * 100, 2),
                round(p2wins / gen * 100, 2),
                round(draws / gen * 100, 2))) 
