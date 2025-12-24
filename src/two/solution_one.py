from functools import reduce
from math import floor
import operator
from util.logging import configure_logging
from logging import getLogger

configure_logging()
logger = getLogger()


from pathlib import Path
from util.input import read_input


def sieve_for_even_counts(num: int):
    """
    We first try and cheaply throw away any obviously not-pattern-matching
    values, using string iteration instead of numeric iteration
    """
    as_str = str(num)

    if len(as_str) % 2 > 0:
        # This means the number is of an odd length and can't possibly be 2x
        # numeric instances. I could do this on the max/min ranges as well but
        # this is currently performing well enough.
        return False

    hash = {}

    # The cheapest thing to do it iterate over figures
    for char in as_str:
        hash.setdefault(char, 0)
        # Count character instances
        hash[char] += 1

    # If any character count is odd, it fails the check
    if any([val % 2 > 0 for val in hash.values()]):
        return False

    return True


def get_ranges_from_line(input: str):
    ranges = [x for x in input.split(",") if x != ""]
    numeric_tuples = []
    for range in ranges:
        split = range.split("-")
        numeric_tuples.append((int(split[0]), int(split[1])))
    return numeric_tuples


# Some values to try and optimise Result cache - where a number has ended up
# at the end of it's assessment, to prevent calculating twice
RESULT_CACHE = dict()
FAKE_IDS = set()

# A set of candidates, to collapse any overlapping ranges
CANDIDATES = set()

# All values, for debugging and stats calc
ALL_VALUES = []


# A cache checker
def check_cache(num: int):
    if num in RESULT_CACHE:
        return RESULT_CACHE[num]
    else:
        return None


def simple_halfway_check(num: int):
    as_str = str(num)
    midpoint = floor(len(as_str) / 2)
    return as_str[:midpoint] == as_str[midpoint:]


def process_range(range: str):
    initial = range[0]
    current = range[0]
    fake_found: list[int] = []

    # Iterate through the raw ranges
    while current <= range[1]:
        # Append the value for tracking
        ALL_VALUES.append(current)

        # Check the cache for a result, potentially skipping the sieve if
        # we've seen it before
        cached_value = check_cache(current)
        if cached_value is not None:
            return cached_value

        if (
            sieve_for_even_counts(current) is False
            or simple_halfway_check(current) is False
        ):
            RESULT_CACHE[current] = False
        else:
            RESULT_CACHE[current] = True
            fake_found.append(current)

        current += 1

    logger.info(
        f"{range[0]}-{range[1]} has {len(fake_found)} invalid IDs: {fake_found}"
    )
    for id in fake_found:
        FAKE_IDS.add(id)


def main():
    ranges = []
    for line in read_input(Path(__file__).parent / "input.txt"):
        ranges.extend(get_ranges_from_line(line.strip()))

    for range in ranges:
        process_range(range)

    sum = reduce(operator.add, FAKE_IDS, 0)
    logger.info(f"Adding up all the invalid IDs produces {sum}")


if __name__ == "__main__":
    main()
