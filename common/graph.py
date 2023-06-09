from __future__ import annotations

from math import radians, sin, cos, sqrt, asin
import os
import pandas as pd


class Vertex:

    def __init__(self, val: str, lat: float, lon: float) -> None:
        self.val: str = val
        self.lat: float = lat
        self.lon: float = lon

    def __hash__(self) -> int:
        return hash(self.val)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Vertex) and o.val == self.val

    def __str__(self) -> str:
        return f"{self.val} ({self.lat}, {self.lon})"

    def distance_to(self, to: Vertex) -> float:
        lat1 = radians(self.lat)
        lat2 = radians(to.lat)
        lon1 = radians(self.lon)
        lon2 = radians(to.lon)
        d_lat = lat2 - lat1
        d_lon = lon2 - lon1
        return asin(sqrt(sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2)) * 2 * 3963


class Edge:

    def __init__(self, src: Vertex, dst: Vertex, weight: float = 1) -> None:
        self.src: Vertex = src
        self.dst: Vertex = dst
        self.weight: float = weight

    def __hash__(self) -> int:
        return hash((self.src, self.dst))

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Edge) and o.src.__eq__(self.src) and o.dst.__eq__(self.dst) and o.weight == self.weight

    def __str__(self) -> str:
        return f"{self.src.val} to {self.dst.val}: {self.weight}"


class Graph:

    def __init__(self) -> None:
        self.adj_list: dict[Vertex, list[tuple[Vertex, float]]] = {}

    def add_vertex(self, vertex: Vertex) -> None:
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, edge: Edge) -> None:
        self.add_vertex(edge.src)
        self.add_vertex(edge.dst)
        self.adj_list[edge.src].append((edge.dst, edge.weight))

    def build_graph(self, vertices: list[Vertex], edges: list[Edge]) -> None:
        for v in vertices:
            self.add_vertex(v)
        for e in edges:
            self.add_edge(e)


def get_airports() -> dict[str, Vertex]:
    dir_name = os.path.dirname(__file__)
    file_name = os.path.join(dir_name, '../data-processing/airport-geo-location-data.pkl')
    airports_data = pd.read_pickle(file_name)
    return {val: Vertex(val, lat, lon) for val, lat, lon in airports_data.values.tolist()}


def get_first_n_airports(n: int) -> dict[str, Vertex]:
    dir_name = os.path.dirname(__file__)
    file_name = os.path.join(dir_name, '../data-processing/airport-geo-location-data.pkl')
    airports_data = pd.read_pickle(file_name).head(n)
    return {val: Vertex(val, lat, lon) for val, lat, lon in airports_data.values.tolist()}


def get_flights(airports: dict[str, Vertex]) -> dict[str, Edge]:
    dir_name = os.path.dirname(__file__)
    file_name = os.path.join(dir_name, '../data-processing/airport-distance-data.pkl')
    flights_data = pd.read_pickle(file_name)
    return {f"{src}->{dst}": Edge(airports[src], airports[dst], airports[src].distance_to(airports[dst])) for
            src, dst, _ in flights_data.values.tolist()}


def get_flights_limited_airports(airports: dict[str, Vertex]) -> list[Edge]:
    dir_name = os.path.dirname(__file__)
    file_name = os.path.join(dir_name, '../data-processing/airport-distance-data.pkl')
    flights_data = pd.read_pickle(file_name)
    return [Edge(airports[src], airports[dst], airports[src].distance_to(airports[dst])) for src, dst, _ in
            flights_data.values.tolist() if src in airports and dst in airports]


def load_graph() -> tuple[Graph, dict[str, Vertex], dict[str, Edge]]:
    vertices = get_airports()
    edges = get_flights(vertices)
    graph = Graph()
    graph.build_graph(list(vertices.values()), list(edges.values()))
    return graph, vertices, edges


def print_graph(graph: Graph):
    for vertex, neighs in graph.adj_list.items():
        print(f"{str(vertex)}: {[(v[0].val, v[1]) for v in neighs]}")


if __name__ == "__main__":
    print_graph(load_graph()[0])
