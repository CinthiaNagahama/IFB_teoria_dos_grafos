from os import path
from typing import Dict, List, Literal, Optional, Set, Tuple, Deque, Union
import numpy as np
import math as m
from collections import defaultdict, deque
from scipy import sparse as sps
import heapq


class Edge:
    def __init__(self, src: str, dest: str, weight: Union[float, str] = np.nan) -> None:
        self.src = src
        self.dest = dest
        self.weight = float(weight)


class Graph:
    def __init__(self, graph_type: Literal["matriz", "lista"], vertices_num: int, weighted: bool) -> None:
        self.graph_type = graph_type
        self.vertices_num = vertices_num
        self.weighted = weighted

        if self.graph_type == "matriz":
            self.__instance = _GraphMatrix(self.vertices_num, self.weighted)
            self.graph_type = "matrix"
        elif self.graph_type == "lista":
            self.__instance = _GraphList(self.vertices_num)
            self.graph_type = "list"
        else:
            raise ValueError("Tipo de grafo inválido!")

    def insert_relation(self, edge: Edge) -> None:
        if self.weighted and (edge.weight is np.nan):
            raise ValueError("Peso inexistente")
        if (not self.weighted) and (edge.weight is not np.nan):
            raise ValueError("Grafo não aceita pesos")

        self.__instance.insert_relation(edge)

    def get_graph_degrees(self) -> Dict[str, int]:
        return self.__instance.get_graph_degrees()

    def out_graph(self, out_path: str) -> None:
        self.__instance.out_graph(out_path)

    def breadth_first_search(self, origin: str, out_path: Optional[str] = None):
        vertices = self.__instance.breadth_first_search(origin)

        if vertices is None:
            raise ValueError(f"O argumento origem: {origin} não pertence ao grafo!")

        if out_path is not None:
            self._search_out_graph(vertices, "largura", out_path)

    def depth_first_search(self, origin: str, out_path: Optional[str] = None):
        vertices = self.__instance.depth_first_search(origin)

        if vertices is None:
            raise ValueError(f"O argumento origem: {origin} não pertence ao grafo!")

        if out_path is not None:
            self._search_out_graph(vertices, "profundidade", out_path)

    def find_minimum_path(self, origin: str, end: str) -> Optional[Union[List[str], List[Tuple[str, float]]]]:
        if self.weighted:  # dijkstra
            # Dijkstra feito com Heap Binária

            if not self.__instance._check_all_positive():
                print(
                    "WARNING: Há pesos negativos no grafo, ou seja, o algorítmo de dijkstra pode não achar uma solução ótima ou até mesmo entrar em um ciclo infinito"
                )

            vertices = self.__instance.dijkstra(origin)
            if end not in vertices:
                print("O vértice de destino não se encontra no mesmo componente do vértice de origem")
                return None

            # [(edge, acc_weight), ...]
            path: List[Tuple[str, float]] = []
            next_vertice, accumulated_weight = vertices[end]
            current = end
            while current != origin:
                path.append((current, accumulated_weight))
                current = next_vertice
                next_vertice, accumulated_weight = vertices[current]

            path.append((current, accumulated_weight))

            return path[::-1]
        else:  # bfs
            vertices = self.__instance.breadth_first_search(origin)

            if end not in vertices:
                print("O vértice de destino não se encontra no mesmo componente do vértice de origem")
                return None

            # [edge, edge, ...]
            path = []
            next_vertice, _ = vertices[end]
            current = end
            while current != origin:
                path.append(current)
                current = next_vertice
                next_vertice, _ = vertices[current]

            path.append(current)

            return path[::-1]

    def _dijkstra(self, origin: str) -> List[Tuple[str, float]]:
        return self.__instance.dijkstra(origin)

    def find_connected_components(self) -> List[Set[str]]:
        return self.__instance.find_connected_components()

    def _search_out_graph(
        self,
        vertices: Dict[str, Tuple[str, int]],
        search_type: Literal["largura", "profundidade"],
        out_path: str,
    ):
        translate_search_type = {"largura": "breadth", "profundidade": "depth"}
        max_len_number = m.floor(m.log10(self.vertices_num)) + 1
        max_len_level = m.floor(m.log10(max((values[1] for values in vertices.values())))) + 1

        with open(
            path.join(out_path, f"graph_{self.graph_type}_{translate_search_type[search_type]}_search_out.txt"), "w"
        ) as file:
            for vertex, (parent, level) in vertices.items():
                line = (
                    f"{vertex:>{max_len_number}}: {'Raiz':^{max_len_number + 6}} | Nível = {level:>{max_len_level}}\n"
                    if parent == ""
                    else f"{vertex:>{max_len_number}}: Pai = {parent:>{max_len_number}} | Nível = {level:>{max_len_level}}\n"
                )

                file.write(line)


