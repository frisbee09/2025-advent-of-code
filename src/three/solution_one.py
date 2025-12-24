from logging import getLogger
from pathlib import Path
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()


def get_largest_jolt(bank: str):
    bank_it = [int(n) for n in bank.strip()]
    max_tens = max(bank_it[:-1])
    earliest_instance = bank_it.index(max_tens)
    max_units = max(bank_it[(earliest_instance + 1) :])
    return int(str(max_tens) + str(max_units))


def main():
    joltage = 0
    # for line in read_input(Path(__file__).parent / "test_input.txt"):
    for line in read_input(Path(__file__).parent / "input.txt"):
        joltage += get_largest_jolt(line)

    logger.info(f"Max joltage: {joltage}")


if __name__ == "__main__":
    main()
