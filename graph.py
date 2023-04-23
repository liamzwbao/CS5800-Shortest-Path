from __future__ import annotations

from math import radians, sin, cos, sqrt, asin


class Vertex:

    def __init__(self, val: str, lat: float, lon: float) -> None:
        self.val = val
        self.lat = lat
        self.lon = lon

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
        self.src = src
        self.dst = dst
        self.weight = weight

    def __hash__(self) -> int:
        return hash((self.src, self.dst))

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Edge) and o.src == self.src and o.dst == self.dst and o.weight == self.weight

    def __str__(self) -> str:
        return f"{self.src.val} to {self.dst.val}: {self.weight}"


class Graph:

    def __init__(self) -> None:
        self.adj_list = {}

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


def load_graph() -> Graph:
    v1 = Vertex('MHK', 39.140998840332, -96.6707992553711)
    v2 = Vertex('EUG', 44.1245994567871, -123.21199798584)
    v3 = Vertex('RDM', 44.2541008, -121.1500015)
    v4 = Vertex('MFR', 42.3741989135742, -122.873001098633)
    v5 = Vertex('SEA', 47.4490013122559, -122.30899810791)
    vertices = [v1, v2, v3, v4, v5]
    e1 = Edge(v2, v3, 103)
    e2 = Edge(v4, v3, 156)
    e3 = Edge(v5, v3, 228)
    edges = [e1, e2, e3]
    graph = Graph()
    graph.build_graph(vertices, edges)
    return graph


def print_graph(graph: Graph):
    for vertex, neighs in graph.adj_list.items():
        print(f"{str(vertex)}: {[(v[0].val, v[1]) for v in neighs]}")


if __name__ == "__main__":
    print_graph(load_graph())
