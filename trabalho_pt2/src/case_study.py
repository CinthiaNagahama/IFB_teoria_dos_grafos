# Objetivos: (collaboration_graph.txt)
# 1. Compare o desempenho em termo de utilização de memória para as duas formas de representação de grafo
# 2. Compare a complexidade em termo de tempo para a BFS das duas formas de representação
# 3. Obtenha os componentes conexos do grafo
#    3.1 Quantidade de componentes conexos
#    3.2 Maior e menor componente conexo

from graph import Graph, Edge
from time import time
from os import makedirs, path

if __name__ == "__main__":

    input_paths = [
        path.join("..", "input", "trab2grafo_1.txt"),
        path.join("..", "input", "trab2grafo_2.txt"),
        path.join("..", "input", "trab2grafo_3.txt"),
        path.join("..", "input", "trab2grafo_4.txt"),
        path.join("..", "input", "trab2grafo_5.txt"),
    ]

    for i, input_path in enumerate(input_paths):
        with open(input_path, "r") as input_file:
            vertices_num = int(input_file.readline())
            edges = input_file.readlines()
            edges = [Edge(*edge.strip().split()) for edge in edges]

            g_list = Graph("lista", vertices_num, weighted=True)
            g_matrix = Graph("matriz", vertices_num, weighted=True)

            for edge in edges:
                g_list.insert_relation(edge)
                g_matrix.insert_relation(edge)

            src = "1"
            for dest in ["10", "100", "1000", "10000"]:
                for g, g_type in [(g_list, "list"), (g_matrix, "matrix")]:
                    start = time()
                    minimum_path = g.find_minimum_path(src, dest)
                    finish = time()

                    print(f"{g_type} - grafo_{i+1} - {src}_to_{dest}: {(finish - start):.2e}")
                    # print(minimum_path)
                    if minimum_path:
                        path_str = (
                            "Complete path:\n"
                            + " -> ".join([f"{step[0]} ({step[1]:.2f})" for step in minimum_path])
                            + "\n"
                        )
                        path_str += f"Destination = {minimum_path[-1][0]} | Total distance = {minimum_path[-1][1]}\n"

                        path_file = path.join(path.curdir, "..", "out", f"{g_type}", f"grafo_{i+1}")
                        makedirs(path_file, exist_ok=True)
                        with open(path.join(path_file, f"{src}_to_{dest}.txt"), "w") as out_file:
                            out_file.write(path_str)
