from tkinter import simpledialog
from collections import deque
import heapq
import time

def bfs_level_by_level(canvas, graph):
    if graph.node_count == 0:
        return

    try:
        start_node = simpledialog.askinteger("BFS Start", "Enter start node ID:", minvalue=0, maxvalue=graph.node_count - 1)
        if start_node is None or start_node not in graph.nodes:
            return
    except:
        return

    def highlight(node_id, color):
        canvas.itemconfig(graph.node_id_to_canvas[node_id], fill=color)

    def reset_all():
        for nid in graph.node_id_to_canvas:
            highlight(nid, "lightblue")

    visited = set()
    queue = deque()
    queue.append(start_node)
    visited.add(start_node)

    while queue:
        level_size = len(queue)
        current_level = list(queue)
        for _ in range(level_size):
            u = queue.popleft()
            for v, _ in graph.adj[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        for node in current_level:
            highlight(node, "green")
        canvas.update()
        time.sleep(0.5)

    time.sleep(0.5)
    reset_all()

def dfs_visual(canvas, graph):
    if graph.node_count == 0:
        return

    try:
        start_node = simpledialog.askinteger("DFS Start", "Enter start node ID:", minvalue=0, maxvalue=graph.node_count - 1)
        if start_node is None or start_node not in graph.nodes:
            return
    except:
        return

    def highlight(node_id, color):
        canvas.itemconfig(graph.node_id_to_canvas[node_id], fill=color)

    def reset_all():
        for nid in graph.node_id_to_canvas:
            highlight(nid, "lightblue")

    visited = set()

    def dfs(u):
        visited.add(u)
        highlight(u, "brown")
        canvas.update()
        time.sleep(0.5)
        for v, _ in graph.adj[u]:
            if v not in visited:
                dfs(v)
        highlight(u, "green")
        canvas.update()
        time.sleep(0.3)

    dfs(start_node)
    time.sleep(0.5)
    reset_all()

def dijkstra_visual(canvas, graph, is_weighted):
    if graph.node_count == 0:
        return

    if not is_weighted:
        canvas.delete("info")
        canvas.create_text(400, 30, text="Graph is not weighted.", font=("Arial", 16), fill="red", tag="info")
        canvas.update()
        time.sleep(2)
        canvas.delete("info")
        return


    try:
        start = simpledialog.askinteger("Dijkstra Start", "Enter start node ID:", minvalue=0, maxvalue=graph.node_count - 1)
        if start is None or start not in graph.nodes:
            return
    except:
        return

    dist = {node: float('inf') for node in graph.nodes}
    dist[start] = 0

    def update_distance_texts():
        canvas.delete("dist")
        for node_id, (x, y) in graph.nodes.items():
            d = dist[node_id]
            text = str(d if d != float('inf') else -1)
            canvas.create_text(x, y - 30, text=text, font=("Arial", 12), fill="red", tag="dist")

    def highlight(node_id, color):
        canvas.itemconfig(graph.node_id_to_canvas[node_id], fill=color)

    def reset_all():
        for nid in graph.node_id_to_canvas:
            highlight(nid, "lightblue")
        canvas.delete("dist")

    pq = [(0, start)]
    visited = set()
    reset_all()
    update_distance_texts()
    canvas.update()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        highlight(u, "green")
        update_distance_texts()
        canvas.update()
        time.sleep(2)  # Slowed down from 0.5

        for v, w in graph.adj[u]:
            if dist[v] > d + w:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
                highlight(v, "brown")
                update_distance_texts()
                canvas.update()
                time.sleep(3)  # Slowed down from 0.3


    time.sleep(4)
    reset_all()

def topo_sort_visual(canvas, graph):
    if graph.node_count == 0:
        return

    if not graph.directed_var.get():
        canvas.create_text(400, 20, text="Topological sort only works on directed graphs.", fill="red", font=("Arial", 12), tag="error")
        canvas.update()
        time.sleep(2)
        canvas.delete("error")
        return


    in_degree = {node: 0 for node in graph.nodes}
    for u in graph.nodes:
        for v, _ in graph.adj[u]:
            in_degree[v] += 1

    queue = deque([u for u in graph.nodes if in_degree[u] == 0])
    topo_order = []

    def highlight(node_id, color):
        canvas.itemconfig(graph.node_id_to_canvas[node_id], fill=color)

    def reset_all():
        for nid in graph.node_id_to_canvas:
            highlight(nid, "lightblue")

    reset_all()
    canvas.update()
    time.sleep(0.5)

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        highlight(u, "green")
        canvas.update()
        time.sleep(0.6)

        for v, _ in graph.adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(topo_order) < graph.node_count:
        canvas.create_text(400, 20, text="Cycle detected: topological sort not possible.", fill="red", font=("Arial", 20), tag="error")
        canvas.update()
        time.sleep(5)
        canvas.delete("error")
    else:
        x_offset = 50
        for idx, node_id in enumerate(topo_order):
            x, y = graph.nodes[node_id]
            canvas.create_text(x, y - 30, text=str(idx), fill="purple", font=("Arial", 20), tag="order")
        canvas.update()
        time.sleep(2)
        canvas.delete("order")

    reset_all()
