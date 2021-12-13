"""
--- Day 13: Transparent Origami ---
You reach another volcanically active part of the cave. It would be nice if you
could do some kind of thermal imaging so you could tell ahead of time which caves
are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you
activate it, you are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.
Apparently, the Elves have never used this feature. To your surprise, you manage
to find the manual; as you go to open it, page 1 falls out. It's a large sheet
of transparent paper! The transparent paper is marked with random dots and
includes instructions on how to fold it up (your puzzle input). For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
The first section is a list of dots on the transparent paper. 0,0 represents the
top-left coordinate. The first value, x, increases to the right. The second
value, y, increases downward. So, the coordinate 3,0 is to the right of 0,0, and
the coordinate 0,7 is below 0,0. The coordinates in this example form the
following pattern, where # is a dot on the paper and . is an empty, unmarked
position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Then, there is a list of fold instructions. Each instruction indicates a line on
the transparent paper and wants you to fold the paper up (for horizontal y=...
lines) or left (for vertical x=... lines). In this example, the first fold
instruction is fold along y=7, which designates the line formed by all of the
positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Because this is a horizontal line, fold the bottom half up. Some of the dots
might end up overlapping after the fold is complete, but dots will never appear
exactly on a fold line. The result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........
Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the
transparent paper is folded; after the fold is complete, those dots appear in
the top left corner (at 0,0 and 0,1). Because the paper is transparent, the dot
just below them in the result (at 0,3) remains visible, as it can be seen
through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge
together and become a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....
Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....
The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the
first fold. After the first fold in the example above, 17 dots are visible -
dots that end up overlapping after the fold is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on
your transparent paper?
"""

from utils import read_input_data, puzzle_a, puzzle_b
from collections import defaultdict

def pprint(paper):
    lines = max(paper)
    columns = max([max(paper[y]) for y in paper])

    for y in range(lines+1):
        for x in range(columns+1):
            if paper[y][x] > 0:
                print("#", end="")
            else:
                print(".", end="")
        print("")
    print("*" * 50)

def fold(paper, axis, amount):
    new_paper = defaultdict(lambda: defaultdict(int))

    for y in list(paper):
        for x in list(paper[y]):
            if axis == "y":
                if y > amount and 2 * amount - y >= 0:
                    new_paper[2 * amount - y][x] = paper[2 * amount - y][x] + paper[y][x]
            else:
                if x > amount and 2 * amount - x >= 0:
                    new_paper[y][2 * amount - x] = paper[y][2 * amount - x] + paper[y][x]

    return new_paper

def challenge_a(dots, folds, nr_folds = 1):
    paper = defaultdict(lambda: defaultdict(int))

    for x, y in dots:
        paper[y][x] = 1

    ### <hack> paper needs to be expanded
    lines = max(paper)
    columns = max([max(paper[y]) for y in paper])
    for y in range(lines+1):
        for x in range(columns+1):
            paper[y][x]
    ### </hack>

    for axis, amount in folds[:nr_folds]:
        paper = fold(paper, axis, amount)

    s = 0
    for y in paper:
        for x in paper[y]:
            s += 1 if paper[y][x] > 0 else 0

    return s, paper

def parse_data(data):
    lines = [line for line in data.strip().split("\n") if line != ""]

    dots = []
    folds = []
    for line in lines:
        if "fold" in line:
            axis, amount = line.replace("fold along ", "").split("=")
            amount = int(amount)
            folds.append((axis, amount))
        elif "," in line:
            x, y = line.split(",")
            x, y = int(x), int(y)
            dots.append((x,y))
        else:
            raise Exception("invalid line")

    return dots, folds

def solve_challenge_a(data):
    dots, folds = parse_data(data)
    nr_dots, paper = challenge_a(dots, folds)
    return nr_dots

challenge_test_data = \
"""
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

assert solve_challenge_a(challenge_test_data) == 17

"""
Finish folding the transparent paper according to the instructions. The manual
says the code is always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?
"""

def solve_challenge_b(data):
    dots, folds = parse_data(data)
    pprint(challenge_a(dots, folds, nr_folds = len(folds))[1])

if __name__ == "__main__":
    DAY = 13
    puzzle_a(DAY, solve_challenge_a) # 850
    puzzle_b(DAY, solve_challenge_b) # AHGCPGAU
