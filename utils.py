DATA_FOLDER = "./data"

def read_input_data(day: int) -> str:
    """Read this day's input file."""
    if day < 10:
        day_str = f"0{day}"
    else:
        day_str = f"{day}"

    input_data_path = f"{DATA_FOLDER}/day_{day_str}/input.txt"
    with open(input_data_path, 'r') as f:
        return f.read()

def count_from(i):
    while True:
        yield i
        i += 1

def hex_to_bin(data, size=128):
    return bin(int(data, 16))[2:].zfill(size)

def chunks_of(lst, n):
    if len(lst) % n != 0:
        raise Exception("chunks will not have equal length")

    return map(list, zip(*[iter(lst)]*n))

def quantify(iterable, pred=bool):
    "Count how many times the predicate is true."
    return sum(map(pred, iterable))

def transpose(matrix): return tuple(zip(*matrix))

def int_range_incl(a, b):
    return range(a, b + 1) if a < b else range(a, b - 1, -1)

####

def puzzle_a(day, solve_challenge_a):
    data = read_input_data(day)
    print(solve_challenge_a(data))


def puzzle_b(day, solve_challenge_b):
    data = read_input_data(day)
    print(solve_challenge_b(data))

