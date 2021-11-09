import sys
from typing import Optional
from graph import Graph, Edge


def validate_args() -> Optional[str]:
    try:
        text_arg = sys.argv[1]
    except IndexError:
        print("Argumento de texto de entrada não encontrado!")
    else:
        return text_arg


if __name__ == "__main__":

    text_arg = validate_args()

    if text_arg is None:
        exit(0)

    with open(text_arg) as text_file:
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

        # g_matrix.breadth_first_search("1")
        # g_list.breadth_first_search("1")

        # g_list.depth_first_search("1")
        # g_matrix.depth_first_search("1")

        print("Matriz: ")
        print(g_matrix.find_connected_components())

        print("Lista: ")
        print(g_list.find_connected_components())
