from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


def read_input(input_path: Path | str):
    logger.info(f"Using {input_path}")
    with open(input_path) as f:
        for line in f:
            yield line
