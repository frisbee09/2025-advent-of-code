from functools import reduce
from logging import getLogger
import operator
from pathlib import Path
from uuid import uuid4
from util.input import read_input
from util.logging import configure_logging


configure_logging()
logger = getLogger()


class Junction:
    id: str
    nearest_neighbour_id: str | None
    nearest_neighbour_distance: int | None

    circuit: str | None

    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int):
        self.id = str(uuid4())[:6]
        self.nearest_neighbour_id = None
        self.nearest_neighbour_distance = None
        self.circuit = None

        self.x = x
        self.y = y
        self.z = z

    def distance_from(self, j: Junction):
        return ((self.x - j.x) ** 2 + (self.y - j.y) ** 2 + (self.z - j.z) ** 2) ** 0.5

    def get_nearest_unconnected_neighbour(self, js: list[Junction]):
        for j in js:
            if j.id == self.id or (
                self.circuit is not None and j.circuit == self.circuit
            ):
                continue

            d = self.distance_from(j)
            if self.nearest_neighbour_id is None or d < self.nearest_neighbour_distance:
                self.nearest_neighbour_distance = d
                self.nearest_neighbour_id = j.id


def main():
    # line_generator = read_input(Path(__file__).parent / "input.txt")
    line_generator = read_input(Path(__file__).parent / "test_input.txt")
    j_boxes_by_id: dict[str, Junction] = {}
    circuits: dict[str, set[Junction]] = {}

    logger.info("Reading coords and constructing circuits")

    for line in line_generator:
        x, y, z = (int(i) for i in line.strip().split(","))
        j = Junction(x, y, z)
        j_boxes_by_id[j.id] = j

    logger.info("Connecting the closest ten...")
    total_circuits = len(j_boxes_by_id.keys())
    connections_made = 0

    while connections_made < 10:
        for j in j_boxes_by_id.values():
            j.get_nearest_unconnected_neighbour(j_boxes_by_id.values())

        for j in sorted(
            j_boxes_by_id.values(), key=(lambda j: j.nearest_neighbour_distance)
        ):

            nnb_id = j.nearest_neighbour_id
            nnb = j_boxes_by_id.get(nnb_id)

            if j.circuit is None and nnb.circuit is None:
                # Both are un-attached. We create a new circuit
                circuit_id_to_join = str(uuid4())[:6]
                circuits[circuit_id_to_join] = set([j.id, nnb.id])

            elif j.circuit == nnb.circuit:
                # Both are attached to each other already, skip
                continue

            elif j.circuit is None or nnb.circuit is None:
                # One is unattached. Attach to the existing circuit
                circuit_id_to_join = j.circuit or nnb.circuit
                circuits[circuit_id_to_join].add(j.id)
                circuits[circuit_id_to_join].add(nnb.id)

            else:
                # Two distinct circuits combine!
                circuit_id_to_join = j.circuit

                # Grab the circuits
                circuit_to_join = circuits[j.circuit]
                circuit_to_merge = circuits[nnb.circuit]

                # Union the sets
                circuits[j.circuit] = circuit_to_join.union(circuit_to_merge)

                # Update the Jbox states to reflect the merge
                for m in circuit_to_merge:
                    m.circuit = j.circuit

            j.circuit = circuit_id_to_join
            nnb.circuit = circuit_id_to_join
            total_circuits -= 1
            connections_made += 1

            break

    logger.info(circuits)
    circuits_by_length = sorted([len(x) for x in circuits.values()], reverse=True)[:3]
    answer = reduce(operator.mul, circuits_by_length)
    assert answer == 40


if __name__ == "__main__":
    main()
