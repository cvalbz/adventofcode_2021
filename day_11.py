"""
You enter a large cavern full of rare bioluminescent dumbo octopuses! They seem
to not like the Christmas lights on your submarine, so you turn them off for now.

There are 100 octopuses arranged neatly in a 10 by 10 grid. Each octopus slowly
gains energy over time and flashes brightly for a moment when its energy is full.
Although your lights are off, maybe you could navigate through the cave without
disturbing the octopuses if you could predict when the flashes of light will happen.

Each octopus has an energy level - your submarine can remotely measure the
energy level of each octopus (your puzzle input). For example:

5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526

The energy level of each octopus is a value between 0 and 9. Here, the top-left
octopus has an energy level of 5, the bottom-right one has an energy level of 6,
and so on.

You can model the energy levels and flashes of light in steps. During a single
step, the following occurs:

First, the energy level of each octopus increases by 1.
Then, any octopus with an energy level greater than 9 flashes. This increases
the energy level of all adjacent octopuses by 1, including octopuses that are
diagonally adjacent. If this causes an octopus to have an energy level greater
than 9, it also flashes. This process continues as long as new octopuses keep
having their energy level increased beyond 9. (An octopus can only flash at
most once per step.)
Finally, any octopus that flashed during this step has its energy level set to
0, as it used all of its energy to flash.
Adjacent flashes can cause an octopus to flash on a step even if it begins
that step with very little energy. Consider the middle octopus with 1 energy in
this situation:

Before any steps:
11111
19991
19191
19991
11111

After step 1:
34543
40004
50005
40004
34543

After step 2:
45654
51115
61116
51115
45654
An octopus is highlighted when it flashed during the given step.

Here is how the larger example above progresses:

Before any steps:
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526

After step 10, there have been a total of 204 flashes. Fast forwarding, here is
the same configuration every 10 steps:

After step 20:
3936556452
5686556806
4496555690
4448655580
4456865570
5680086577
7000009896
0000000344
6000000364
4600009543

After 100 steps, there have been a total of 1656 flashes.

Given the starting energy levels of the dumbo octopuses in your cavern, simulate
100 steps. How many total flashes are there after 100 steps?

"""

from utils import read_input_data, puzzle_a, puzzle_b

def get_neighs(m, i, j):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]
    for ix, jx in directions:
        neigh_i, neigh_j = i + ix, j + jx

        if neigh_i < 0 or neigh_i >= len(m) or neigh_j < 0 or neigh_j >= len(m[i]):
            continue

        yield neigh_i, neigh_j

class Octopus:
    def __init__(self, octopuses, position, energy):
        self.i, self.j = position
        self.energy = energy
        self.flashed = False
        self.octopuses = octopuses

    def tick(self):
        if self.flashed: return
        self.energy += 1
        if self.energy > 9:
            if not self.flashed:
                self.flashed = True
                for a, b in get_neighs(self.octopuses, self.i, self.j):
                    self.octopuses[a][b].tick()
                self.energy = 0

def init_octopuses(data):
    octopuses = []
    for i in range(len(data)):
        octopuses.append([None] * len(data[i]))
    
    for i in range(len(data)):
        for j in range(len(data[i])):
            octopuses[i][j] = Octopus(octopuses, (i, j), data[i][j])

    return octopuses

def tick_octopuses(octopuses):
    for i in range(len(octopuses)):
        for j in range(len(octopuses[i])):
            octopuses[i][j].tick()

def reset_flashes(octopuses):
    for i in range(len(octopuses)):
        for j in range(len(octopuses[i])):
            octopuses[i][j].flashed = False

def challenge_a(data, steps):
    octopuses = init_octopuses(data)

    flashes = 0
    for step in range(1, steps+1):
        tick_octopuses(octopuses)

        # count flashes
        for i in range(len(octopuses)):
            for j in range(len(octopuses[i])):
                if octopuses[i][j].flashed:
                    flashes += 1
            
        reset_flashes(octopuses)

    return flashes

def parse_data(data):
    lines = [list(map(int, line)) for line in data.strip().split("\n")]
    return lines

def solve_challenge_a(data, steps):
    data = parse_data(data)
    return challenge_a(data, steps)

challenge_test_data = \
"""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

assert solve_challenge_a(challenge_test_data, 100) == 1656

"""
It seems like the individual flashes aren't bright enough to navigate. However,
you might have a better option: the flashes seem to be synchronizing!

In the example above, the first time all octopuses flash simultaneously is step
195:

After step 193:
5877777777
8877777777
7777777777
7777777777
7777777777
7777777777
7777777777
7777777777
7777777777
7777777777

After step 194:
6988888888
9988888888
8888888888
8888888888
8888888888
8888888888
8888888888
8888888888
8888888888
8888888888

After step 195:
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000
0000000000

If you can calculate the exact moments when the octopuses will all flash
simultaneously, you should be able to navigate through the cavern. What is the
first step during which all octopuses flash?
"""


def challenge_b(data):
    octopuses = init_octopuses(data)

    step = 0
    while True:
        step += 1

        tick_octopuses(octopuses)

        # check sync flashes
        sync = True
        for i in range(len(octopuses)):
            for j in range(len(octopuses[i])):
                if not octopuses[i][j].flashed:
                    sync = False
            
        if sync:
            return step

        reset_flashes(octopuses)

def solve_challenge_b(data):
    data = parse_data(data)
    return challenge_b(data)

assert solve_challenge_b(challenge_test_data) == 195

if __name__ == "__main__":
    DAY = 11
    puzzle_a(DAY, lambda x: solve_challenge_a(x, 100)) # 1785 
    puzzle_b(DAY, solve_challenge_b) # 354
