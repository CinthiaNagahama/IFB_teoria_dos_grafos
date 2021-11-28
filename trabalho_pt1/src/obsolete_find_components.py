from itertools import filterfalse
from typing import Dict, FrozenSet, List, NamedTuple, Set, Tuple
from functools import reduce


class Edge(NamedTuple):
    src: str
    dest: str


class OldGraphList:
    def __init__(self, vertices_num: int) -> None:
        self.elements: Dict[str, Set[str]] = {
            vertex: set() for vertex in (str(vertice + 1) for vertice in range(vertices_num))
        }

    def insert_relation(self, edge: Edge):
        self[edge.src].add(edge.dest)
        self[edge.dest].add(edge.src)

    def find_connected_components(self) -> List[Set[str]]:
        components: Set[FrozenSet[str]] = set()
        connected_components: List[Set[str]] = list()

        for vertex in self.elements:
            components.add(frozenset({vertex, *self[vertex]}))

        while len(components) > 0:
            acc_component = components.pop()

            while True:
                acc_component, merged = reduce(
                    self._reduce_components, components, (acc_component, False))
                components = set(filterfalse(
                    lambda component: component.issubset(acc_component), components))
                if not merged:
                    break

            connected_components.append(set(acc_component))

        return connected_components

    @staticmethod
    def _reduce_components(acc: Tuple[Set[str], bool], component: Set[str]):
        acc_component, merged = acc
        if acc_component.isdisjoint(component):
            return acc_component, merged
        else:
            return acc_component.union(component), True

    def __getitem__(self, key):
        return self.elements[key]
