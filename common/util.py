from typing import Optional, List

from common.graph import Vertex


def shortest_path(prev_vertices: dict[Vertex, Optional[Vertex]], dst: Vertex) -> List[Vertex]:
    path = []
    cur_vertex = dst

    while cur_vertex is not None:
        path.append(cur_vertex)
        cur_vertex = prev_vertices.get(cur_vertex, None)

    return path[::-1]


def get_path(path: List[Vertex]) -> str:
    return ' -> '.join([v.val for v in path])


def print_path(path: List[Vertex]) -> None:
    src, dst = path[0], path[-1]
    print(f"Shortest path from {src.val} to {dst.val}: {get_path(path)}")


def print_distance(distance: float) -> None:
    print(f"Distance: {distance:.2f} miles")


def print_elapsed_time(elapsed_time: float) -> None:
    print(f"Elapsed time: {elapsed_time:.4f} seconds\n")


def print_result(path: List[Vertex], distance: float, elapsed_time: float) -> None:
    print_path(path)
    print_distance(distance)
    print_elapsed_time(elapsed_time)
