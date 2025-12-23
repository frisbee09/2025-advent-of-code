from math import floor
from config.logging import configure_logging

configure_logging()

from pathlib import Path
from logging import getLogger

logger = getLogger()

from one.solution_one import (
    HIGHEST_VALUE,
    STARTING_VALUE,
    handle_instruction,
    read_input,
)


def main():
    position = STARTING_VALUE
    password = 0
    for line in read_input():
        result = handle_instruction(position, line)
        bound_result = result % 100

        # Perform a more in-depth password calc
        password_contribution = floor(abs(result) / 100)

        # Check if we have crossed 0
        if position != 0 and result <= 0:
            # Add 1 for crossing into the negative
            password_contribution += 1

        password += password_contribution
        if password_contribution > 1 or result == 0:
            logger.info(
                f"Starting at {position}, we rotate {line.strip()} to point at {bound_result} ({result}) contributing {password_contribution}."
            )
        # Not quite so important now, but the logic assumes we are between
        # 0 and 100 (e.g. crossing 0)
        position = bound_result

    logger.info(f"Password: {password}")


if __name__ == "__main__":
    main()
