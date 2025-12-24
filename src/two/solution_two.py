from functools import reduce
from math import floor
import operator
import re
from two.solution_one import get_ranges_from_line
from util.logging import configure_logging
from logging import getLogger

configure_logging()
logger = getLogger()


from pathlib import Path
from util.input import read_input


def check_number(num: int):
    """
    We first try and cheaply throw away any obviously not-pattern-matching
    values, using string iteration instead of numeric iteration
    """
    as_str = str(num)

    # We remove the even-length check since the new problem definition
    # invalidates this constraint

    hash = {}

    # The cheapest thing to do it iterate over figures
    for char in as_str:
        hash.setdefault(char, 0)
        # Count character instances
        hash[char] += 1

    # We can't check for even counts any more, since the contraints have
    # changed.

    # Instead, find the smallest number. It *must* be bigger than one.
    least_reoccurance = min(hash.values())
    if least_reoccurance == 1:
        return False

    length = len(as_str)
    # If the length of the string isn't a multiple of least_reoccurance we can't
    # meet criteria
    if length % least_reoccurance != 0:
        return False

    # Least re-occurance tells us *how many times* the pattern repeats.
    # If any other re-occurance is not a multiple of this, it's not got the right makeup
    if any([val % least_reoccurance != 0 for val in hash.values()]):
        return False

    substr_length = int(length / least_reoccurance)
    substr = as_str[:substr_length]

    # If we remove all instances of the substring we should get an empty string
    # if the number is the right pattern
    return as_str.replace(substr, "") == ""


REGEX_TEMPLATE = r"([0-9]+)"


def check_number_with_backreferences(num: int):
    as_str = str(num)
    length = len(as_str)
    hash = {}

    # The cheapest thing to do it iterate over figures
    for char in as_str:
        hash.setdefault(char, 0)
        # Count character instances
        hash[char] += 1

    least_reoccurance = min(hash.values())
    if least_reoccurance == 1:
        return False

    for substr_length in range(1, floor(length / 2) + 1):
        recurrance = floor(length / substr_length)
        pattern = (
            r"^([0-9]{" + str(substr_length) + r"})" + (r"\1" * (recurrance - 1)) + "$"
        )
        subbed = re.sub(pattern, "", as_str)
        if len(subbed) == 0:
            return True

    return False


# Some values to try and optimise Result cache - where a number has ended up
# at the end of it's assessment, to prevent calculating twice
RESULT_CACHE = dict()
FAKE_IDS = []

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


def process_range(range: str):
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

        if check_number_with_backreferences(current) is False:
            RESULT_CACHE[current] = False
        else:
            RESULT_CACHE[current] = True
            fake_found.append(current)

        current += 1

    logger.info(
        f"{range[0]}-{range[1]} has {len(fake_found)} invalid IDs: {fake_found}"
    )
    for id in fake_found:
        FAKE_IDS.append(id)


def main():
    ranges = []
    for line in read_input(Path(__file__).parent / "test_input.txt"):
    # for line in read_input(Path(__file__).parent / "input.txt"):
        ranges.extend(get_ranges_from_line(line.strip()))

    for range in ranges:
        process_range(range)

    sum = reduce(operator.add, FAKE_IDS, 0)
    logger.info(f"Adding up all the invalid IDs produces {sum}")


if __name__ == "__main__":
    main()
