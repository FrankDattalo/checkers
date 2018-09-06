from board import Board

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

plays = []

for li, letter in enumerate(letters):
    for ni, number in enumerate(numbers):
        position = letter + number

        if not Board.is_valid_position(position):
            continue

        all_plays = []
        moves = Board.ONE_SPACE_SET[position]
        jumps = Board.TWO_SPACE_SET[position]

        all_plays += moves
        all_plays += jumps

        for play in all_plays:
            plays.append((position, play))

for play in plays:
    print('{},'.format(play))