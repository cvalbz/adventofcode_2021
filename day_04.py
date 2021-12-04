"""
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean,
already so deep that you can't see any sunlight. What you can see, however,
is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers.
Numbers are chosen at random, and the chosen number is marked on all boards
on which it appears. (Numbers may not appear on all boards.) If all numbers
in any row or any column of a board are marked, that board wins.
(Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and
the giant squid) pass the time. It automatically generates a random order
in which to draw numbers and a random set of boards (your puzzle input).
For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7

After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no
winners, but the boards are marked as follows (shown here adjacent to each
other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are
still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row
or column of marked numbers (in this case, the entire top row is
marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum
of all unmarked numbers on that board; in this case, the sum is 188. Then,
multiply that sum by the number that was just called when the board won, 24,
to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win
first. What will your final score be if you choose that board?
"""

from utils import read_input_data, puzzle_a, puzzle_b

class Board:
    def __init__(self, board):
        self.board = board
        self.N = len(board) # square board
        self.marked = []

    def mark(self, number):
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i][j] == number:
                    self.marked.append((i,j))

    def game_finished(self):
        for i in range(self.N):
            lines = [(i, j) for j in range(self.N)]
            if all([c in self.marked for c in lines]):
                return True
            columns = [(j, i) for j in range(self.N)]
            if all([c in self.marked for c in columns]):
                return True

        return False
    
    def score(self):
        s = 0
        for i in range(self.N):
            for j in range(self.N):
                if (i,j) not in self.marked:
                    s += self.board[i][j]
        i, j = self.marked[-1]
        return s * self.board[i][j]

def challenge_a(numbers, boards):
    for n in numbers:
        for b in boards:
            b.mark(n)
            if b.game_finished():
                return b.score()

def parse_data(data):
    lines = data.strip().split("\n")
    lines = [i for i in lines if i != ""]

    numbers = map(int, lines[0].split(","))
    boards = [lines[i*5+1:(i+1)*5+1] for i in range(len(lines[1:]) // 5)]
    boards = [[tuple(map(int, line.split())) for line in b] for b in boards]
    boards = [Board(b) for b in boards]

    return (numbers, boards)

def solve_challenge_a(data):
    numbers, boards = parse_data(data)
    return challenge_a(numbers, boards)

challenge_test_data = \
"""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

assert solve_challenge_a(challenge_test_data) == 4512

"""
--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant
squid win.

You aren't sure how many bingo boards a giant squid could play at once, so
rather than waste time counting its arms, the safe thing to do is to figure
out which board will win last and choose that one. That way, no matter which
boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after
13 is eventually called and its middle column is completely marked. If you were
to keep playing until this point, the second board would have a sum of unmarked
numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?
"""

def challenge_b(numbers, boards):
    done = set()

    for n in numbers:
        for ix, b in enumerate(boards):
            b.mark(n)
            if b.game_finished():
                if ix not in done:
                    done.add(ix)
                    if len(done) == len(boards):
                        return b.score()

def solve_challenge_b(data):
    numbers, boards = parse_data(data)
    return challenge_b(numbers, boards)

assert solve_challenge_b(challenge_test_data) == 1924

if __name__ == "__main__":
    DAY = 4
    puzzle_a(DAY, solve_challenge_a) # 29440
    puzzle_b(DAY, solve_challenge_b) # 13884 
