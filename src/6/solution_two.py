from functools import reduce
from logging import getLogger
import operator
from pathlib import Path
import re
from util.input import read_input
from util.logging import configure_logging


configure_logging("DEBUG")
logger = getLogger()


def get_next_space(line: str):
    scan_idx = None
    while scan_idx != -1:
        try:
            scan_idx = line.index(" ", scan_idx + 1 if scan_idx is not None else None)
            yield scan_idx
        except ValueError:
            scan_idx = -1


def get_next_number(line: str):
    scan_idx = None
    while scan_idx != -1:
        num_match = re.match(
            r"[0-9]", line[(scan_idx + 1 if scan_idx is not None else 0) :]
        )
        if num_match is None:
            scan_idx = -1
        else:
            scan_idx = num_match.start


def trim_puzzles(lines: list[str]):
    mainline = lines[0]
    other_lines = lines[1:]

    scan_idx = 0
    puzzles = []

    for idx in get_next_space(mainline):
        if all(line[idx] == " " for line in other_lines):
            puzzles.append(
                [line[scan_idx : idx + 1].replace("\n", "") for line in lines]
            )
            scan_idx = idx + 1

    # Get the last puzzle
    puzzles.append([line[scan_idx:] for line in lines])

    # scan_idx = 0
    # while True:
    #     next_space_idx = mainline[scan_idx:].index(" ")

    return puzzles


def solve_puzzle(lines: list[str]):
    op = operator.add if lines[-1].strip() == "+" else operator.mul
    pivot = ["".join(i).strip() for i in zip(*lines[:-1])]
    nums = [int(x) for x in pivot if x.strip() != ""]
    nums.reverse()

    return reduce(op, nums)


def main():
    worksheet_lines = []
    for line in read_input(Path(__file__).parent / "input.txt"):
        worksheet_lines.append(line)

    puzzle_cols = trim_puzzles(worksheet_lines)
    sum = 0
    for col in puzzle_cols:
        sum += solve_puzzle(col)

    logger.info(f"The checksum for the worksheet is {sum}")


if __name__ == "__main__":
    main()
