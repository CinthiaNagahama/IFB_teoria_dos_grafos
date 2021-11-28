from os import path
from typing import Dict, List, Literal, NamedTuple, Optional, Set, Tuple, Deque
import numpy as np
import math as m
from collections import deque


class Edge(NamedTuple):
    src: str
    dest: str


class Graph:
    def __init__(self, graph_type: Literal["matriz", "lista"], vertices_num: int) -> None:
        self.graph_type = graph_type
        self.vertices_num = vertices_num

        if self.graph_type == "matriz":
            self.__instance = _GraphMatrix(self.vertices_num)
            self.graph_type = "matrix"
        elif self.graph_type == "lista":
            self.__instance = _GraphList(self.vertices_num)
            self.graph_type = "list"
        else:
            raise ValueError("Tipo de grafo inválido!")

    def insert_relation(self, edge: Edge) -> None:
        self.__instance.insert_relation(edge)

    def get_graph_degrees(self) -> Dict[str, int]:
        return self.__instance.get_graph_degrees()

    def out_graph(self, out_path: str) -> None:
        self.__instance.out_graph(out_path)

    def breadth_first_search(self, origin: str, out_path: Optional[str] = None):
        vertices = self.__instance.breadth_first_search(origin)

        if vertices is None:
            raise ValueError(
                f"O argumento origem: {origin} não pertence ao grafo!")

        if out_path is not None:
            self._search_out_graph(vertices, "largura", out_path)

    def depth_first_search(self, origin: str, out_path: Optional[str] = None):
        vertices = self.__instance.depth_first_search(origin)

        if vertices is None:
            raise ValueError(
                f"O argumento origem: {origin} não pertence ao grafo!")

        if out_path is not None:
            self._search_out_graph(vertices, "profundidade", out_path)

    def find_connected_components(self) -> List[Set[str]]:
        return self.__instance.find_connected_components()

    def _search_out_graph(
        self, vertices: Dict[str, Tuple[str, int]], search_type: Literal["largura", "profundidade"], out_path: str
    ):
        translate_search_type = {"largura": "breadth", "profundidade": "depth"}
        max_len_number = m.floor(m.log10(self.vertices_num)) + 1

        with open(
            path.join(
                out_path, f"graph_{self.graph_type}_{translate_search_type[search_type]}_search_out.txt"), "w"
        ) as file:
            for vertex, (parent, level) in vertices.items():
                file.write(
                    f"{vertex:>{max_len_number}}: {'Raiz':^{max_len_number + 6}} | Nível = {level}\n"
                    if parent == ""
                    else f"{vertex:>{max_len_number}}: Pai = {parent:>{max_len_number}} | Nível = {level}\n"
                )


