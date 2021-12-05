"""
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents
constantly produce large, opaque clouds, so it would be best to avoid them if
possible.

They tend to form in lines; the submarine helpfully produces a list of nearby
lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where
x1,y1 are the coordinates of one end the line segment and x2,y2 are the
coordinates of the other end. These line segments include the points at both
ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either
x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the
following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9.
Each position is shown as the number of lines which cover that point or . if no
line covers that point. The top-left pair of 1s, for example, comes from
2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9
and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points
where at least two lines overlap. In the above example, this is anywhere in
the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least
two lines overlap?
"""

from utils import read_input_data, puzzle_a, puzzle_b
from collections import defaultdict
from utils import int_range_incl

def challenge_a(segments):
    board = defaultdict(lambda : defaultdict(int))

    for a, b in segments:
        x1, y1 = a
        x2, y2 = b

        if x1 == x2:
            for i in int_range_incl(y1, y2):
                board[i][x1] += 1
        elif y1 == y2:
            for i in int_range_incl(x1, x2):
                board[y1][i] += 1
        else:
            continue # "only horizontal and vertical lines"

    result = 0
    for _, lines in board.items():
        for _, v in lines.items():
            if v >= 2:
                result += 1

    return result

def parse_data(data):
    lines = data.strip().split("\n")
    lines = [i.split(" -> ") for i in lines]

    def parse_segment(s):
        a, b = s
        x1, y1 = list(map(int, a.split(",")))
        x2, y2 = list(map(int, b.split(",")))
        return ((x1, y1), (x2, y2))

    segments = [parse_segment(i) for i in lines]
    return segments

def solve_challenge_a(data):
    segments = parse_data(data)
    return challenge_a(segments)

challenge_test_data = \
"""
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

assert solve_challenge_a(challenge_test_data) == 5

"""
--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you
the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your
list will only ever be horizontal, vertical, or a diagonal line at exactly 45
degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following
diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....

You still need to determine the number of points where at least two lines overlap.
In the above example, this is still anywhere in the diagram with a 2 or larger -
now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?
"""

def challenge_b(segments):
    board = defaultdict(lambda : defaultdict(int))

    for a, b in segments:
        x1, y1 = a
        x2, y2 = b

        if x1 == x2:
            for i in int_range_incl(y1, y2):
                board[i][x1] += 1
        elif y1 == y2:
            for i in int_range_incl(x1, x2):
                board[y1][i] += 1
        elif abs(x1 - x2) == abs(y1 - y2):
            for i, j in zip(int_range_incl(x1, x2), int_range_incl(y1, y2)):
                board[j][i] += 1
        else:
            continue # "only horizontal, vertical lines and diagonal"

    result = 0
    for _, lines in board.items():
        for _, v in lines.items():
            if v >= 2:
                result += 1

    return result

def solve_challenge_b(data):
    segments = parse_data(data)
    return challenge_b(segments)

assert solve_challenge_b(challenge_test_data) == 12

if __name__ == "__main__":
    DAY = 5
    puzzle_a(DAY, solve_challenge_a) # 7468
    puzzle_b(DAY, solve_challenge_b) # 22364
