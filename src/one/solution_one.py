from config.logging import configure_logging

configure_logging()

from pathlib import Path
from logging import getLogger

logger = getLogger()


def read_input():
    input_path = Path(__file__).parent / "input.txt"
    logger.info(f"Using {input_path}")
    with open(input_path) as f:
        for line in f:
            yield line


STARTING_VALUE = 50
PASSWORD_VALUE = 0
HIGHEST_VALUE = 100


def handle_instruction(curr: int, instruction: str):
    clean = instruction.strip()
    LR = clean[0]
    num = int(clean[1:])
    result = curr
    if LR == "L":
        result = result - num
    elif LR == "R":
        result = result + num

    return result


def main():
    position = STARTING_VALUE
    password = 0
    for line in read_input():
        position = handle_instruction(position, line)
        position = position % HIGHEST_VALUE

        logger.info(f"The dial is rotated {line.strip()} to point at {position}.")
        if position == 0:
            password += 1

    logger.info(f"Password: {password}")


if __name__ == "__main__":
    main()
