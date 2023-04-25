import random
import time

import matplotlib.pyplot as plt

from algorithms.astar import astar_heap, astar_unsorted_list
from algorithms.dijkstra import dijkstra_heap, dijkstra_unsorted_list
from algorithms.floyd_warshall import floyd_warshall
from common.graph import Graph, get_first_n_airports, \
    get_flights_limited_airports, Edge


def draw_line_graph_same_datapoint():
    vertices = get_first_n_airports(100)
    edges = get_flights_limited_airports(vertices)

    # Convert the Edge objects to use Vertex objects as the src and dst attributes
    edges = [Edge(vertices[edge.src.val], vertices[edge.dst.val], edge.weight) for edge in
             edges]

    graph = Graph()
    graph.build_graph(vertices.values(), edges)

    iterations = list(range(1, 101))
    dijkstra_heap_times = []
    dijkstra_unsorted_times = []
    astar_heap_times = []
    astar_unsorted_times = []
    floyd_warshall_times = []

    # Run Floyd-Warshall once and store the result
    floyd_warshall_result = floyd_warshall(vertices, edges)

    # Run algorithms and measure time
    for _ in iterations:
        src, dst = random.choice(list(vertices.keys())), random.choice(
            list(vertices.keys()))

        start = time.time()
        dijkstra_heap(src, dst, vertices, graph)
        dijkstra_heap_times.append(time.time() - start)

        start = time.time()
        dijkstra_unsorted_list(src, dst, vertices, graph)
        dijkstra_unsorted_times.append(time.time() - start)

        start = time.time()
        astar_heap(src, dst, vertices, graph)
        astar_heap_times.append(time.time() - start)

        start = time.time()
        astar_unsorted_list(src, dst, vertices, graph)
        astar_unsorted_times.append(time.time() - start)

        # Measure the time taken to access the distance from the precomputed result
        start = time.time()
        _ = floyd_warshall_result[src][dst]
        floyd_warshall_times.append(time.time() - start)

    # Plot results
    plt.plot(iterations, dijkstra_heap_times, label="Dijkstra Heap")
    plt.plot(iterations, dijkstra_unsorted_times, label="Dijkstra Unsorted List")
    plt.plot(iterations, astar_heap_times, label="A* Heap")
    plt.plot(iterations, astar_unsorted_times, label="A* Unsorted List")
    plt.plot(iterations, floyd_warshall_times, label="Floyd-Warshall")

    plt.xlabel("Iterations")
    plt.ylabel("Elapsed Time (s)")
    plt.title("Algorithms Performance Comparison")
    plt.legend()
    plt.grid()
    plt.show()


def draw_line_graph(num_iterations: int) -> None:
    datapoints = list(range(50, 451, 50))
    dijkstra_heap_avg_times = []
    dijkstra_unsorted_avg_times = []
    astar_heap_avg_times = []
    astar_unsorted_avg_times = []
    floyd_warshall_avg_times = []

    for num_airports in datapoints:
        vertices = get_first_n_airports(num_airports)
        edges = get_flights_limited_airports(vertices)

        edges = [Edge(vertices[edge.src.val], vertices[edge.dst.val], edge.weight) for
                 edge in edges]

        graph = Graph()
        graph.build_graph(vertices.values(), edges)

        dijkstra_heap_times = []
        dijkstra_unsorted_times = []
        astar_heap_times = []
        astar_unsorted_times = []
        floyd_warshall_times = []

        # Run Floyd-Warshall once and store the result
        start_fw = time.time()
        floyd_warshall_result = floyd_warshall(vertices, edges)
        floyd_warshall_times.append(time.time() - start_fw)

        for _ in range(num_iterations - 1):
            src, dst = random.choice(list(vertices.keys())), random.choice(
                list(vertices.keys()))

            start = time.time()
            dijkstra_heap(src, dst, vertices, graph)
            dijkstra_heap_times.append(time.time() - start)

            start = time.time()
            dijkstra_unsorted_list(src, dst, vertices, graph)
            dijkstra_unsorted_times.append(time.time() - start)

            start = time.time()
            astar_heap(src, dst, vertices, graph)
            astar_heap_times.append(time.time() - start)

            start = time.time()
            astar_unsorted_list(src, dst, vertices, graph)
            astar_unsorted_times.append(time.time() - start)

            start = time.time()
            _ = floyd_warshall_result[src][dst]
            floyd_warshall_times.append(time.time() - start)

        dijkstra_heap_avg_times.append(sum(dijkstra_heap_times) / num_iterations)
        dijkstra_unsorted_avg_times.append(sum(dijkstra_unsorted_times) / num_iterations)
        astar_heap_avg_times.append(sum(astar_heap_times) / num_iterations)
        astar_unsorted_avg_times.append(sum(astar_unsorted_times) / num_iterations)
        floyd_warshall_avg_times.append(sum(floyd_warshall_times) / num_iterations)

    plt.plot(datapoints, dijkstra_heap_avg_times, label="Dijkstra Heap")
    plt.plot(datapoints, dijkstra_unsorted_avg_times, label="Dijkstra Unsorted List")
    plt.plot(datapoints, astar_heap_avg_times, label="A* Heap")
    plt.plot(datapoints, astar_unsorted_avg_times, label="A* Unsorted List")
    plt.plot(datapoints, floyd_warshall_avg_times, label="Floyd-Warshall")

    plt.xlabel("Data Points (Number of Airports)")
    plt.ylabel("Average Elapsed Time (s)")
    plt.title("Algorithms Performance Comparison")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    draw_line_graph_same_datapoint()
    draw_line_graph(100)
    draw_line_graph(500)
    draw_line_graph(1000)
