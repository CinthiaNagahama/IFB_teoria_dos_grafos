#!/usr/bin/env python3

import sys
from typing import Optional
from graph import Graph, Edge
from os import path


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

        g_matrix = Graph("matriz", vertices_num)
        g_list = Graph("lista", vertices_num)

        for edge in edges:
            g_matrix.insert_relation(edge)
            g_list.insert_relation(edge)

        out_path = path.join("..", "out")

        g_matrix.out_graph(out_path)
        g_list.out_graph(out_path)

        g_matrix.breadth_first_search("1", out_path)
        g_list.breadth_first_search("1", out_path)

        g_list.depth_first_search("1", out_path)
        g_matrix.depth_first_search("1", out_path)

        print("Matriz: ")
        print(g_matrix.find_connected_components())

        print("Lista: ")
        print(g_list.find_connected_components())
