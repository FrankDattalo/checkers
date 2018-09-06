import board

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
numbers = [str(number) for number in numbers]

for lettersi, letter in enumerate(letters):
    for numbersi, number in enumerate(numbers):
        center = letter + number
        if not board.Board.is_valid_position(center): continue

        left_2_letter = ''
        left_2_number = ''
        right_2_letter = ''
        right_2_number = ''

        if lettersi > 1:
            left_2_letter = letters[lettersi - 2]
        if numbersi > 1:
            left_2_number = numbers[numbersi - 2]
        if lettersi < 6:
            right_2_letter = letters[lettersi + 2]
        if numbersi < 6:
            right_2_number = numbers[numbersi + 2]


        top_left = left_2_letter + right_2_number
        top_right = right_2_letter + right_2_number
        bottom_left = left_2_letter + left_2_number
        bottom_right = right_2_letter + left_2_number

        moves = [top_left, top_right, bottom_left, bottom_right]
        moves = [move for move in moves if len(move) == 2]

        print("'{}': (".format(center), end='')
        for move in moves:
            print("'{}',".format(move), end='')
        print('),')        
