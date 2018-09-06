from game import Game
from randomplayer import RandomPlayer
from humanplayer import HumanPlayer
from policynetplayer import PolicyNetPlayer
from utils import choose, clear

def normal_game():
    player_types = {
        'Human': (HumanPlayer, 'Human'),
        'Random': (RandomPlayer, 'Random'),
        'PolicyNet': (PolicyNetPlayer, 'PolicyNet')
    }

    display = choose('Display?', {
        'Display': True,
        'No Display': False
    })

    delay = choose('Delay?', {
        'None': None,
        '50 milliseconds': 0.050,
        '250 milliseconds': 0.250,
        '1 second': 1,
        '5 seconds': 5
    })

    num_moves = choose('Moves Before Draw?', {
        '100': 100,
        '50': 50,
        '200': 200,
        '1,000': 1000
    })

    player1, player1_name = choose('Player 1 Type?', player_types)
    player1 = player1()
    
    player2, player2_name = choose('Player 2 Type?', player_types)
    player2 = player2()
    
    game = Game(player1, player2, player1_name=player1_name, 
        player2_name=player2_name, display=display, moves=num_moves, delay=delay)

    game.run()


def generations_game():
    player_types = {
        'Random': (RandomPlayer, 'Random'),
        'PolicyNet': (PolicyNetPlayer, 'PolicyNet')
    }

    num_generations = choose('Number of Simulations?', {
        '10': 10,
        '100': 100,
        '1,000': 1000,
        '10,000': 10000,
        '100,000': 100000,
        '1,000,000': 1000000
    })

    num_moves = choose('Moves Before Draw?', {
        '100': 100,
        '50': 50,
        '200': 200,
        '1,000': 1000
    })

    print_interval = choose('Update Interval?', {
        'Every Round': 1,
        '10 Rounds': 10,
        '100 Rounds': 100,
        '1,000 Rounds': 1000,
        '10,000 Rounds': 10000 
    })

    player1, player1_name = choose('Player 1 Type?', player_types)
    player1 = player1()

    player2, player2_name = choose('Player 2 Type?', player_types)
    player2 = player2()

    game = Game(player1, player2, player1_name=player1_name, 
        player2_name=player2_name, display=None, moves=num_moves)

    player1_wins = 0
    player2_wins = 0
    draws = 0

    for gen in range(num_generations):
        winner = game.run()
        
        if winner is not None:
            if winner is player1:
                player1_wins += 1
            else:
                player2_wins += 1
        else:
            draws += 1

        if gen % print_interval == 0:
            # prevents divide by zero
            gen += 1
            clear()
            print('Complete: {}/{}, {} 1 Wins: {:5}%, {} 2 Wins: {:5}%, Draws: {:5}%'.format(
                gen,
                num_generations,
                player1_name,
                round(player1_wins / gen * 100, 2),
                player2_name,
                round(player2_wins / gen * 100, 2),
                round(draws / gen * 100, 2))) 

def main():
    game_type = choose('Game Type?', {
        'Normal': 'n',
        'Fast Forward': 's'
    })

    if game_type == 'n':
        normal_game()

    elif game_type == 's':
        generations_game()

if __name__ == '__main__':
    main()
