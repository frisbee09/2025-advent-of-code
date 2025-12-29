from logging import getLogger
from pathlib import Path
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()


def main():
    # Beams are no longer collapsing if they share an index
    timelines = 1

    line_generator = read_input(Path(__file__).parent / "input.txt")
    start = next(line_generator).strip()
    beams = {idx: 0 for idx in range(len(start))}
    beams[start.index("S")] += 1

    # Iterate through the manifold
    for line in line_generator:
        # Create a clean copy so we don't mutate our iterator
        beams_copy = beams.copy()

        # At each stage, progress the beams
        for beam_idx, num in beams_copy.items():
            # If we hit a splitter
            if line[beam_idx] == "^":
                beams[beam_idx] = 0
                # The number of timelines increases by the number of beams
                # currently occupying the index, x2
                timelines += num
                beams[beam_idx - 1] += num
                beams[beam_idx + 1] += num

    logger.info(f"There are a total of {timelines} timelines.")


if __name__ == "__main__":
    main()
