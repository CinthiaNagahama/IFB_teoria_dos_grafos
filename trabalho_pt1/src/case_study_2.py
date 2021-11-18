# Objetivos: (as_graph.txt)
# 1. Trace um gráfico a partir dos graus do grafo.
#    1.1 Maior e menor graus
#    1.2 Compare o maior e o menor graus
# 2. Obtenha os componentes conexos do grafo
#    2.1 Quantidade de componentes conexos
#    2.2 Maior e menor componente conexo
# 3. Busca em largura
#    3.1 Maior nível tendo como origem o vértice 1
#    3.2 Repetir para pelo menos outros dois vértices
#    3.3 Comparar 3.1 e 3.2
# 4. Determine o comprimento do maior caminho mínimo entre dois vértices (BFS)

from graph import Graph, Edge
import matplotlib.pyplot as plt
from os import path


if __name__ == "__main__":

    input_path = path.join("..", "input", "as_graph.txt")

    with open(input_path) as text_file:
        vertices_num = int(text_file.readline())
        edges = text_file.readlines()
        edges = [Edge(*edge.strip().split()) for edge in edges]

        g_list = Graph("lista", vertices_num)

        for edge in edges:
            g_list.insert_relation(edge)

    # --------------- Questão 1 ------------------- #

    graph_degrees = g_list.get_graph_degrees()
    greatest_degree = g_list.vertices_num - 1
    print(f"O maior grau possível para o grafo seria {greatest_degree}")
    print(f"O maior grau do grafo é {max(graph_degrees.values())}")
    print(f"O menor grau do grafo é {min(graph_degrees.values())}")

    plt.plot(list(graph_degrees.values()))
    plt.fill_between(range(len(graph_degrees.values())),
                     list(graph_degrees.values()), alpha=0.5)
    plt.axhline(y=greatest_degree, color="r")
    plt.legend(["Graus", "Grau máximo"])
    plt.xlabel("Vértices")
    plt.ylabel("Graus")
    plt.title("Comparação de Graus")
    plt.grid(True)
    plt.show()

    # --------------- Questão 2 ------------------- #

    connected_components = g_list.find_connected_components()
    print(f"O grafo possui {len(connected_components)} componentes conexos.")

    size_connected_components = [len(c) for c in connected_components]

    print(
        f"O maior componente conexo do grafo possui {max(size_connected_components)} vértices")
    print(
        f"O menor componente conexo do grafo possui {min(size_connected_components)} vértices")

    # --------------- Questão 3 ------------------- #

    out_path = path.join("..", "out")

    searching_vertices = ["1", "728", "16379", "29382"]
    for v in searching_vertices:
        g_list.breadth_first_search(v, out_path)

        with open(path.join(out_path, "graph_list_breadth_search_out.txt")) as file:
            vertices = file.readlines()
            levels = [int(vertex.strip().split(sep="Nível = ")[-1])
                      for vertex in vertices]

            print(
                f"O maior nível encontrado durante a busca em largura foi: {max(levels)}")

    # --------------- Questão 4 ------------------- #

    connected_components_diameters = list()
    for c in connected_components:
        component_diameter = 0
        for v in c:
            g_list.breadth_first_search(v, out_path)

            with open(path.join(out_path, "graph_list_breadth_search_out.txt")) as file:
                vertices = file.readlines()
                levels = [int(vertex.strip().split(sep="Nível = ")[-1])
                          for vertex in vertices]

            component_diameter = max(component_diameter, max(levels))
        connected_components_diameters.append(component_diameter)

    print(f"O diâmetro da internet é: {max(connected_components_diameters)}")
