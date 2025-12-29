from logging import getLogger
from pathlib import Path
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()


def main():
    # Keep track of the beams
    beams = set()
    splits = 0

    line_generator = read_input(Path(__file__).parent / "input.txt")
    start = next(line_generator).strip()
    beams.add(start.index("S"))

    # Iterate through the manifold
    for line in line_generator:
        # Create a clean copy so we don't mutate our iterator
        beams_copy = beams.copy()

        # At each stage, progress the beams
        for beam_idx in beams_copy:
            # If we hit a splitter
            if line[beam_idx] == "^":
                beams.remove(beam_idx)
                beams.add(beam_idx - 1)
                beams.add(beam_idx + 1)
                splits += 1

    logger.info(f"There are a total of {splits} splits.")


if __name__ == "__main__":
    main()
