from logging import getLogger
from pathlib import Path
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()


def parse_line(line: str):
    return line.split("")


def get_adjacent_tiles(matrix: list[list[str]], row: int, col: int):
    min_row = max(0, row - 1)
    max_row = min(len(matrix), row + 2)
    row_range = range(min_row, max_row)

    min_col = max(0, col - 1)
    max_col = min(len(matrix[0]), col + 2)
    col_range = range(min_col, max_col)

    return [
        matrix[i][j] for i in row_range for j in col_range if (i != row or j != col)
    ]


def main():
    puzzle_matrix = []
    for line in read_input(Path(__file__).parent / "input.txt"):
        # for line in read_input(Path(__file__).parent / "test_input.txt"):
        puzzle_matrix.append([x for x in line.strip()])

    blank_matrix = [
        [" " for x in range(len(puzzle_matrix[0]))] for x in range(len(puzzle_matrix))
    ]
    accessible_loo_rolls = 0

    for row_idx, row in enumerate(puzzle_matrix):
        for col_idx, char in enumerate(row):
            if char != "@":
                continue

            adjacent_tiles = get_adjacent_tiles(puzzle_matrix, row_idx, col_idx)
            if len([x for x in adjacent_tiles if x == "@"]) < 4:
                accessible_loo_rolls += 1
                blank_matrix[row_idx][col_idx] = "x"

    logger.info(f"There are {accessible_loo_rolls} rolls accessible via forklift.")


if __name__ == "__main__":
    main()
