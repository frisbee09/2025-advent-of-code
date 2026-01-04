import copy
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from itertools import combinations
from logging import getLogger
from math import isclose
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
        if pivot is None:
            pivot_col += 1
            continue

        if pivot_idx != pivot_row:
            # Swap!
            matrix[pivot_idx], matrix[pivot_row] = matrix[pivot_row], matrix[pivot_idx]

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
                gen_solution[i][col_idx] = aug_m[row_index][col_idx] * -1

    return gen_solution


def find_min_solution(gen_solution: list[list[int | Fraction]]):
    particular = gen_solution[0]
    frees = gen_solution[1:]

    if len(frees) == 0:
        # There is only one solution
        return sum(particular)

    best_cost = float("inf")

    # We are doing nCp where n is the number of variables (length of the
    # particular vector) and p is the number of free variables

    for indicies_to_zero in combinations(range(len(particular)), len(frees)):
        # We now take those rows and set them to 0, creating a smaller system
        # e.g. P[i] + SUM(cx*vx[i]) = 0
        vx = [[vec[row_idx] for vec in frees] for row_idx in indicies_to_zero]
        P = [particular[row_idx] * -1 for row_idx in indicies_to_zero]
        aug_m = [[*vx[i], P[i]] for i in range(len(vx))]
        rref = get_rref(aug_m)
        cx = [r[-1] for r in rref]

        solution_is_valid = False
        impossible_row = any(
            (all(x == 0 for x in row[:-1]) and row[-1] != 0) for row in rref
        )
        no_negs = all(c >= 0 for c in cx)
        all_ints = all(round(c) == c for c in cx)

        if not impossible_row and no_negs and all_ints:
            solution_is_valid = True

        if solution_is_valid:
            all_scalars = [1, *cx]
            final_vectors = [
                [x * scalar for x in vec]
                for vec, scalar in zip(gen_solution, all_scalars)
            ]
            final_vector = [sum(x) for x in zip(*final_vectors)]

            no_negs = all(v >= 0 for v in final_vector)
            all_ints = all(round(v) == v for v in final_vector)

            if no_negs and all_ints:
                solution_is_valid = True
            else:
                solution_is_valid = False

            if solution_is_valid:
                best_cost = min(best_cost, sum(final_vector))

    return best_cost


class Machine:
    # Puzzle properties
    target: list[int]
    buttons: list[list[int]]
    joltages: list[int]

    # Solution state tracking
    num_presses: int

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

    def solve(self):
        aug_matrix = [list(x) for x in zip(*self.buttons, self.joltages)]
        rref = get_rref(aug_matrix)
        gen_solution = analyse_rref(rref)

        self.num_presses = find_min_solution(gen_solution)

        return self.num_presses


def main():
    # line_generator = read_input(Path(__file__).parent / "input.txt")
    line_generator = read_input(Path(__file__).parent / "test_input.txt")
    machines: list[Machine] = []

    for line in line_generator:
        m = Machine(line)
        machines.append(m)

    for idx, machine in enumerate(machines):
        machine.solve()

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
