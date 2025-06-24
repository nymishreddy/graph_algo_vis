import tkinter as tk
from tkinter import simpledialog
import time
from collections import deque

# Initialize main window
root = tk.Tk()
root.title("Graph Algorithm Visualizer")

canvas = tk.Canvas(root, width=800, height=600, bg="white")
canvas.pack()

# Checkboxes for Directed and Weighted mode
directed_var = tk.BooleanVar()
weighted_var = tk.BooleanVar()

directed_check = tk.Checkbutton(root, text="Directed", variable=directed_var)
directed_check.pack(side=tk.LEFT)

weighted_check = tk.Checkbutton(root, text="Weighted", variable=weighted_var)
weighted_check.pack(side=tk.LEFT)

# Buttons
bfs_button = tk.Button(root, text="Run BFS")
bfs_button.pack(side=tk.LEFT)

# Graph Data
nodes = {}                # node_id -> (x, y)
node_canvas_ids = {}      # canvas_id -> node_id
node_id_to_canvas = {}    # node_id -> canvas_id (oval)
edges = []                # (u, v, weight)
adj = {}                  # node_id -> list of (neighbor, weight)

node_count = 0
selected_node = None

# Draw node and store canvas ID
def draw_node(x, y, node_id):
    r = 20
    oval_id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue")
    canvas.create_text(x, y, text=str(node_id), font=("Arial", 12))
    node_canvas_ids[oval_id] = node_id
    node_id_to_canvas[node_id] = oval_id
    nodes[node_id] = (x, y)
    adj[node_id] = []

# Add node on click or select for edge
def on_canvas_click(event):
    global node_count, selected_node

    clicked = canvas.find_overlapping(event.x, event.y, event.x, event.y)
    if not clicked:
        draw_node(event.x, event.y, node_count)
        node_count += 1
        selected_node = None
    else:
        node_id = node_canvas_ids.get(clicked[0], None)
        if node_id is None:
            return
        if selected_node is None:
            selected_node = node_id
        elif selected_node != node_id:
            u, v = selected_node, node_id
            x1, y1 = nodes[u]
            x2, y2 = nodes[v]

            if weighted_var.get():
                weight = simpledialog.askinteger("Edge Weight", f"Weight from {u} to {v}:", minvalue=1)
                if weight is None:
                    selected_node = None
                    return
            else:
                weight = 1

            # Adjust start and end to avoid overlapping arrows
            def adjust(x1, y1, x2, y2, offset=20):
                from math import atan2, cos, sin
                angle = atan2(y2 - y1, x2 - x1)
                return (x1 + offset * cos(angle), y1 + offset * sin(angle),
                        x2 - offset * cos(angle), y2 - offset * sin(angle))

            ax1, ay1, ax2, ay2 = adjust(x1, y1, x2, y2)

            if directed_var.get():
                canvas.create_line(ax1, ay1, ax2, ay2, width=2, fill="black", arrow=tk.LAST)
            else:
                canvas.create_line(x1, y1, x2, y2, width=2, fill="black")

            if weighted_var.get():
                label_x = (x1 + x2) // 2 + (y2 - y1) // 10
                label_y = (y1 + y2) // 2 - (x2 - x1) // 10
                canvas.create_text(label_x, label_y, text=str(weight), font=("Arial", 20), fill="black")

            adj[u].append((v, weight))
            if not directed_var.get():
                adj[v].append((u, weight))

            edges.append((u, v, weight))
            selected_node = None

canvas.bind("<Button-1>", on_canvas_click)

# Highlight a node
def highlight_node(node_id, color):
    canvas.itemconfig(node_id_to_canvas[node_id], fill=color)

# Reset all nodes to blue
def reset_node_colors():
    for node_id in node_id_to_canvas:
        highlight_node(node_id, "lightblue")

# Run BFS level-by-level
def run_bfs():
    if node_count == 0:
        return

    try:
        start_node = simpledialog.askinteger("BFS Start", "Enter start node ID (0-indexed):", minvalue=0, maxvalue=node_count - 1)
        if start_node is None or start_node not in nodes:
            return
    except:
        return

    visited = set()
    queue = deque()
    queue.append(start_node)
    visited.add(start_node)

    while queue:
        level_size = len(queue)
        current_level = list(queue)
        for _ in range(level_size):
            u = queue.popleft()
            for v, _ in adj[u]:
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        for node in current_level:
            highlight_node(node, "green")
        canvas.update()
        time.sleep(0.5)

    time.sleep(0.5)
    reset_node_colors()

bfs_button.config(command=run_bfs)

root.mainloop()