class _GraphMatrix:
    def __init__(self, vertices_num: int) -> None:
        self.vertices = {str(v + 1): v for v in range(vertices_num)}
        self.adj_matrix = np.zeros((vertices_num, vertices_num), dtype="bool")

    def insert_relation(self, edge: Edge):
        self.adj_matrix[self.vertices[edge.src]][self.vertices[edge.dest]] = 1
        self.adj_matrix[self.vertices[edge.dest]][self.vertices[edge.src]] = 1

    def breadth_first_search(self, origin: str) -> Optional[Dict[str, Tuple[str, int]]]:
        if origin not in self.vertices:
            return None

        # [current, parent, level]
        vertices_queue: Deque[Tuple[str, str, int]] = deque()
        # {current: (parent, level)}
        visited_vertices: Dict[str, Tuple[str, int]] = dict()

        to_be_visited_vertices: Set[str] = set()

        vertices_queue.append((origin, "", 0))

        while len(vertices_queue) > 0:
            (current, parent, level) = vertices_queue.popleft()
            to_be_visited_vertices.discard(current)

            visited_vertices[current] = (parent, level)

            (indexes,) = np.nonzero(self.adj_matrix[self.vertices[current]])
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
        vertices_stack: Deque[Tuple[str, str, int]] = deque()
        # {current: (parent, level)}
        visited_vertices: Dict[str, Tuple[str, int]] = dict()
        to_be_visited_vertices: Set[str] = set()

        vertices_stack.append((origin, "", 0))

        while len(vertices_stack) != 0:
            current, parent, level = vertices_stack.pop()
            visited_vertices[current] = (parent, level)
            to_be_visited_vertices.discard(current)

            (indexes,) = np.nonzero(self.adj_matrix[self.vertices[current]])
            for idx in indexes:
                vertex = str(idx + 1)
                if vertex not in visited_vertices and vertex not in to_be_visited_vertices:
                    vertices_stack.append((vertex, current, level + 1))
                    to_be_visited_vertices.add(vertex)

        return visited_vertices

    def find_connected_components(self) -> List[Set[str]]:
        connected_components: List[Set[str]] = list()
        component: List[str] = list()

        vertices_queue: Deque[str] = deque()

        to_be_visited_vertices: Set[str] = set()
        visited_vertices: Set[str] = set()

        for vertex in self.vertices:
            if vertex not in visited_vertices:
                vertices_queue.append(vertex)
                component = list()

                while len(vertices_queue) != 0:
                    current = vertices_queue.popleft()

                    component.append(current)

                    to_be_visited_vertices.discard(current)
                    visited_vertices.add(current)

                    (indexes,) = np.nonzero(
                        self.adj_matrix[self.vertices[current]])
                    for idx in indexes:
                        vertex = str(idx + 1)
                        if vertex not in visited_vertices and vertex not in to_be_visited_vertices:
                            vertices_queue.append(vertex)
                            to_be_visited_vertices.add(vertex)

                connected_components.append(set(component))

        return connected_components

    def get_graph_degrees(self) -> Dict[str, int]:
        return {str(vertex + 1): np.count_nonzero(line) for vertex, line in enumerate(self.adj_matrix)}

    def out_graph(self, out_path: str):
        with open(path.join(out_path, "graph_matrix_out.txt"), "w") as file:
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

    def get_graph_degrees(self) -> Dict[str, int]:
        return {vertex: len(edges) for vertex, edges in self.elements.items()}

    def out_graph(self, out_path: str):
        with open(path.join(out_path, "graph_list_out.txt"), "w") as file:
            file.write(f"# n = {len(self.elements.keys())}\n")
            file.write(
                f"# m = {int(sum(len(edges) for edges in self.elements.values()) / 2)}\n")

            for vertex, edges in self.elements.items():
                file.write(f"{vertex} {len(edges)}\n")

    def breadth_first_search(self, origin: str) -> Optional[Dict[str, Tuple[str, int]]]:
        if origin not in self.elements:
            return None

        # [current, parent, level]
        # vertices_queue: List[Tuple[str, str, int]] = []
        vertices_queue: Deque[Tuple[str, str, int]] = deque()
        # {current: (parent, level)}
        visited_vertices: Dict[str, Tuple[str, int]] = dict()

        to_be_visited_vertices: Set[str] = set()

        vertices_queue.append((origin, "", 0))

        while len(vertices_queue) != 0:
            current, parent, level = vertices_queue.popleft()
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
        vertices_stack: Deque[Tuple[str, str, int]] = deque()
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
        connected_components: List[Set[str]] = list()
        visited_vertices: Set[str] = set()

        for vertex in self.elements:
            if vertex in visited_vertices:
                continue

            to_be_visited_vertices: Set[str] = set()
            vertices_stack: Deque[str] = deque()
            local_component: Set[str] = set()

            vertices_stack.append(vertex)

            while len(vertices_stack) != 0:
                current_vertex = vertices_stack.pop()

                visited_vertices.add(current_vertex)
                local_component.add(current_vertex)
                to_be_visited_vertices.discard(current_vertex)

                for edge in self[current_vertex]:
                    if edge not in visited_vertices and edge not in to_be_visited_vertices:
                        vertices_stack.append(edge)
                        to_be_visited_vertices.add(edge)

            connected_components.append(local_component)

        return connected_components


if __name__ == "__main__":
    with open("teste.txt") as text_file:
        vertices_num = int(text_file.readline())
        edges = text_file.readlines()
        edges = [Edge(*edge.strip().split()) for edge in edges]

        g_matrix = Graph("matriz", vertices_num)
        g_list = Graph("lista", vertices_num)

        for edge in edges:
            g_matrix.insert_relation(edge)
            g_list.insert_relation(edge)

        out_path = path.join("..", "out")

        g_matrix.out_graph(out_path)
        g_list.out_graph(out_path)

        # g_matrix.breadth_first_search("1", out_path)
        # g_list.breadth_first_search("1", out_path)

        # g_matrix.depth_first_search("1", out_path)
        # g_list.depth_first_search("1", out_path)
