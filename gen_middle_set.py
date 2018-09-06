import board

def c(position):
    return '' if len(position) < 2 else position

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
for letteri, letter in enumerate(letters):
    for numberi, number in enumerate(numbers):
        if board.Board.is_valid_position(letter + str(number)):
            left_letter = ''
            right_letter = ''
            left_number = ''
            right_number = ''
            if letteri > 0:
                left_letter = letters[letteri - 1]
            if letteri < 7:
                right_letter = letters[letteri + 1]
            if numberi > 0:
                left_number = str(numbers[numberi - 1])
            if numberi < 7:
                right_number = str(numbers[numberi + 1])
            leftleft = c(left_letter + left_number)
            leftright = c(left_letter + right_number)
            rightleft = c(right_letter + left_number)
            rightright = c(right_letter + right_number)
            moves = [leftleft, leftright, rightleft, rightright]
            moves = [move for move in moves if len(move) == 2]
            center = letter + str(number)
            print("'{}': (".format(center),end='')
            for move in moves:
                print("'{}',".format(move),end='')
            print('),')
