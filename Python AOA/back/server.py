from flask import Flask, request, jsonify
from flask_cors import CORS
from graph import Graph, Vertex, shortest_path

app = Flask(__name__)
CORS(app)

# Initialize the graph
def initialize_graph():
    test_graph = Graph(True, True)

    # Add vertices and edges (same as in graph.py)
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

    return test_graph

# Initialize the graph
test_graph = initialize_graph()

@app.route('/calculate-route', methods=['POST'])
def calculate_route():
    # Get JSON data from the front-end
    data = request.json
    origin_name = data.get('origin')
    destination_name = data.get('destination')
    avoid = data.get('avoid', [])
    by_distance = data.get('byDistance', True)

    # Debugging: Log the values received from the front-end
    print(f"Received request - Origin: {origin_name}, Destination: {destination_name}, By Distance: {by_distance}")

    # Find the origin and destination vertices
    origin = test_graph.get_vertex_by_value(origin_name)
    destination = test_graph.get_vertex_by_value(destination_name)

    if origin is None or destination is None:
        print(f"Invalid origin or destination - Origin: {origin_name}, Destination: {destination_name}")
        return jsonify({
            "status": "error",
            "message": "Invalid origin or destination",
            "data": None
        })

    # Calculate the shortest path
    try:
        result = shortest_path(test_graph, origin, destination, by_distance)

        if result["status"] == "success":
            response = {
                "status": "success",
                "message": "Route calculated successfully",
                "data": {
                    "origin": origin_name,
                    "destination": destination_name,
                    "distance": result["data"]["distance"],
                    "duration": result["data"]["duration"],
                    "path": result["data"]["path"],
                    "avoid": avoid
                }
            }
        else:
            response = {
                "status": "error",
                "message": result["message"],
                "data": None
            }
    except Exception as e:
        print(f"Error calculating route: {str(e)}")
        response = {
            "status": "error",
            "message": f"Error calculating route: {str(e)}",
            "data": None
        }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)