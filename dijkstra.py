import heapq, time
from typing import List, Tuple, Optional
from graph import Vertex, Graph, get_airports, get_flights


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

    path = shortest_path(prev_vertices, start_vertex, end_vertex)
    return distances[end_vertex], path


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

    path = shortest_path(prev_vertices, start_vertex, end_vertex)
    return distances[end_vertex], path


def shortest_path(prev_vertices: dict[Vertex, Optional[Vertex]], start: Vertex,
                  end: Vertex) -> List[Vertex]:
    path = []
    cur_vertex = end

    while cur_vertex is not None:
        path.append(cur_vertex)
        cur_vertex = prev_vertices[cur_vertex]

    return path[::-1]


def main():
    vertices = get_airports()
    edges = get_flights(vertices)
    graph = Graph()
    graph.build_graph(vertices.values(), edges)

    src = "SFO"
    dst = "JFK"

    if src not in vertices or dst not in vertices:
        print("Start or end vertex not found.")
        return

    # Using heap-based Dijkstra
    start_time = time.time()
    distance, path = dijkstra_heap(src, dst, vertices, graph)
    elapsed_time = time.time() - start_time

    print("Using heap-based Dijkstra:")
    print(f"Shortest path from {src} to {dst}: {' -> '.join([v.val for v in path])}")
    print(f"Distance: {distance:.2f} miles")
    print(f"Elapsed time: {elapsed_time:.4f} seconds\n")

    # Using unsorted list-based Dijkstra
    start_time = time.time()
    distance, path = dijkstra_unsorted_list(src, dst, vertices, graph)
    elapsed_time = time.time() - start_time

    print("Using unsorted list-based Dijkstra:")
    print(f"Shortest path from {src} to {dst}: {' -> '.join([v.val for v in path])}")
    print(f"Distance: {distance:.2f} miles")
    print(f"Elapsed time: {elapsed_time:.4f} seconds")


if __name__ == "__main__":
    main()
