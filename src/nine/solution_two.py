from logging import getLogger
from pathlib import Path
from typing import TypedDict
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()


def get_area(c1: tuple[int, int], c2: tuple[int, int]):
    delta_x = 1 + abs(c1[0] - c2[0])
    delta_y = 1 + abs(c1[1] - c2[1])
    return delta_x * delta_y


class Edge(TypedDict):
    edge_axis: int
    at: int
    span_axis: int
    span_from: int
    span_to: int


def get_edge(c1: tuple[int, int], c2: tuple[int, int]) -> Edge:
    # Figure out which edge it is, this represents the idx of the number in the tuple
    # 0 for "column" and 1 for "row"
    edge_axis = 0 if c1[0] - c2[0] == 0 else 1
    at = c1[edge_axis]

    # Get an accessor for the "other" axis
    span_axis = 1 - edge_axis

    from_idx = min(c1[span_axis], c2[span_axis])
    to_idx = max(c1[span_axis], c2[span_axis])

    return {
        "edge_axis": edge_axis,
        "at": at,
        "span_axis": span_axis,
        "span_from": from_idx,
        "span_to": to_idx,
    }


def check_intersection(c1: tuple[int, int], c2: tuple[int, int], edge: Edge):
    # Iterate through the edges and check for intersections

    if logger.level == "DEBUG":
        edge_in_range = c1[edge["edge_axis"]] < edge["at"] < c2[edge["edge_axis"]]
        starts_in_shape = (
            c1[edge["span_axis"]] <= edge["span_from"] <= c2[edge["span_axis"]]
        )
        ends_in_shape = (
            c1[edge["span_axis"]] <= edge["span_to"] <= c2[edge["span_axis"]]
        )

        logger.debug(
            f"\n\nEdge {edge} \n"
            f"is {'not ' if not edge_in_range else ''}in range \n"
            f"{'and starts' if starts_in_shape else 'and ends' if ends_in_shape else 'but is not'} in the shape \n"
            f"formed by {c1} - {c2}"
        )

    return (
        # Check to see if the edge is somewhere in the bounds of the rectangle
        # We use strict inequality since we don't care if the edge is the edge of the rect
        c1[edge["edge_axis"]] < edge["at"] < c2[edge["edge_axis"]]
        and
        # The edge is defined within the range of the shape.
        # But is it also in range from the other direction?
        (
            edge["span_to"] > c1[edge["span_axis"]]
            and edge["span_from"] < c2[edge["span_axis"]]
        )
    )


def main():
    red_coords = []
    line_generator = read_input(Path(__file__).parent / "input.txt")
    # line_generator = read_input(Path(__file__).parent / "test_input.txt")
    for line in line_generator:
        red_coords.append(tuple(int(x) for x in line.strip().split(",")))

    edges = []
    prev_x, prev_y = red_coords[-1]
    for x, y in red_coords:
        e = get_edge((x, y), (prev_x, prev_y))
        edges.append(e)
        prev_x, prev_y = x, y

    def check_intersections(c1, c2):
        zipped = list(zip(c1, c2))
        mins = tuple(min(x) for x in zipped)
        maxs = tuple(max(x) for x in zipped)
        for e in edges:
            if check_intersection(mins, maxs, e) is True:
                return True

        return False

    areas = [
        get_area(c1, c2)
        for c1 in red_coords
        for c2 in red_coords
        if check_intersections(c1, c2) is False
    ]
    answer = max(areas)

    logger.info(f"The largest possible area is {answer}")


if __name__ == "__main__":
    main()
