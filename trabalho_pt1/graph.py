from itertools import filterfalse
from os import path
from typing import Dict, FrozenSet, List, Literal, NamedTuple, Optional, Set, Tuple
import numpy as np
import math as m
from functools import reduce


class Edge(NamedTuple):
    src: str
    dest: str


class Graph:
    def __init__(self, graph_type: Literal["matrix", "list"], vertices_num: int) -> None:
        self.graph_type = graph_type
        self.vertices_num = vertices_num
        if self.graph_type == "matrix":
            self.__instance = _GraphMatrix(self.vertices_num)
        elif self.graph_type == "list":
            self.__instance = _GraphList(self.vertices_num)
        else:
            raise ValueError("Tipo de grafo inválido!")

    def insert_relation(self, edge: Edge) -> None:
        self.__instance.insert_relation(edge)

    def out_graph(self) -> None:
        self.__instance.out_graph()

    def breadth_first_search(self, origin: str):
        vertices = self.__instance.breadth_first_search(origin)

        if vertices is None:
            raise ValueError(f"O argumento origem: {origin} não pertence ao grafo!")

        self._search_out_graph(vertices, "largura")

    def depth_first_search(self, origin: str):
        vertices = self.__instance.depth_first_search(origin)

        if vertices is None:
            raise ValueError(f"O argumento origem: {origin} não pertence ao grafo!")

        self._search_out_graph(vertices, "profundidade")

    def find_connected_components(self):
        return self.__instance.find_connected_components()

    def _search_out_graph(self, vertices: Dict[str, Tuple[str, int]], search_type: Literal["largura", "profundidade"]):
        translate_search_type = {"largura": "breadth", "profundidade": "depth"}
        max_len_number = m.floor(m.log10(self.vertices_num)) + 1

        with open(
            path.join(path.curdir, f"graph_{self.graph_type}_{translate_search_type[search_type]}_search_out.txt"), "w"
        ) as file:
            for vertex, (parent, level) in vertices.items():
                file.write(
                    f"{vertex:>{max_len_number}}: {'Raiz':^{max_len_number + 6}} | Nível = {level}\n"
                    if parent == ""
                    else f"{vertex:>{max_len_number}}: Pai = {parent:>{max_len_number}} | Nível = {level}\n"
                )


class _GraphMatrix:
    def __init__(self, vertices_num: int) -> None:
        self.vertices = [str(v + 1) for v in range(vertices_num)]
        self.adj_matrix = np.zeros((vertices_num, vertices_num), dtype=int)

    def _get_vertex_index(self, vertex: str) -> int:
        return self.vertices.index(vertex)

    def insert_relation(self, edge: Edge):
        self.adj_matrix[self._get_vertex_index(edge.src)][self._get_vertex_index(edge.dest)] = 1
        self.adj_matrix[self._get_vertex_index(edge.dest)][self._get_vertex_index(edge.src)] = 1

    def breadth_first_search(self, origin: str) -> Optional[Dict[str, Tuple[str, int]]]:
        if origin not in self.vertices:
            return None

        # [current, parent, level]
        vertices_queue: List[Tuple[str, str, int]] = []
        # {current: (parent, level)}
        visited_vertices: Dict[str, Tuple[str, int]] = dict()

        to_be_visited_vertices: Set[str] = set()

        vertices_queue.append((origin, "", 0))

        while len(vertices_queue) != 0:
            (current, parent, level) = vertices_queue.pop(0)
            to_be_visited_vertices.discard(current)

            visited_vertices[current] = (parent, level)

            (indexes,) = np.nonzero(self.adj_matrix[self._get_vertex_index(current)])
            for idx in indexes:
                vertex = str(idx + 1)
                if vertex not in visited_vertices and vertex not in to_be_visited_vertices:
                    vertices_queue.append((vertex, current, level + 1))
                    to_be_visited_vertices.add(vertex)

        return visited_vertices

    def depth_first_search(self, origin: str) -> Optional[Dict[str, Tuple[str, int]]]:
        if origin not in self.vertices:
            return None

        # [current, parent, level]
        vertices_stack: List[Tuple[str, str, int]] = []
        # {current: (parent, level)}
        visited_vertices: Dict[str, Tuple[str, int]] = dict()
        to_be_visited_vertices: Set[str] = set()

        vertices_stack.append((origin, "", 0))

        while len(vertices_stack) != 0:
            current, parent, level = vertices_stack.pop()
            visited_vertices[current] = (parent, level)
            to_be_visited_vertices.discard(current)

            (indexes,) = np.nonzero(self.adj_matrix[self._get_vertex_index(current)])
            for idx in indexes:
                vertex = str(idx + 1)
                if vertex not in visited_vertices and vertex not in to_be_visited_vertices:
                    vertices_stack.append((vertex, current, level + 1))
                    to_be_visited_vertices.add(vertex)

        return visited_vertices

    def _search_out_graph(self, vertices: Dict[str, Tuple[str, int]], search_type: Literal["largura", "profundidade"]):
        translate_search_type = {"largura": "breadth", "profundidade": "depth"}

        with open(
            path.join(path.curdir, f"graph_list_{translate_search_type[search_type]}_search_out.txt", "w")
        ) as file:
            for vertex, (parent, level) in vertices.items():
                file.write(
                    f"{vertex}: Nível = {level}" if parent == "" else f"{vertex}: Pai = {parent} | Nível = {level}"
                )

    def find_connected_components(self) -> List[Set[str]]:
        connected_components: List[Set[str]] = list()
        component: List[str] = list()

        vertices_queue: List[str] = []

        to_be_visited_vertices: Set[str] = set()
        visited_vertices: Set[str] = set()

        for vertex in self.vertices:
            if vertex not in visited_vertices:
                vertices_queue.append(vertex)
                component = list()

                while len(vertices_queue) != 0:
                    current = vertices_queue.pop(0)

                    component.append(current)

                    to_be_visited_vertices.discard(current)
                    visited_vertices.add(current)

                    (indexes,) = np.nonzero(self.adj_matrix[self._get_vertex_index(current)])
                    for idx in indexes:
                        vertex = str(idx + 1)
                        if vertex not in visited_vertices and vertex not in to_be_visited_vertices:
                            vertices_queue.append(vertex)
                            to_be_visited_vertices.add(vertex)

                connected_components.append(set(component))

        return connected_components

    def out_graph(self):
        with open(path.join(path.curdir, "graph_matrix_out.txt"), "w") as file:
            file.write(f"# n = {len(self.vertices)}\n")
            file.write(f"# m = {int(np.count_nonzero(self.adj_matrix) / 2)}\n")
            for vertex, line in enumerate(self.adj_matrix):
                file.write(f"{vertex + 1} {np.count_nonzero(line)}\n")


