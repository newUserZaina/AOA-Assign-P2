import heapq
from collections import defaultdict, deque

class Vertex:
    def __init__(self, data):
        self.data = data
        self.edges = []

    def add_edge(self, end_vertex, dist_weight, dur_weight):
        self.edges.append(Edge(self, end_vertex, dist_weight, dur_weight))

    def remove_edge(self, end_vertex):
        self.edges = [edge for edge in self.edges if edge.end != end_vertex]

    def get_edges(self):
        return self.edges

class Edge:
    def __init__(self, start, end, dist_weight, dur_weight):
        self.start = start
        self.end = end
        self.dist_weight = dist_weight
        self.dur_weight = dur_weight

class Graph:
    def __init__(self, is_weighted, is_directed):
        self.vertices = []
        self.is_weighted = is_weighted
        self.is_directed = is_directed

    def add_vertex(self, data):
        new_vertex = Vertex(data)
        self.vertices.append(new_vertex)
        return new_vertex

    def add_edge(self, vertex1, vertex2, dist_weight=None, dur_weight=None):
        if not self.is_weighted:
            dist_weight = None
            dur_weight = None

        vertex1.add_edge(vertex2, dist_weight, dur_weight)
        if not self.is_directed:
            vertex2.add_edge(vertex1, dist_weight, dur_weight)

    def remove_edge(self, vertex1, vertex2):
        vertex1.remove_edge(vertex2)
        if not self.is_directed:
            vertex2.remove_edge(vertex1)

    def remove_vertex(self, vertex):
        self.vertices.remove(vertex)

    def get_vertex_by_value(self, value):
        for v in self.vertices:
            if v.data == value:
                return v
        return None

class QueueObj:
    def __init__(self, vertex, priority):
        self.vertex = vertex
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority

def navigation(graph, origin, by_distance):
    distances = defaultdict(lambda: float('inf'))
    durations = defaultdict(lambda: float('inf'))
    previous = defaultdict(lambda: None)
    queue = []

    heapq.heappush(queue, QueueObj(origin, 0))
    distances[origin.data] = 0
    durations[origin.data] = 0

    while queue:
        current = heapq.heappop(queue).vertex
        for edge in current.get_edges():
            alternative_dist = distances[current.data] + (edge.dist_weight if edge.dist_weight else 0)
            alternative_dur = durations[current.data] + (edge.dur_weight if edge.dur_weight else 0)
            neighbor_value = edge.end.data

            if by_distance and alternative_dist < distances[neighbor_value]:
                distances[neighbor_value] = alternative_dist
                previous[neighbor_value] = current
                heapq.heappush(queue, QueueObj(edge.end, alternative_dist))
            elif not by_distance and alternative_dur < durations[neighbor_value]:
                durations[neighbor_value] = alternative_dur
                previous[neighbor_value] = current
                heapq.heappush(queue, QueueObj(edge.end, alternative_dur))

    return distances, durations, previous

def shortest_path(graph, origin_vertex, target_vertex, by_distance):
    distances, durations, previous = navigation(graph, origin_vertex, by_distance)

    if by_distance and distances[target_vertex.data] == float('inf'):
        print(f"No path exists between {origin_vertex.data} and {target_vertex.data}")
        return {
            "status": "error",
            "message": f"No path exists between {origin_vertex.data} and {target_vertex.data}"
        }
    elif not by_distance and durations[target_vertex.data] == float('inf'):
        print(f"No path exists between {origin_vertex.data} and {target_vertex.data}")
        return {
            "status": "error",
            "message": f"No path exists between {origin_vertex.data} and {target_vertex.data}"
        }

    # Reconstruct the path
    path = []
    v = target_vertex
    while v is not None:
        path.insert(0, v.data)
        v = previous[v.data]

    print(f"Path calculated: {path}")
    print(f"Distance: {distances[target_vertex.data]} km")
    print(f"Duration: {durations[target_vertex.data]} mins")

    return {
        "status": "success",
        "data": {
            "path": path,
            "distance": distances[target_vertex.data],
            "duration": durations[target_vertex.data]
        }
    }

def main():
    test_graph = Graph(True, True)

    a = test_graph.add_vertex("Montego Bay")
    b = test_graph.add_vertex("Lucea")
    c = test_graph.add_vertex("Savanna la Mar")
    d = test_graph.add_vertex("Black River")
    e = test_graph.add_vertex("Santa Cruz")
    f = test_graph.add_vertex("Falmouth")
    g = test_graph.add_vertex("St. Ann's Bay")
    h = test_graph.add_vertex("Ocho Rios")
    j = test_graph.add_vertex("Christiana")
    k = test_graph.add_vertex("Mandeville")
    l = test_graph.add_vertex("May Pen")
    m = test_graph.add_vertex("Alley")
    n = test_graph.add_vertex("Port Maria")
    o = test_graph.add_vertex("Annotto Bay")
    p = test_graph.add_vertex("Ewarton")
    q = test_graph.add_vertex("Spanish Town")
    r = test_graph.add_vertex("Port Royal")
    s = test_graph.add_vertex("Kingston")
    t = test_graph.add_vertex("Port Antonio")
    u = test_graph.add_vertex("Morant Point")
    v = test_graph.add_vertex("Negril")

    test_graph.add_edge(s, u, 87.4, 105)
    test_graph.add_edge(s, t, 92.2, 124)
    test_graph.add_edge(s, o, 46.8, 73)
    test_graph.add_edge(s, q, 20.2, 28)
    test_graph.add_edge(s, r, 26.3, 32)
    test_graph.add_edge(u, t, 67.7, 83)
    test_graph.add_edge(t, o, 45.5, 52)
    test_graph.add_edge(o, n, 25.2, 27)
    test_graph.add_edge(n, h, 31.4, 32)
    test_graph.add_edge(h, g, 12.1, 14)
    test_graph.add_edge(g, f, 57.1, 57)
    test_graph.add_edge(f, a, 34.9, 36)
    test_graph.add_edge(a, b, 36.5, 37)
    test_graph.add_edge(b, v, 39.6, 37)
    test_graph.add_edge(q, m, 54.7, 68)
    test_graph.add_edge(m, e, 93.1, 106)
    test_graph.add_edge(e, d, 28.9, 28)
    test_graph.add_edge(d, c, 47.3, 47)
    test_graph.add_edge(c, v, 28.1, 28)
    test_graph.add_edge(q, p, 30.5, 43)
    test_graph.add_edge(p, h, 46.8, 48)
    test_graph.add_edge(p, j, 77.6, 117)
    test_graph.add_edge(q, l, 34.6, 37)
    test_graph.add_edge(l, m, 24.5, 45)
    test_graph.add_edge(l, k, 39.4, 44)
    test_graph.add_edge(k, j, 20.9, 32)
    test_graph.add_edge(j, f, 70.2, 93)
    test_graph.add_edge(j, e, 51.2, 54)
    test_graph.add_edge(c, a, 49.5, 59)

    origin_input = input("Enter origin: ")
    destination_input = input("Enter destination: ")
    by_distance = input("Optimize by distance (True) or time (False): ").lower() == 'true'

    origin = test_graph.get_vertex_by_value(origin_input)
    destination = test_graph.get_vertex_by_value(destination_input)

    if origin and destination:
        shortest_path(test_graph, origin, destination, by_distance)
    else:
        print("Invalid locations entered.")

if __name__ == "__main__":
    main()