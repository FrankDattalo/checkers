from board import Board

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

def for_each(fn):
    for li, letter in enumerate(letters):
        for ni, number in enumerate(numbers):
            position = letter + number
            if not Board.is_valid_position(position):
                continue
            liOff = 7 - li
            niOff = 7 - ni
            to = letters[liOff] + numbers[niOff]
            fn(position, to)

for_each(lambda f, s: print("'{}': '{}',".format(f, s)))

print()

for_each(lambda f, s: print("'{}': '{}',".format(s, f)))