class _GraphList:
    def __init__(self, vertices_num: int) -> None:
        self.elements: Dict[str, Set[str]] = {
            vertex: set() for vertex in (str(vertice + 1) for vertice in range(vertices_num))
        }

    def insert_relation(self, edge: Edge):
        self[edge.src].add(edge.dest)
        self[edge.dest].add(edge.src)

    def out_graph(self):
        with open(path.join(path.curdir, "graph_list_out.txt"), "w") as file:
            file.write(f"# n = {len(self.elements.keys())}\n")
            file.write(f"# m = {int(sum(len(edges) for edges in self.elements.values()) / 2)}\n")

            for vertex, edges in self.elements.items():
                file.write(f"{vertex} {len(edges)}\n")

    def breadth_first_search(self, origin: str) -> Optional[Dict[str, Tuple[str, int]]]:
        if origin not in self.elements:
            return None

        # [current, parent, level]
        vertices_queue: List[Tuple[str, str, int]] = []
        # {current: (parent, level)}
        visited_vertices: Dict[str, Tuple[str, int]] = dict()

        to_be_visited_vertices: Set[str] = set()

        vertices_queue.append((origin, "", 0))

        while len(vertices_queue) != 0:
            current, parent, level = vertices_queue.pop(0)
            visited_vertices[current] = parent, level
            to_be_visited_vertices.discard(current)

            for edge in self[current]:
                if edge not in visited_vertices and edge not in to_be_visited_vertices:
                    vertices_queue.append((edge, current, level + 1))
                    to_be_visited_vertices.add(edge)

        return visited_vertices

    def depth_first_search(self, origin: str) -> Optional[Dict[str, Tuple[str, int]]]:
        if origin not in self.elements:
            return None

        # [current, parent, level]
        vertices_stack: List[Tuple[str, str, int]] = []
        # {current: (parent, level)}
        visited_vertices: Dict[str, Tuple[str, int]] = dict()

        to_be_visited_vertices: Set[str] = set()

        vertices_stack.append((origin, "", 0))

        while len(vertices_stack) != 0:
            current, parent, level = vertices_stack.pop()
            visited_vertices[current] = parent, level
            to_be_visited_vertices.discard(current)

            for edge in self[current]:
                if edge not in visited_vertices and edge not in to_be_visited_vertices:
                    vertices_stack.append((edge, current, level + 1))
                    to_be_visited_vertices.add(edge)

        return visited_vertices

    def find_connected_components(self) -> List[Set[str]]:
        components: Set[FrozenSet[str]] = set()
        connected_components: List[Set[str]] = list()

        for vertex in self.elements:
            components.add(frozenset({vertex, *self[vertex]}))

        while len(components) > 0:
            acc_component = components.pop()

            while True:
                acc_component, merged = reduce(self._reduce_components, components, (acc_component, False))
                components = set(filterfalse(lambda component: component.issubset(acc_component), components))
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


if __name__ == "__main__":
    with open("teste.txt") as text_file:
        vertices_num = int(text_file.readline())
        edges = text_file.readlines()
        edges = [Edge(*edge.strip().split()) for edge in edges]

        g_matrix = Graph("matrix", vertices_num)
        g_list = Graph("list", vertices_num)

        for edge in edges:
            g_matrix.insert_relation(edge)
            g_list.insert_relation(edge)

        g_matrix.out_graph()
        g_list.out_graph()

        g_matrix.breadth_first_search("1")
        g_list.breadth_first_search("1")