class _GraphMatrix:
    def __init__(self, vertices_num: int, weighted: bool) -> None:
        self.vertices = {str(v + 1): v for v in range(vertices_num)}
        self.adj_matrix = sps.dok_matrix((vertices_num, vertices_num), dtype=float if weighted else bool)

    def insert_relation(self, edge: Edge):
        if edge.weight is not np.nan:
            self.adj_matrix[self.vertices[edge.src], self.vertices[edge.dest]] = edge.weight
            self.adj_matrix[self.vertices[edge.dest], self.vertices[edge.src]] = edge.weight
        else:
            self.adj_matrix[self.vertices[edge.src], self.vertices[edge.dest]] = 1
            self.adj_matrix[self.vertices[edge.dest], self.vertices[edge.src]] = 1

    def find_minimum_path(
        self, origin: str, end: str, mode: Union[Literal["bfs"], Literal["dijkstra"]]
    ) -> Optional[Dict[str, Tuple[str, int]]]:
        if mode == "dijkstra":
            return self.dijkstra(origin)
        else:
            return self.breadth_first_search(origin, end)

    def _check_all_positive(self) -> bool:
        return min(self.adj_matrix.values()) >= 0

    def dijkstra(self, origin: str):
        if origin not in self.vertices:
            return None

        paths: Dict[str, Tuple[str, float]] = defaultdict(lambda: ("", np.inf))
        paths[origin] = ("", 0)

        vertices_queue: List[Tuple[float, str]] = list()
        visited_vertices: Set[str] = set()

        heapq.heappush(vertices_queue, (0, origin))

        qtd_vertices = len(self.vertices)
        while len(visited_vertices) < qtd_vertices:
            acc_weigth, current = heapq.heappop(vertices_queue)
            if current in visited_vertices:
                continue

            for next_vertice, weight in self.adj_matrix[self.vertices[current]].items():
                next_vertice = str(next_vertice[1] + 1)
                new_weigth = acc_weigth + weight
                old_weigth = paths[next_vertice][1]

                if new_weigth < old_weigth:
                    paths[next_vertice] = current, new_weigth
                    heapq.heappush(vertices_queue, (new_weigth, next_vertice))

            visited_vertices.add(current)

        return dict(paths)

    def breadth_first_search(self, origin: str, end: Optional[str] = None) -> Optional[Dict[str, Tuple[str, int]]]:
        if origin not in self.vertices:
            return None
        if end is not None and end not in self.vertices:
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

            for _, idx in self.adj_matrix[self.vertices[current]].keys():
                vertex = str(idx + 1)
                if vertex not in visited_vertices and vertex not in to_be_visited_vertices:
                    vertices_queue.append((vertex, current, level + 1))
                    to_be_visited_vertices.add(vertex)

            if current == end:
                return visited_vertices

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

            for _, idx in self.adj_matrix[self.vertices[current]].keys():
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

                    for _, idx in self.adj_matrix[self.vertices[current]].keys():
                        vertex = str(idx + 1)
                        if vertex not in visited_vertices and vertex not in to_be_visited_vertices:
                            vertices_queue.append(vertex)
                            to_be_visited_vertices.add(vertex)

                connected_components.append(set(component))

        return connected_components

    def get_graph_degrees(self) -> Dict[str, int]:
        return {str(vertex + 1): line.count_nonzero() for vertex, line in enumerate(self.adj_matrix)}

    def out_graph(self, out_path: str):
        with open(path.join(out_path, "graph_matrix_out.txt"), "w") as file:
            file.write(f"# n = {len(self.vertices)}\n")
            file.write(f"# m = {int(self.adj_matrix.count_nonzero() / 2)}\n")
            for vertex, line in enumerate(self.adj_matrix):
                file.write(f"{vertex + 1} {line.count_nonzero()}\n")


