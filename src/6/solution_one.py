from functools import reduce
from logging import getLogger
import operator
from pathlib import Path
from util.input import read_input
from util.logging import configure_logging


configure_logging("DEBUG")
logger = getLogger()


def main():
    puzzle_matrix = []
    for line in read_input(Path(__file__).parent / "input.txt"):
        nums = [x.strip() for x in line.strip().split(" ") if x.strip() != ""]
        puzzle_matrix.append(nums)

    puzzle_cols = zip(*puzzle_matrix)

    sum = 0
    for col in puzzle_cols:
        op_to_perform = operator.add if col[-1] == "+" else operator.mul

        result = reduce(op_to_perform, [int(x) for x in col[:-1]])
        logger.debug(result)
        sum += result

    logger.info(f"The checksum for the worksheet is {sum}")


if __name__ == "__main__":
    main()
