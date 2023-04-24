import heapq
import time
from typing import List, Tuple

from common.graph import Vertex, Graph, load_graph, Edge
from common.util import shortest_path, print_result


def dijkstra_heap(src: str, dst: str, vertices: dict[str, Vertex], graph: Graph) -> Tuple[
    float, List[Vertex]]:
    start_vertex = vertices[src]
    end_vertex = vertices[dst]

    distances = {vertex: float("inf") for vertex in graph.adj_list}
    distances[start_vertex] = 0
    prev_vertices = {vertex: None for vertex in graph.adj_list}
    priority_queue = [(0, start_vertex.val, start_vertex)]

    while priority_queue:
        cur_distance, _, cur_vertex = heapq.heappop(priority_queue)

        if cur_distance > distances[cur_vertex]:
            continue

        for neigh, edge_weight in graph.adj_list[cur_vertex]:
            new_distance = cur_distance + edge_weight

            if new_distance < distances[neigh]:
                distances[neigh] = new_distance
                prev_vertices[neigh] = cur_vertex
                heapq.heappush(priority_queue, (new_distance, neigh.val, neigh))

    path = shortest_path(prev_vertices, end_vertex)
    return distances.get(end_vertex, float('inf')), path


def dijkstra_unsorted_list(src: str, dst: str, vertices: dict[str, Vertex],
                           graph: Graph) -> Tuple[float, List[Vertex]]:
    start_vertex = vertices[src]
    end_vertex = vertices[dst]

    distances = {vertex: float("inf") for vertex in graph.adj_list}
    distances[start_vertex] = 0
    prev_vertices = {vertex: None for vertex in graph.adj_list}

    unvisited = list(vertices.values())

    while unvisited:
        # Find the vertex with the minimum distance value
        cur_vertex = min(unvisited, key=lambda v: distances[v])
        unvisited.remove(cur_vertex)

        for neigh, edge_weight in graph.adj_list[cur_vertex]:
            new_distance = distances[cur_vertex] + edge_weight

            if new_distance < distances[neigh]:
                distances[neigh] = new_distance
                prev_vertices[neigh] = cur_vertex

    path = shortest_path(prev_vertices, end_vertex)
    return distances.get(end_vertex, float('inf')), path


def run(src: str, dst: str, graph: Graph, vertices: dict[str, Vertex]) -> None:
    if src not in vertices or dst not in vertices:
        print("Start or end vertex not found.")
        return

    # Using heap-based Dijkstra
    start_time = time.time()
    distance, path = dijkstra_heap(src, dst, vertices, graph)
    elapsed_time = time.time() - start_time

    print("Using heap-based Dijkstra:")
    print_result(path, distance, elapsed_time)

    # Using unsorted list-based Dijkstra
    start_time = time.time()
    distance, path = dijkstra_unsorted_list(src, dst, vertices, graph)
    elapsed_time = time.time() - start_time

    print("Using unsorted list-based Dijkstra:")
    print_result(path, distance, elapsed_time)


if __name__ == '__main__':
    src_airport = "SFO"
    dst_airport = "JFK"
    run(src_airport, dst_airport, *load_graph()[:2])
