#!/usr/bin/env python3

from os import path
import sys
from typing import Optional, Tuple
from graph import Graph, Edge


def validate_args() -> Optional[Tuple[str, str]]:
    try:
        text_arg = sys.argv[1]
        graph_type_arg = sys.argv[2]

        if not path.exists(text_arg):
            raise FileNotFoundError

        assert graph_type_arg == "matriz" or graph_type_arg == "lista"

    except IndexError:
        print("Há argumento(s) faltando!")
    except FileNotFoundError:
        print("Arquivo de texto de entrada inválido")
    except AssertionError:
        print("Tipo de grafo inválido!")
    else:
        return text_arg, graph_type_arg


if __name__ == "__main__":

    args = validate_args()

    if args is None:
        exit(0)

    text_arg, graph_type = args

    with open(text_arg) as text_file:
        vertices_num = int(text_file.readline())
        edges = text_file.readlines()
        edges = [Edge(*edge.strip().split()) for edge in edges]

        graph = Graph(graph_type, vertices_num)

        for edge in edges:
            graph.insert_relation(edge)

        graph.out_graph(path.join("..", "out"))
