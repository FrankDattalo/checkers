import board

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
numbers = [str(number) for number in numbers]

def display(center, to, contin):
    if not board.Board.is_valid_position(center): return
    
    if len(to) == 2 and len(contin) == 2:
        print("'{}{}': '{}',".format(center, contin, to))

for lettersi, letter in enumerate(letters):
    for numbersi, number in enumerate(numbers):
        left_1_letter = ''
        left_1_number = ''
        left_2_letter = ''
        left_2_number = ''
        right_1_letter = ''
        right_1_number = ''
        right_2_letter = ''
        right_2_number = ''

        if lettersi > 0:
            left_1_letter = letters[lettersi - 1]
        if numbersi > 0:
            left_1_number = numbers[numbersi - 1]
        if lettersi > 1:
            left_2_letter = letters[lettersi - 2]
        if numbersi > 1:
            left_2_number = numbers[numbersi - 2]
        if lettersi < 7:
            right_1_letter = letters[lettersi + 1]
        if numbersi < 7:
            right_1_number = numbers[numbersi + 1]
        if lettersi < 6:
            right_2_letter = letters[lettersi + 2]
        if numbersi < 6:
            right_2_number = numbers[numbersi + 2]

        center = letter + number
        leftleft1 = left_1_letter + left_1_number
        leftright1 = left_1_letter + right_1_number
        rightleft1 = right_1_letter + left_1_number
        rightright1 = right_1_letter + right_1_number

        top_left = left_2_letter + right_2_number
        top_right = right_2_letter + right_2_number
        bottom_left = left_2_letter + left_2_number
        bottom_right = right_2_letter + left_2_number

        display(center, leftleft1, bottom_left)
        display(center, leftright1, top_left)
        display(center, rightleft1, bottom_right)
        display(center, rightright1, top_right)


        
