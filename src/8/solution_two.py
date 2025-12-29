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
        self.circuit = self.id

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
    line_generator = read_input(Path(__file__).parent / "input.txt")
    # line_generator = read_input(Path(__file__).parent / "test_input.txt")
    j_boxes_by_id: dict[str, Junction] = {}

    logger.info("Reading coords and constructing circuits")

    for line in line_generator:
        x, y, z = (int(i) for i in line.strip().split(","))
        j = Junction(x, y, z)
        j_boxes_by_id[j.id] = j

    circuits: dict[str, set[Junction]] = {
        j.circuit: set([j.id]) for j in j_boxes_by_id.values()
    }
    logger.info("Connecting the closest ten...")
    total_circuits = len(j_boxes_by_id.keys())
    connections_made = 0

    all_j_boxes = list(j_boxes_by_id.values())
    all_conns = [
        x
        for x in sorted(
            [
                {"distance": i.distance_from(j), "from": i, "to": j}
                for i in all_j_boxes
                for j in all_j_boxes
                if i.id != j.id
            ],
            key=(lambda j: j["distance"]),
        )
    ]

    for conn in all_conns:
        j = conn["from"]
        nnb = conn["to"]

        if j.circuit == nnb.circuit:
            # Both are attached to each other already, skip
            continue

        elif j.circuit is None or nnb.circuit is None:
            # One is unattached. Attach to the existing circuit
            circuit_id_to_join = j.circuit or nnb.circuit
            circuits[circuit_id_to_join].add(j.id)
            circuits[circuit_id_to_join].add(nnb.id)
            j.circuit = circuit_id_to_join
            nnb.circuit = circuit_id_to_join

        else:
            # Two distinct circuits combine!
            circuits_by_size = sorted(
                [j.circuit, nnb.circuit],
                key=(lambda id: len(circuits.get(id))),
                reverse=True,
            )

            # Grab the circuits
            circuit_to_join = circuits[circuits_by_size[0]]
            circuit_to_merge = circuits[circuits_by_size[1]]

            # Union the sets
            circuits[circuits_by_size[0]] = circuit_to_join.union(circuit_to_merge)

            # Update the Jbox states to reflect the merge
            for m in circuit_to_merge:
                j_boxes_by_id[m].circuit = circuits_by_size[0]

            del circuits[circuits_by_size[1]]

        total_circuits -= 1
        connections_made += 1

        not_connected_jbs = reduce(
            operator.add, sorted([len(x) for x in circuits.values()], reverse=True)[1:]
        )
        if not_connected_jbs <= 1:
            break

    # Get the last remaining node
    last_node_id = next(list(j) for j in circuits.values() if len(j) == 1)[0]
    node = j_boxes_by_id[last_node_id]
    node.get_nearest_unconnected_neighbour(j_boxes_by_id.values())
    x1 = node.x
    x2 = j_boxes_by_id[node.nearest_neighbour_id].x
    answer = x1 * x2

    # assert answer == 40
    logger.info(answer)


if __name__ == "__main__":
    main()
