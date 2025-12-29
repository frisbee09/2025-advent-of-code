from logging import getLogger
from pathlib import Path
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()


def main():
    # line_generator = read_input(Path(__file__).parent / "input.txt")
    line_generator = read_input(Path(__file__).parent / "test_input.txt")
    for line in line_generator:
        print(line)


if __name__ == "__main__":
    main()
