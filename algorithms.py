from tkinter import simpledialog
from collections import deque
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
