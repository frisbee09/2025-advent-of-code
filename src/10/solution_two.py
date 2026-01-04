import copy
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from itertools import combinations, product
from logging import getLogger
from math import ceil, floor, isclose
from operator import add
import operator
from pathlib import Path
import re
from util.input import read_input
from util.logging import configure_logging


configure_logging("DEBUG")
logger = getLogger()

INPUT_REGEX = r"\[([.#]+)\] ((\([0-9,]*\) )*)\{([0-9,]*)\}"


def get_rref(m: list[list[int]]):
    matrix = copy.deepcopy(m)
    pivot_row = 0
    pivot_col = 0
    while pivot_row < len(matrix) and pivot_col < len(matrix[0]) - 1:
        pivot_idx, pivot = next(
            (
                (row_idx, row)
                for row_idx, row in enumerate(matrix)
                if row_idx >= pivot_row and row[pivot_col] != 0
            ),
            (None, None),
        )
        # This column is not a pivot column. Go to the next one
        if pivot is None:
            pivot_col += 1
            continue

        # If the row we find is not in the right position, swap it
        if pivot_idx != pivot_row:
            # Swap!
            matrix[pivot_idx], matrix[pivot_row] = matrix[pivot_row], matrix[pivot_idx]

        # Normalise the pivot row
        pivot_scalar = matrix[pivot_row][pivot_col]
        if pivot_scalar != 0:
            matrix[pivot_row] = [Fraction(x / pivot_scalar) for x in pivot]
            pivot = matrix[pivot_row]

        for row_idx, row in enumerate(matrix):
            if row_idx == pivot_row:
                continue

            if row[pivot_col] != 0:
                # Eliminate by subtracting the pivot
                scalar = Fraction(row[pivot_col] / pivot[pivot_col])
                matrix[row_idx] = [x - (scalar * y) for x, y in zip(row, pivot)]

        pivot_row += 1
        pivot_col += 1

    return matrix


def analyse_rref(aug_m: list[list[int]]):
    if any(all(x == 0 for x in row[:-1]) and row[-1] != 0 for row in aug_m):
        raise ValueError(
            f"Issue with aug_m. Row suggests no solution to the problem. \n\n {'\n'.join(','.join(row) for row in aug_m)}"
        )

    T = [list(a) for a in zip(*aug_m)]

    pivot_rows_by_column = {
        next(idx for idx, val in enumerate(row) if val != 0): row_idx
        for row_idx, row in enumerate(aug_m)
        if any(x != 0 for x in row)
    }

    # Num variables - rank
    num_frees = (
        len(T) - 1 - sum([1 if any(x != 0 for x in row) else 0 for row in aug_m])
    )
    free_idxs = [idx for idx in range(len(T) - 1) if idx not in pivot_rows_by_column]
    gen_solution = [[0] * (len(T) - 1) for _ in range(num_frees + 1)]

    for col_idx, col in enumerate(T[:-1]):
        if col_idx not in pivot_rows_by_column:
            # We are a free column!
            gen_solution[0][col_idx] = 0
            for i in range(1, len(gen_solution)):
                gen_solution[i][col_idx] = 1 if free_idxs[i - 1] == col_idx else 0
        else:
            row_index = pivot_rows_by_column[col_idx]
            gen_solution[0][col_idx] = aug_m[row_index][-1]
            for i in range(1, len(gen_solution)):
                free_col_idx = free_idxs[i - 1]
                gen_solution[i][col_idx] = aug_m[row_index][free_col_idx] * -1

    return gen_solution


def make_int_range(low, high):
    lo = int(ceil(float(low)))
    hi = int(floor(float(high)))
    if lo <= hi:
        return range(lo, hi + 1)
    else:
        return range(lo, hi - 1, -1)


def find_min_solution(gen_solution: list[list[int | Fraction]]):
    particular = gen_solution[0]
    frees = gen_solution[1:]

    if len(frees) == 0:
        # There is only one solution
        return sum(particular)

    # Use something akin to partial differentiation to understand the
    # coefficient ranges if we consider them to be linearly independent
    coeff_ranges = []
    for free_vector in frees:
        mins = [0]
        maxes = []
        for idx, v in enumerate(free_vector):
            if v < 0:
                maxes.append(Fraction(particular[idx] / (-1 * v)))
            elif v > 0:
                mins.append(Fraction(particular[idx] / (-1 * v)))

        coeff_ranges.append((max(mins), min(maxes)))

    # This should be a very small solution space now
    # In fact, if the number of frees is 1, we can analytically find the
    # min_solution. However, for simplicity I am going to implement a general
    # case algo which is less efficient for len(coeff_ranges) == 1

    coeff_ranges_as_ints = [make_int_range(low, high) for low, high in coeff_ranges]
    costs = []
    for combo in product(*coeff_ranges_as_ints):
        coeffs = [1, *combo]
        scaled_vectors = [
            [x * scal for x in vec] for vec, scal in zip(gen_solution, coeffs)
        ]
        final_vector = [sum(a) for a in zip(*scaled_vectors)]
        if all(x >= 0 and round(x) == x for x in final_vector):
            costs.append(sum(final_vector))
        else:
            logger.debug("Not a viable solution")
            continue

    return min(costs)


class Machine:
    # Puzzle properties
    target: list[int]
    buttons: list[list[int]]
    joltages: list[int]

    # Solution state tracking
    num_presses: int
    num_frees: int

    def parse_puzzle(self, puzzle_input: str):
        parsed = re.match(INPUT_REGEX, puzzle_input)
        gs = parsed.groups()

        self.target = list(0 if x == "." else 1 for x in gs[0])

        self.buttons = []
        for b in gs[1].strip().split(" "):
            parsed_button = set(
                int(x) for x in re.sub(r"[\(\)]", "", b).split(",") if x != ""
            )
            button = list(
                1 if _ in parsed_button else 0 for _ in range(len(self.target))
            )
            self.buttons.append(button)

        self.joltages = tuple(int(x) for x in gs[3].split(","))

    def __init__(self, puzzle_input: str):
        self.parse_puzzle(puzzle_input)
        self.solution = None
        self.num_presses = None

    def solve(self):
        aug_matrix = [list(x) for x in zip(*self.buttons, self.joltages)]
        rref = get_rref(aug_matrix)
        gen_solution = analyse_rref(rref)

        self.num_frees = len(gen_solution) - 1
        # self.num_presses = find_min_solution(gen_solution)
        self.num_presses = 0

        # logger.info(f"The minimum solution is {self.num_presses} moves.")
        return self.num_presses


def main():
    line_generator = read_input(Path(__file__).parent / "input.txt")
    # line_generator = read_input(Path(__file__).parent / "test_input.txt")
    machines: list[Machine] = []

    for line in line_generator:
        m = Machine(line)
        machines.append(m)

    for machine in machines:
        machine.solve()

    logger.debug(f"Most frees needed to handle = {max(m.num_frees for m in machines)}.")
    answer = reduce(
        operator.add,
        [m.num_presses for m in machines if m.num_presses is not None],
    )
    logger.info(f"The answer is: {answer}")


if __name__ == "__main__":
    # import cProfile, pstats, io
    # from pstats import SortKey

    # pr = cProfile.Profile()
    # pr.enable()
    # main()
    # pr.disable()
    # s = io.StringIO()
    # sortby = SortKey.CUMULATIVE
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # logger.info(s.getvalue())

    main()
