import tkinter as tk
from tkinter import simpledialog
from algorithms import bfs_level_by_level, dfs_visual, dijkstra_visual, topo_sort_visual


class GraphVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph Algorithm Visualizer")

        self.graph = GraphData()

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        tk.Checkbutton(self.root, text="Directed", variable=self.graph.directed_var).pack(side=tk.LEFT)
        tk.Checkbutton(self.root, text="Weighted", variable=self.graph.weighted_var).pack(side=tk.LEFT)

        tk.Button(self.root, text="Run BFS", command=self.run_bfs).pack(side=tk.LEFT)
        tk.Button(self.root, text="Run DFS", command=self.run_dfs).pack(side=tk.LEFT)
        tk.Button(self.root, text="Run Dijkstra", command=self.run_dijkstra).pack(side=tk.LEFT)
        tk.Button(self.root, text="Run Topo Sort", command=self.run_topo_sort).pack(side=tk.LEFT)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def draw_node(self, x, y, node_id):
        r = 20
        oval_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="lightblue")
        self.canvas.create_text(x, y, text=str(node_id), font=("Arial", 12))
        self.graph.nodes[node_id] = (x, y)
        self.graph.node_id_to_canvas[node_id] = oval_id
        self.graph.node_canvas_ids[oval_id] = node_id
        self.graph.adj[node_id] = []

    def on_canvas_click(self, event):
        clicked = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if not clicked:
            self.draw_node(event.x, event.y, self.graph.node_count)
            self.graph.node_count += 1
            self.graph.selected_node = None
        else:
            node_id = self.graph.node_canvas_ids.get(clicked[0], None)
            if node_id is None:
                return
            if self.graph.selected_node is None:
                self.graph.selected_node = node_id
            elif self.graph.selected_node != node_id:
                u, v = self.graph.selected_node, node_id
                x1, y1 = self.graph.nodes[u]
                x2, y2 = self.graph.nodes[v]

                weight = 1
                if self.graph.weighted_var.get():
                    weight = simpledialog.askinteger("Edge Weight", f"Weight from {u} to {v}:", minvalue=1)
                    if weight is None:
                        self.graph.selected_node = None
                        return

                from math import atan2, cos, sin
                angle = atan2(y2 - y1, x2 - x1)
                offset = 20
                ax1, ay1 = x1 + offset * cos(angle), y1 + offset * sin(angle)
                ax2, ay2 = x2 - offset * cos(angle), y2 - offset * sin(angle)

                if self.graph.directed_var.get():
                    self.canvas.create_line(ax1, ay1, ax2, ay2, width=2, fill="black", arrow=tk.LAST)
                else:
                    self.canvas.create_line(x1, y1, x2, y2, width=2, fill="black")

                if self.graph.weighted_var.get():
                    label_x = (x1 + x2) // 2 + (y2 - y1) // 10
                    label_y = (y1 + y2) // 2 - (x2 - x1) // 10
                    self.canvas.create_text(label_x, label_y, text=str(weight), font=("Arial", 20), fill="black")

                self.graph.adj[u].append((v, weight))
                if not self.graph.directed_var.get():
                    self.graph.adj[v].append((u, weight))

                self.graph.edges.append((u, v, weight))
                self.graph.selected_node = None

    def run_bfs(self):
        bfs_level_by_level(self.canvas, self.graph)

    def run_dfs(self):
        dfs_visual(self.canvas, self.graph)

    def run_dijkstra(self):
        dijkstra_visual(self.canvas, self.graph, self.graph.weighted_var.get())

    def run_topo_sort(self):
        topo_sort_visual(self.canvas, self.graph)

    def run(self):
        self.root.mainloop()


class GraphData:
    def __init__(self):
        self.nodes = {}
        self.node_canvas_ids = {}
        self.node_id_to_canvas = {}
        self.edges = []
        self.adj = {}
        self.node_count = 0
        self.selected_node = None

        self.directed_var = tk.BooleanVar()
        self.weighted_var = tk.BooleanVar()
