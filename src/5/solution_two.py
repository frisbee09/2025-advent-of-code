from logging import getLogger
from pathlib import Path
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()


def optimise_ranges(ranges: list[tuple[int, int]]):
    # Sort the ranges by the lower bounds
    sorted_ranges = sorted(ranges, key=(lambda x: x[0]))

    # Create a set to reduce the ranges
    reduced_ranges = {}

    # Variables to store where we are in the ranges
    current_lower, current_higher = sorted_ranges[0]

    # Iterate through the sorted ranges
    for lower, upper in sorted_ranges[1:]:
        # We know each lower is bigger than the last
        # The main question is, is the lower bound overlapping?
        if lower <= current_higher:
            # If the upper extends the range, we tack on the additional numbers
            current_higher = max(upper, current_higher)

        else:
            # The range does NOT overlap. So, flush the current values into the reduced set
            reduced_ranges[current_lower] = current_higher

            # Reinitialise the current range we are focussing on
            current_lower = lower
            current_higher = upper

    # A final flush
    reduced_ranges[current_lower] = current_higher

    return reduced_ranges


def parse_range(line: str):
    lower, higher = (int(x) for x in line.split("-"))

    return lower, higher


def parse_id(ranges, id):
    l, h = next(((l, h) for l, h in ranges.items() if (l <= id <= h)), (None, None))
    logger.info(f"ID {id} in range {l}-{h}")
    if l is not None:
        return 1
    else:
        return 0


def main():
    ranges_from_input = []
    parse_mode = "ranges"
    handlers = {"ranges": parse_range, "ids": parse_id}
    line_generator = read_input(Path(__file__).parent / "input.txt")
    for line in line_generator:
        if line.strip() == "":
            break
        l, h = parse_range(line.strip())
        ranges_from_input.append((l, h))

    reduced_ranges = optimise_ranges(ranges_from_input)

    count = 0
    for l, h in reduced_ranges.items():
        count += h - l + 1

    # logger.info(fresh_id_ranges)
    logger.info(f"There are {count} fresh IDs")


if __name__ == "__main__":
    main()
