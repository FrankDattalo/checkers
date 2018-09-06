from board import Board
from policynetplayer import PolicyNetPlayer

acc = 2
for play in Board.POSSIBLE_PLAYS:
    print("{}: {},".format(play, acc))
    acc += 1

print()

for position in Board.VALID_POSITIONS:
    print("'{}': {},".format(position, acc))
    acc += 1
