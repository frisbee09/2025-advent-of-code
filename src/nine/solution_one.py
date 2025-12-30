from logging import getLogger
from pathlib import Path
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()


def get_area(c1: tuple[int, int], c2: tuple[int, int]):
    delta_x = 1 + abs(c1[0] - c2[0])
    delta_y = 1 + abs(c1[1] - c2[1])
    return delta_x * delta_y


def main():
    red_coords = []
    line_generator = read_input(Path(__file__).parent / "input.txt")
    # line_generator = read_input(Path(__file__).parent / "test_input.txt")
    for line in line_generator:
        red_coords.append(tuple(int(x) for x in line.strip().split(",")))

    logger.info(red_coords)

    areas = [
        get_area(c1, c2)
        for l_idx, c1 in enumerate(red_coords)
        for r_idx, c2 in enumerate(red_coords)
        if l_idx != r_idx
    ]

    answer = sorted(areas)[-1]

    logger.info(f"The largest possible area is {answer}")


if __name__ == "__main__":
    main()
