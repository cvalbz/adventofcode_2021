"""
These caves seem to be lava tubes. Parts are even still volcanically active;
small hydrothermal vents release smoke into the caves that slowly settles
like rain.

If you can model how the smoke flows through the caves, you might be able to
avoid it and be that much safer. The submarine generates a heightmap of the
floor of the nearby caves for you (your puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the
following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the
highest and 0 is the lowest a location can be.

Your first goal is to find the low points - the locations that are lower than
any of its adjacent locations. Most locations have four adjacent locations
(up, down, left, and right); locations on the edge or corner of the map have
three or two adjacent locations, respectively. (Diagonal locations do not count
as adjacent.)

In the above example, there are four low points, all highlighted: two are in
the first row (a 1 and a 0), one is in the third row (a 5), and one is in the
bottom row (also a 5). All other locations on the heightmap have some lower
adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the
risk levels of the low points are 2, 1, 6, and 6. The sum of the risk levels
of all low points in the heightmap is therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points on your heightmap?
"""

from utils import read_input_data, puzzle_a, puzzle_b

def challenge_a(smokes):
    s = 0
    lowpoints = []

    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    for i in range(len(smokes)):
        for j in range(len(smokes[i])):
            is_lowpoint = True

            for ix, jx in directions:
                neigh_i, neigh_j = i + ix, j + jx

                if neigh_i < 0 or neigh_i >= len(smokes) or neigh_j < 0 or neigh_j >= len(smokes[i]):
                    continue
                
                if smokes[neigh_i][neigh_j] <= smokes[i][j]:
                    is_lowpoint = False

            if is_lowpoint:
                s += smokes[i][j] + 1
                lowpoints.append((i, j))

    return s, lowpoints

def parse_data(data):
    lines = [list(map(int, line)) for line in data.strip().split("\n")]
    return lines

def solve_challenge_a(data):
    smokes = parse_data(data)
    return challenge_a(smokes)[0]

challenge_test_data = \
"""
2199943210
3987894921
9856789892
8767896789
9899965678
"""

assert solve_challenge_a(challenge_test_data) == 15

"""
Next, you need to find the largest basins so you know what areas are most
important to avoid.

A basin is all locations that eventually flow downward to a single low point.
Therefore, every low point has a basin, although some basins are very small.
Locations of height 9 do not count as being in any basin, and all other
locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the
low point. The example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678
The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678
The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678
Find the three largest basins and multiply their sizes together. In the above
example, this is 9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?
"""

def get_neighs(smokes, i, j):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for ix, jx in directions:
        neigh_i, neigh_j = i + ix, j + jx

        if neigh_i < 0 or neigh_i >= len(smokes) or neigh_j < 0 or neigh_j >= len(smokes[i]):
            continue

        yield neigh_i, neigh_j

def get_basin(smokes, position, visited):
    i, j = position

    if (i, j) not in visited and smokes[i][j] != 9:
        visited.add((i, j))
        for neigh_i, neigh_j in get_neighs(smokes, i, j):
            if smokes[neigh_i][neigh_j] > smokes[i][j]:
                get_basin(smokes, (neigh_i, neigh_j), visited)

    return visited

def challenge_b(smokes):
    _, lowpoints = challenge_a(smokes)
    sizes = sorted([get_basin(smokes, i, set()) for i in lowpoints],
                    key=lambda s: len(s), reverse=True)

    result = 1
    for s in sizes[:3]:
        result *= len(s)

    return result

def solve_challenge_b(data):
    smokes = parse_data(data)
    return challenge_b(smokes)

assert solve_challenge_b(challenge_test_data) == 1134

if __name__ == "__main__":
    DAY = 9
    puzzle_a(DAY, solve_challenge_a) # 502
    puzzle_b(DAY, solve_challenge_b) # 1330560 
