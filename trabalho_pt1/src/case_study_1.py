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

    graph_type_matrix_memusg = int(graph_type_matrix.stdout)
    graph_type_list_memusg = int(graph_type_list.stdout)

    print(
        "Gasto de memória (kb)",
        f"Grafo lista: {graph_type_list_memusg} ({time_list:.3f}s)",
        f"Grafo matriz: {graph_type_matrix_memusg} ({time_matrix:.3f}s)",
        sep="\n",
        end="\n\n",
    )

    # ---------------------------------------------- #

    with open(input_path) as text_file:
        vertices_num = int(text_file.readline())
        edges = text_file.readlines()
        edges = [Edge(*edge.strip().split()) for edge in edges]

        g_matrix = Graph("matriz", vertices_num)
        g_list = Graph("lista", vertices_num)

        for edge in edges:
            g_matrix.insert_relation(edge)
            g_list.insert_relation(edge)

        # --------------- Questão 2 - extra ------------------- #
        out_path = path.join("..", "out")

        random_vertices = ["13681", "21383", "352", "53446", "67379"]
        times_matrix = []
        times_list = []

        for vertex in random_vertices:
            local_times_matrix = 0
            local_times_list = 0

            for _ in range(10):
                start = time.time()
                g_matrix.breadth_first_search(vertex, out_path)
                end = time.time()
                local_times_matrix += end - start

                start = time.time()
                g_list.breadth_first_search(vertex, out_path)
                end = time.time()
                local_times_list += end - start

            times_matrix.append(local_times_matrix / 10)
            times_list.append(local_times_list / 10)

        print(
            f"Tempos (grafo matriz): {', '.join(f'{time:.2e}s' for time in times_matrix)}")
        print(
            f"Tempos (grafo lista): {', '.join(f'{time:.2e}s' for time in times_list)}")
        print()

        # --------------- Questão 3 ------------------- #
        start = time.time()
        connected_components_list = g_list.find_connected_components()
        end = time.time()
        time_list = end - start

        start = time.time()
        connected_components_matrix = g_matrix.find_connected_components()
        end = time.time()
        time_matrix = end - start

        print(
            f"O grafo (lista) possui {len(connected_components_list)} componentes conexos. ({time_list:.3f})")
        print(
            f"O grafo (matriz) possui {len(connected_components_matrix)} componentes conexos. ({time_matrix:.3f})")

        size_connected_components = [len(c) for c in connected_components_list]

        print(
            f"O maior componente conexo do grafo possui {max(size_connected_components)} vértices")
        print(
            f"O menor componente conexo do grafo possui {min(size_connected_components)} vértices")
