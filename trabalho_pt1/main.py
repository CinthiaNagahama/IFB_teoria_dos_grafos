import sys
from typing import Optional
from graph import Graph, Edge


def validate_args() -> Optional[str]:
    try:
        text_arg = sys.argv[1]
    except IndexError as e:
        print(e)
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
