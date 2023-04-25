import heapq
import time
from math import inf

from common.graph import Vertex, Graph, load_graph
from common.util import shortest_path, print_result


def get_heuristic(src: Vertex, dst: Vertex) -> float:
    return src.distance_to(dst)


def astar_heap(src: str, dst: str, vertices: dict[str, Vertex], graph: Graph) -> tuple[float, list[Vertex]]:
    src_vertex = vertices[src]
    dst_vertex = vertices[dst]

    initial_h = get_heuristic(src_vertex, dst_vertex)
    g_scores: dict[Vertex, float] = {src_vertex: 0}
    f_scores: dict[Vertex, float] = {src_vertex: initial_h}
    heap: list[tuple[float, str, Vertex]] = [(f_scores[src_vertex], src_vertex.val, src_vertex)]
    open_set: set[Vertex] = {src_vertex}
    close_set: set[Vertex] = set()
    prev_vertices: dict[Vertex, Vertex] = {}

    while heap:
        _, _, cur_vertex = heapq.heappop(heap)

        if cur_vertex == dst_vertex:
            break
        close_set.add(cur_vertex)

        for neigh, weight in graph.adj_list[cur_vertex]:
            cur_g_score = g_scores[cur_vertex] + weight
            if neigh in close_set and cur_g_score >= g_scores[neigh]:
                continue

            if neigh not in open_set or cur_g_score < g_scores[neigh]:
                g_scores[neigh] = cur_g_score
                f_scores[neigh] = cur_g_score + get_heuristic(neigh, dst_vertex)
                heapq.heappush(heap, (f_scores[neigh], neigh.val, neigh))
                open_set.add(neigh)
                prev_vertices[neigh] = cur_vertex

    path = shortest_path(prev_vertices, dst_vertex)
    return g_scores.get(dst_vertex, inf), path


def astar_unsorted_list(src: str, dst: str, vertices: dict[str, Vertex], graph: Graph) -> tuple[float, list[Vertex]]:
    src_vertex = vertices[src]
    dst_vertex = vertices[dst]

    initial_h = get_heuristic(src_vertex, dst_vertex)
    g_scores: dict[Vertex, float] = {src_vertex: 0}
    f_scores: dict[Vertex, float] = {src_vertex: initial_h}
    unvisited: list[Vertex] = [src_vertex]
    open_set: set[Vertex] = {src_vertex}
    close_set: set[Vertex] = set()
    prev_vertices: dict[Vertex, Vertex] = {}

    while unvisited:
        cur_vertex = min(unvisited, key=lambda v: f_scores[v])
        unvisited.remove(cur_vertex)

        if cur_vertex == dst_vertex:
            break
        close_set.add(cur_vertex)

        for neigh, weight in graph.adj_list[cur_vertex]:
            cur_g_score = g_scores[cur_vertex] + weight
            if neigh in close_set and cur_g_score >= g_scores[neigh]:
                continue

            if neigh not in open_set or cur_g_score < g_scores[neigh]:
                g_scores[neigh] = cur_g_score
                f_scores[neigh] = cur_g_score + get_heuristic(neigh, dst_vertex)
                unvisited.append(neigh)
                open_set.add(neigh)
                prev_vertices[neigh] = cur_vertex

    path = shortest_path(prev_vertices, dst_vertex)
    return g_scores.get(dst_vertex, inf), path


def run(src: str, dst: str, graph: Graph, vertices: dict[str, Vertex]) -> None:
    if src not in vertices or dst not in vertices:
        print("Start or end vertex not found.")
        return

    # Using heap-based A* Search
    start_time = time.time()
    distance, path = astar_heap(src, dst, vertices, graph)
    elapsed_time = time.time() - start_time

    print("Using heap-based A* Search:")
    print_result(path, distance, elapsed_time)

    # Using unsorted list-based A* Search
    start_time = time.time()
    distance, path = astar_unsorted_list(src, dst, vertices, graph)
    elapsed_time = time.time() - start_time

    print("Using unsorted list-based A* Search:")
    print_result(path, distance, elapsed_time)


if __name__ == '__main__':
    src_airport = 'SFO'
    dst_airport = 'JFK'
    run(src_airport, dst_airport, *load_graph()[:2])
