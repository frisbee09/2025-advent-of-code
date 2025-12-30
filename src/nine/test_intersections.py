from json import dumps
from logging import getLogger
from util.input import read_input
from util.logging import configure_logging

configure_logging("DEBUG")
logger = getLogger()


from nine.solution_two import check_intersection, Edge, get_edge

test_rect = (
    (3, 5),
    (10, 10),
)
edge_coords = [
    # Outside the range (no intersect)
    [(15, 2), (15, 8)],
    # Overlaps the bottom edge (intersect)
    [(6, 8), (6, 12)],
    # Hugs the top corner edge (no intersect)
    [(3, 5), (8, 5)],
    # Is entirely inside the shape (intersect)
    [(4, 6), (10, 6)],
    # Starts and ends on the top edge of the rect (no intersect)
    [(3, 5), (10, 5)],
    # Starts and ends through the middle (intersect)
    [(3, 7), (10, 7)],
    # Starts before, finishes after, but goes straight through (intersect)
    [(2, 7), (11, 7)],
]


def main():
    test_edges = [get_edge(*c) for c in edge_coords]
    logger.info(dumps(test_edges, indent=2))

    is_ok = [
        check_intersection(test_rect[0], test_rect[1], edge) for edge in test_edges
    ]

    assert is_ok == [False, True, False, True, False, True, True]


if __name__ == "__main__":
    main()
