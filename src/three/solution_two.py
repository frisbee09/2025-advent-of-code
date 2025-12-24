from logging import getLogger
from pathlib import Path
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()

NUM_TO_TURN_ON = 12


def get_largest_jolt(bank: str):
    bank_it = [int(n) for n in bank.strip()]
    num = ""
    current_search_idx = 0
    for battery_idx in range(-11, 1):
        search_list = (
            bank_it[current_search_idx:battery_idx]
            if battery_idx < 0
            else bank_it[current_search_idx:]
        )
        digit = max(search_list)
        num += str(digit)
        current_search_idx += 1 + bank_it[current_search_idx:].index(digit)

    return int(num)


def main():
    joltage = 0
    joltages = []
    # for line in read_input(Path(__file__).parent / "test_input.txt"):
    for line in read_input(Path(__file__).parent / "input.txt"):
        j = get_largest_jolt(line.strip())
        joltage += j
        joltages.append(j)

    logger.info(f"Max joltage: {joltage}")
    logger.info(",".join(str(j) for j in joltages))


if __name__ == "__main__":
    main()
