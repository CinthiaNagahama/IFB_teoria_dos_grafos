from os import path
from typing import Dict, Literal, NamedTuple, Set
import numpy as np


class Edge(NamedTuple):
    src: str
    dest: str


class Graph:
    def __init__(self, graph_type: Literal["matrix", "list"], vertices_num: int) -> None:
        if graph_type == "matrix":
            self.__instance = _GraphMatrix(vertices_num)
        elif graph_type == "list":
            self.__instance = _GraphList(vertices_num)
        else:
            raise ValueError("Tipo de grafo inválido!")

    def insert_relation(self, edge: Edge) -> None:
        self.__instance.insert_relation(edge)

    def out_graph(self) -> None:
        self.__instance.out_graph()

    def breadth_first_search(self, origin: str):
        self.__instance.breadth_first_search(origin)

    def depth_first_search(self, origin: str):
        self.__instance.depth_first_search(origin)

    def find_connected_components(self):
        self.__instance.find_connected_components()


class _GraphMatrix:
    def __init__(self, vertices_num: int) -> None:
        self.vertices = [str(v + 1) for v in range(vertices_num)]
        self.adj_matrix = np.zeros((vertices_num, vertices_num), dtype=int)

    def _get_vertex_index(self, vertex: str) -> int:
        return self.vertices.index(vertex)

    def insert_relation(self, edge: Edge):
        self.adj_matrix[self._get_vertex_index(edge.src)][self._get_vertex_index(edge.dest)] = 1
        self.adj_matrix[self._get_vertex_index(edge.dest)][self._get_vertex_index(edge.src)] = 1

    def breadth_first_search(self, origin: str):
        pass

    def depth_first_search(self, origin: str):
        pass

    def find_connected_components(self):
        pass

    def out_graph(self):
        with open(path.join(path.curdir, "graph_matrix_out.txt"), "w") as file:
            file.write(f"# n = {len(self.vertices)}\n")
            file.write(f"# m = {int(len(np.nonzero(self.adj_matrix)[0]) / 2)}\n")
            for vertex, line in enumerate(self.adj_matrix):
                file.write(f"{vertex + 1} {len(np.nonzero(line)[0])}\n")


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

    def breadth_first_search(self, origin: str):
        pass

    def depth_first_search(self, origin: str):
        pass

    def find_connected_components(self):
        pass

    def __getitem__(self, key):
        return self.elements[key]
