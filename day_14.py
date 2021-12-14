"""
--- Day 14: Extended Polymerization ---
The incredible pressures at this depth are starting to put a strain on your
submarine. The submarine has polymerization equipment that would produce
suitable materials to reinforce the submarine, and the nearby volcanically-active
caves should even have the necessary input elements in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer
formula; specifically, it offers a polymer template and a list of pair insertion
rules (your puzzle input). You just need to work out what polymer would result
after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means
that when elements A and B are immediately adjacent, element C should be inserted
between them. These insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously
considers all three pairs:

The first pair (NN) matches the rule NN -> C, so element C is inserted between
the first N and the second N.
The second pair (NC) matches the rule NC -> B, so element B is inserted between
the N and the C.
The third pair (CB) matches the rule CB -> H, so element H is inserted between
the C and the B.
Note that these pairs overlap: the second element of one pair is the first
element of the next pair. Also, because all pairs are considered simultaneously,
inserted elements are not considered to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB
This polymer grows quickly. After step 5, it has length 97; After step 10, it
has length 3073. After step 10, B occurs 1749 times, C occurs 298 times, H
occurs 161 times, and N occurs 865 times; taking the quantity of the most common
element (B, 1749) and subtracting the quantity of the least common element
(H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and
least common elements in the result. What do you get if you take the quantity
of the most common element and subtract the quantity of the least common
element?
"""

from utils import read_input_data, puzzle_a, puzzle_b
from collections import defaultdict, Counter

def replace(template, rules):
    expanded_template = defaultdict(int)
    for polymer, count in template.items():
        new = rules[polymer]

        expanded_template[polymer[0] + new] += count
        expanded_template[new + polymer[1]] += count
    
    return expanded_template

def challenge_a(template, rules, steps):
    template_orig = list(template)
    template_dict = defaultdict(int)

    for i, j in zip(template, template[1:]):
        template_dict[i + j] += 1

    for i in range(steps):
        template_dict = replace(template_dict, rules)

    count = defaultdict(int)
    for k, v in template_dict.items():
        for ch in k:
            count[ch] += v

    # polymer is zip-ed with its tail, adjusting counts
    count[template_orig[0]] += 1
    count[template_orig[-1]] += 1

    for k, v in list(count.items()):
        count[k] = v // 2

    freqs = sorted(count.items(), key=lambda x: x[1])
    return freqs[-1][1] - freqs[0][1]

def parse_data(data):
    lines = [line for line in data.strip().split("\n") if line != ""]
    template = lines[0]
    rules = lines[1:]
    return template, rules

def solve_challenge_a(data, steps):
    template, rules = parse_data(data)

    rules_dict = {}
    for r in rules:
        match, inserted = r.split(" -> ")
        rules_dict[match] = inserted

    return challenge_a(template, rules_dict, steps)

challenge_test_data = \
"""
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""

assert solve_challenge_a(challenge_test_data, 10) == 1588
assert solve_challenge_a(challenge_test_data, 40) == 2188189693529

if __name__ == "__main__":
    DAY = 14
    puzzle_a(DAY, lambda data: solve_challenge_a(data, 10)) # 3095
    puzzle_b(DAY, lambda data: solve_challenge_a(data, 40)) # 3152788426516
