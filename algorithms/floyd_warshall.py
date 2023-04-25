import time

from pandas import DataFrame

from common.graph import Vertex, Edge, get_first_n_airports, get_flights_limited_airports, get_airports


def floyd_warshall(vertex_dict: dict[str, Vertex], edge_list: list[Edge]) -> dict[dict]:

    # create a 2D distance dictionary
    # dist[A][B] = distance between airport A and B (A and B are strings)
    # distance between the airport and itself is 0
    dist = {src: {dest: 0 if dest == src else float("inf") for dest in vertex_dict}
            for src in vertex_dict}

    # initialize the distance dictionary using edge values
    for edge in edge_list:
        src = edge.src.val
        dst = edge.dst.val
        weight = edge.weight
        if weight < dist[src][dst]:
            dist[src][dst] = weight

    # run nested loops to update distance dictionary that takes into account of
    # the presence of intermediate airports
    for k in vertex_dict:
        for i in vertex_dict:
            for j in vertex_dict:
                dist[i][j] = min(dist[i][k]+dist[k][j], dist[i][j])

    return dist


if __name__ == '__main__':
    # 10 airports
    vertex_dict_10 = get_first_n_airports(10)
    edge_list_10 = get_flights_limited_airports(vertex_dict_10)
    start_time = time.time()
    print(DataFrame(floyd_warshall(vertex_dict_10, edge_list_10)))
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")

    # 50 airports
    vertex_dict_50 = get_first_n_airports(50)
    edge_list_50 = get_flights_limited_airports(vertex_dict_50)
    start_time = time.time()
    print(DataFrame(floyd_warshall(vertex_dict_50, edge_list_50)))
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")

    # 100 airports
    vertex_dict_100 = get_first_n_airports(100)
    edge_list_100 = get_flights_limited_airports(vertex_dict_100)
    start_time = time.time()
    print(DataFrame(floyd_warshall(vertex_dict_100, edge_list_100)))
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")

    # All airports
    vertex_dict = get_airports()
    edge_list = get_flights_limited_airports(vertex_dict)
    start_time = time.time()
    print(DataFrame(floyd_warshall(vertex_dict, edge_list)))
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.4f} seconds")