class _GraphList:
    def __init__(self, vertices_num: int) -> None:
        # {vertice: (vizinho, peso)}
        self.elements: Dict[str, Set[Tuple[str, float]]] = {
            vertex: set() for vertex in (str(vertice + 1) for vertice in range(vertices_num))
        }

    def insert_relation(self, edge: Edge):
        self[edge.src].add((edge.dest, edge.weight))
        self[edge.dest].add((edge.src, edge.weight))

    def get_graph_degrees(self) -> Dict[str, int]:
        return {vertex: len(edges) for vertex, edges in self.elements.items()}

    def out_graph(self, out_path: str):
        with open(path.join(out_path, "graph_list_out.txt"), "w") as file:
            file.write(f"# n = {len(self.elements.keys())}\n")
            file.write(f"# m = {int(sum(len(edges) for edges in self.elements.values()) / 2)}\n")

            for vertex, edges in self.elements.items():
                file.write(f"{vertex} {len(edges)}\n")

    def find_minimum_path(
        self, origin: str, end: str, mode: Union[Literal["bfs"], Literal["dijkstra"]]
    ) -> Union[List[Tuple[str, float]], List[str]]:
        if origin not in self.elements or end not in self.elements:
            return None

        if mode == "dijkstra":
            vertices = self.dijkstra(origin)

            if end not in vertices:
                print("O vértice de destino não se encontra no mesmo componente do vértice de origem")
                return None

            # [(edge, acc_weight), ...]
            path: List[Tuple[str, float]] = []
            current, accumulated_weight = vertices[end]
            while current != origin:
                path.append((current, accumulated_weight))
                current, accumulated_weight = vertices[current]

            path.append((current, accumulated_weight))

            return path.reverse()
        else:  # bfs
            vertices = self.breadth_first_search(origin)

            # [edge, edge, ...]
            path = []
            current, _ = vertices[end]
            while current != origin:
                path.append(current)
                current, _ = vertices[current]

            path.append(current)

            return path.reverse()

    def breadth_first_search(self, origin: str) -> Optional[Dict[str, Tuple[str, int]]]:
        if origin not in self.elements:
            return None

        # [current, parent, level]
        vertices_queue: Deque[Tuple[str, str, int]] = deque()
        # {current: (parent, level)}
        visited_vertices: Dict[str, Tuple[str, int]] = dict()

        to_be_visited_vertices: Set[str] = set()

        vertices_queue.append((origin, "", 0))

        while len(vertices_queue) != 0:
            current, parent, level = vertices_queue.popleft()
            visited_vertices[current] = parent, level
            to_be_visited_vertices.discard(current)

            for edge, _ in self[current]:
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

            for edge, _ in self[current]:
                if edge not in visited_vertices and edge not in to_be_visited_vertices:
                    vertices_stack.append((edge, current, level + 1))
                    to_be_visited_vertices.add(edge)

        return visited_vertices

    def dijkstra(self, origin: str) -> Dict[str, Tuple[str, float]]:
        # {vertex: (parent, weight)}
        paths: Dict[str, Tuple[str, float]] = defaultdict(lambda: ("", np.inf))
        paths[origin] = ("", 0)

        vertices_queue: List[Tuple[float, str]] = list()
        visited_vertices: Set[str] = set()

        heapq.heappush(vertices_queue, (0, origin))

        qtd_vertices = len(self.elements)
        while len(visited_vertices) < qtd_vertices:
            accumulated_weight, current = heapq.heappop(vertices_queue)
            if current in visited_vertices:
                continue

            for (edge, weight) in self[current]:
                new_weight = accumulated_weight + weight
                old_weight = paths[edge][1]

                if new_weight < old_weight:
                    paths[edge] = current, new_weight
                    heapq.heappush(vertices_queue, (new_weight, edge))

            visited_vertices.add(current)

        return dict(paths)

    def _check_all_positive(self) -> bool:
        return min(min(edge[1] for edge in edges) for edges in self.elements.values()) >= 0

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

                for edge, _ in self[current_vertex]:
                    if edge not in visited_vertices and edge not in to_be_visited_vertices:
                        vertices_stack.append(edge)
                        to_be_visited_vertices.add(edge)

            connected_components.append(local_component)

        return connected_components

    def __getitem__(self, key):
        return self.elements[key]


if __name__ == "__main__":
    with open(path.join("..", "input", "teste copy.txt")) as text_file:
        vertices_num = int(text_file.readline())
        edges = text_file.readlines()
        edges = [Edge(*edge.strip().split()) for edge in edges]

        g_matrix = Graph("matriz", vertices_num, False)
        g_list = Graph("lista", vertices_num, False)

        for edge in edges:
            g_matrix.insert_relation(edge)
            g_list.insert_relation(edge)

        out_path = path.join("..", "out")

        g_matrix.out_graph(out_path)
        g_list.out_graph(out_path)

        g_matrix.breadth_first_search("1", out_path)
        g_list.breadth_first_search("1", out_path)

        g_matrix.depth_first_search("1", out_path)
        g_list.depth_first_search("1", out_path)
