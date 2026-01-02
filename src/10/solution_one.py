import copy
from dataclasses import dataclass
from functools import reduce
from logging import getLogger
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
                if row_idx >= pivot_row and row[pivot_col] == 1
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

            if row[pivot_col] == 1:
                # Eliminate by subtracting the pivot
                matrix[row_idx] = [x ^ y for x, y in zip(row, pivot)]

        pivot_row += 1
        pivot_col += 1

    return matrix


def analyse_rref(aug_m: list[list[int]]):
    if any(all(x == 0 for x in row[:-1]) and row[-1] == 1 for row in aug_m):
        raise ValueError(
            f"Issue with aug_m. Row suggests no solution to the problem. \n\n {'\n'.join(','.join(row) for row in aug_m)}"
        )

    T = [list(a) for a in zip(*aug_m)]
    pivot_rows_by_column = []
    pivot_col_indexes = [
        next((idx for idx, x in enumerate(row) if x == 1), None) for row in aug_m
    ]
    free_col_indexes = [
        idx for idx in range(len(T[:-1])) if idx not in pivot_col_indexes
    ]

    for col in T[:-1]:
        rev = copy.deepcopy(col)
        rev.reverse()

        pivot_row = next(len(col) - 1 - idx for idx, x in enumerate(rev) if x == 1)
        pivot_rows_by_column.append(pivot_row)

    gen_solution = [[] for _ in range(len(free_col_indexes) + 1)]

    for col_idx in range(len(T) - 1):
        row_to_use = aug_m[pivot_rows_by_column[col_idx]]

        if col_idx in pivot_col_indexes:
            gen_solution[0].append(row_to_use[-1])
            for var_idx, free_column_idx in enumerate(free_col_indexes):
                gen_solution[var_idx + 1].append(row_to_use[free_column_idx])

        else:
            gen_solution[0].append(0)
            for var_idx, free_column_idx in enumerate(free_col_indexes):
                gen_solution[var_idx + 1].append(1 if free_column_idx == col_idx else 0)

    return gen_solution


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
        aug_matrix = [list(x) for x in zip(*self.buttons, self.target)]
        rref = get_rref(aug_matrix)
        gen_solution = analyse_rref(rref)

        free_dims = len(gen_solution) - 1

        logger.debug(f"There are {2 ** free_dims} solutions to compute and analyse")

        solution_weights = []
        for i in range(2**free_dims):
            free_var_values = [(i >> j) & 1 for j in range(free_dims)]

            # Filter the gen_solution vectors depending on whether they are
            # expressed, based upon the bitwise array gen above
            vectors = [
                gen_solution[0],
                *[
                    x
                    for idx, x in enumerate(gen_solution[1:])
                    if free_var_values[idx] == 1
                ],
            ]
            zipped = [list(a) for a in zip(*vectors)]
            final_sol = [reduce((lambda x, y: x ^ y), z) for z in zipped]
            solution_weights.append(sum(final_sol))

        self.num_presses = min(solution_weights)
        return self.num_presses


def main():
    line_generator = read_input(Path(__file__).parent / "input.txt")
    # line_generator = read_input(Path(__file__).parent / "test_input.txt")
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
