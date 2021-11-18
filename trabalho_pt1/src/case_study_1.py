# Objetivos: (collaboration_graph.txt)
# 1. Compare o desempenho em termo de utilização de memória para as duas formas de representação de grafo
# 2. Compare a complexidade em termo de tempo para a BFS das duas formas de representação
# 3. Obtenha os componentes conexos do grafo
#    3.1 Quantidade de componentes conexos
#    3.2 Maior e menor componente conexo

from graph import Graph, Edge
import time
from subprocess import run
from os import path

if __name__ == "__main__":

    input_path = path.join("..", "input", "collaboration_graph.txt")

    # --------------- Questão 1 ------------------- #
    start = time.time()
    graph_type_matrix = run(
        ["./memusg.py", "./case_study_1_1.py", input_path, "matriz"],
        capture_output=True,
        encoding="utf-8",
    )
    end = time.time()
    time_matrix = end - start

    start = time.time()
    graph_type_list = run(
        ["./memusg.py", "./case_study_1_1.py", input_path, "lista"],
        capture_output=True,
        encoding="utf-8",
    )
    end = time.time()
    time_list = end - start

    # print(graph_type_matrix)
    # print(graph_type_list)

    graph_type_matrix_memusg = int(graph_type_matrix.stdout)
    graph_type_list_memusg = int(graph_type_list.stdout)

    print(
        "Gasto de memória (kb)",
        f"Grafo lista: {graph_type_list_memusg} ({time_list:.2e}s)",
        f"Grafo matriz: {graph_type_matrix_memusg} ({time_matrix:.2e}s)",
        sep="\n",
    )

    # ---------------------------------------------- #

    # with open(input_path) as text_file:
    #     vertices_num = int(text_file.readline())
    #     edges = text_file.readlines()
    #     edges = [Edge(*edge.strip().split()) for edge in edges]

    #     g_matrix = Graph("matriz", vertices_num)
    #     g_list = Graph("lista", vertices_num)

    #     for edge in edges:
    #         g_matrix.insert_relation(edge)
    #         g_list.insert_relation(edge)

    #     # --------------- Questão 2 - extra ------------------- #
    #     out_path = path.join("..", "out")

    #     start = time.time()
    #     g_matrix.breadth_first_search("1", out_path)
    #     end = time.time()
    #     time_matrix = end - start
    #     print(f"Tempo grafo matriz: {time_matrix:.2e}s")

    #     start = time.time()
    #     g_list.breadth_first_search("1", out_path)
    #     end = time.time()
    #     time_list = end - start
    #     print(f"Tempo grafo lista: {time_list:.2e}s")

    #     # --------------- Questão 3 ------------------- #
    #     connected_components = g_list.find_connected_components()
    #     print(f"O grafo possui {len(connected_components)} componentes conexos.")

    #     size_connected_components = [len(c) for c in connected_components]

    #     print(f"O maior componente conexo do grafo possui {max(size_connected_components)} vértices")
    #     print(f"O menor componente conexo do grafo possui {min(size_connected_components)} vértices")
