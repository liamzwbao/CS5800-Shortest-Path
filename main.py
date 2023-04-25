import random
import time

from algorithms import dijkstra, astar
from common.graph import load_graph
from common.util import print_elapsed_time

if __name__ == '__main__':
    graph, vertices, _ = load_graph()
    iterations = 1000
    path_pairs = [(random.choice(list(vertices.keys())), random.choice(list(vertices.keys())))] * iterations

    print("Using heap-based Dijkstra:")
    start_time = time.time()
    for src_airport, dst_airport in path_pairs:
        dijkstra.dijkstra_heap(src_airport, dst_airport, vertices, graph)
    elapsed_time = time.time() - start_time
    print_elapsed_time(elapsed_time)

    print("Using unsorted list-based Dijkstra:")
    start_time = time.time()
    for src_airport, dst_airport in path_pairs:
        dijkstra.dijkstra_unsorted_list(src_airport, dst_airport, vertices, graph)
    elapsed_time = time.time() - start_time
    print_elapsed_time(elapsed_time)

    print("Using heap-based A* Search:")
    start_time = time.time()
    for src_airport, dst_airport in path_pairs:
        astar.astar_heap(src_airport, dst_airport, vertices, graph)
    elapsed_time = time.time() - start_time
    print_elapsed_time(elapsed_time)

    print("Using unsorted list-based A* Search:")
    start_time = time.time()
    for src_airport, dst_airport in path_pairs:
        astar.astar_unsorted_list(src_airport, dst_airport, vertices, graph)
    elapsed_time = time.time() - start_time
    print_elapsed_time(elapsed_time)
