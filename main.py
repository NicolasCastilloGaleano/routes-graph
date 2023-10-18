import networkx as nx
import matplotlib.pyplot as plt
from grafo import *
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from math import *


class Rutas:
    def __init__(self) -> None:
        self.locations = [
            [0, "huila", 37, 41],
            [1, "norte de santander", 51, 70],
            [2, "antioquia", 36, 63],
            [3, "caldas", 37, 56],
            [4, "choco", 29, 55],
            [5, "san andres y providencia", 13, 93],
            [6, "la guajira", 53, 90],
            [7, "nariño", 24, 35],
            [8, "bogota", 44, 49],
            [9, "amazonas", 60, 20],
            [10, "vaupes", 63, 31],
            [11, "caqueta", 45, 30],
            [12, "putumayo", 35, 30],
            [13, "cauca", 29, 40],
            [14, "guaviare", 55, 36],
            [15, "meta", 50, 45],
            [16, "guainia", 73, 42],
            [17, "vichada", 70, 53],
            [18, "valle del cauca", 30, 46],
            [19, "tolima", 38, 48],
            [20, "quindio", 35, 52],
            [21, "cundinamarca", 45, 54],
            [22, "risaralda", 33, 55],
            [23, "casanare", 57, 55],
            [24, "boyaca", 50, 57],
            [25, "arauca", 61, 62],
            [26, "santander", 48, 64],
            [27, "cordoba", 35, 73],
            [28, "bolivar", 44, 74],
            [29, "sucre", 38, 77],
            [30, "magdalena", 43, 81],
            [31, "cesar", 48, 81],
            [32, "atlantico", 39, 85],
        ]
        self.paths = [
            
        ]
        self.edges = []
        self.nodes = []
        self.current_nodes = {}
        for i in self.locations:
            self.nodes.append(GraphNode(i[0],i[1], [
                              i[2], i[3]]))
            self.current_nodes[i[1]] = i[0]

        for path in self.paths:
            self.edges.append(GraphEdge(
                GraphNode(path[0][0], path[0][1], [path[0][2], path[0][3]]),
                GraphNode(path[1][0], path[1][1], [path[1][2], path[1][3]])))

        self.graph = Graph(self.nodes, self.edges)
        self.graphic = nx.Graph()
        self.create_window()

    def create_window(self):
        self.window = Tk()
        self.window.geometry("1340x680+0+0")
        self.window.resizable(0, 0)
        self.window.title("Graph")
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=2)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        # nombres aeropuertos
        self.names_frame = Frame(
            self.window, width=300, height=600, bg="#000000")
        self.names_frame.grid(column=0, row=0, sticky=NSEW)
        self.names = Listbox(self.names_frame, font=("", 12))
        self.names.pack(fill="both")
        self.names = self.names
        self.update_listBox()
        # area grafico
        self.create_graphic(self.graphic, self.window)
        # navegacion
        self.nav = Frame(self.window, width=300, height=600)
        self.nav.grid(column=2, row=0, sticky=NSEW)
        self.nav.grid_rowconfigure(0, weight=1)
        self.nav.grid_rowconfigure(1, weight=1)
        self.nav.grid_rowconfigure(2, weight=1)

        # Aeropuertos
        self.nodes_frame = Frame(self.nav)
        self.nodes_frame.grid(column=0, row=0, sticky=NSEW)
        # crear aeropuerto
        self.create_node_frame = Frame(self.nodes_frame)
        self.create_node_frame.grid(column=0, row=0, sticky=EW)
        self.create_node_label = Label(
            self.create_node_frame, text="Crear aeropuerto: ", anchor="w", font=("", 12))
        self.create_node_label.grid(column=0, row=0, sticky=EW)
        self.create_node_select = ttk.Combobox(
            self.create_node_frame, state="readonly", values=self.select_values(False), font=("", 12))
        self.create_node_select.grid(column=0, row=1, sticky=NSEW)
        self.create_node_button = Button(
            self.create_node_frame, width=30, text="CREAR", font=("bold", 12), command=self.add_node)
        self.create_node_button.grid(column=0, row=2, sticky=N)
        # Eliminar aeropuerto
        self.delete_node_frame = Frame(self.nodes_frame)
        self.delete_node_frame.grid(column=0, row=1, sticky=EW)
        self.delete_node_label = Label(
            self.delete_node_frame, text="Eliminar aeropuerto: ", anchor="w", font=("", 12))
        self.delete_node_label.grid(column=0, row=0, sticky=EW)
        self.delete_node_select = ttk.Combobox(
            self.delete_node_frame, state="readonly", values=self.select_values(True), font=("", 12))
        self.delete_node_select.grid(column=0, row=1, sticky=NSEW)
        self.delete_node_button = Button(
            self.delete_node_frame, width=30, text="ELIMINAR", font=("bold", 12), command=self.delete_node)
        self.delete_node_button.grid(column=0, row=2, sticky=N)

        # rutas
        self.edges_frame = Frame(self.nav)
        self.edges_frame.grid(column=0, row=1, sticky=NSEW)
        # crear ruta
        self.create_edge_frame = Frame(self.edges_frame)
        self.create_edge_frame.grid(column=0, row=1, sticky=EW)
        self.create_edge_label = Label(
            self.create_edge_frame, text="Crear o actualizar ruta: ", anchor="w", font=("", 12))
        self.create_edge_label.grid(column=0, columnspan=2, row=0, sticky=EW)
        self.create_edge_origin_label = Label(
            self.create_edge_frame, text="Origen: ", anchor="w", font=("", 12))
        self.create_edge_origin_label.grid(
            column=0, columnspan=2, row=1, sticky=EW)
        self.create_edge_origin_select = ttk.Combobox(
            self.create_edge_frame, state="readonly", values=self.select_values(True), font=("", 12))
        self.create_edge_origin_select.grid(
            column=0, columnspan=2, row=2, sticky=NSEW)
        self.create_edge_origin_select.bind(
            "<<ComboboxSelected>>", lambda event: self.update_edge_content(event))
        self.create_edge_destination_label = Label(
            self.create_edge_frame, text="Destino: ", anchor="w", font=("", 12))
        self.create_edge_destination_label.grid(
            column=0, columnspan=2, row=3, sticky=EW)
        self.create_edge_destination_select = ttk.Combobox(
            self.create_edge_frame, state="readonly", values=self.select_values(True), font=("", 12))
        self.create_edge_destination_select.grid(
            column=0, columnspan=2, row=4, sticky=NSEW)
        self.create_edge_destination_select.bind(
            "<<ComboboxSelected>>", lambda event: self.update_edge_content(event))
        self.distance_entry_label = Label(
            self.create_edge_frame, text="distancia:")
        self.distance_entry_label.grid(column=0, row=5, sticky=NSEW)
        self.flying_time_entry_label = Label(
            self.create_edge_frame, text="tiempo:")
        self.flying_time_entry_label.grid(column=1, row=5, sticky=NSEW)
        self.distance_entry = Entry(self.create_edge_frame)
        self.distance_entry.grid(column=0, row=6)
        self.flying_time_entry = Entry(self.create_edge_frame)
        self.flying_time_entry.grid(column=1, row=6)
        self.create_edge_button = Button(
            self.create_edge_frame, width=30, text="CREAR O ACTUALIZAR", font=("bold", 12), command=self.add_edge)
        self.create_edge_button.grid(column=0, columnspan=2, row=7, sticky=N)
        # busqueda de rutas
        self.search_paths = Frame(self.nav)
        self.search_paths.grid(column=0, row=2, sticky=NSEW)
        self.search_paths_label = Label(
            self.search_paths, text="buscar ruta: ", anchor="w", font=("", 12))
        self.search_paths_label.grid(column=0, row=0, sticky=EW)
        self.search_paths_origin_label = Label(
            self.search_paths, text="Origen: ", anchor="w", font=("", 12))
        self.search_paths_origin_label.grid(column=0, row=1, sticky=EW)
        self.search_paths_origin_select = ttk.Combobox(
            self.search_paths, state="readonly", values=self.select_values(True), font=("", 12))
        self.search_paths_origin_select.grid(column=0, row=2, sticky=NSEW)
        self.search_paths_destination_label = Label(
            self.search_paths, text="Destino: ", anchor="w", font=("", 12))
        self.search_paths_destination_label.grid(column=0, row=3, sticky=EW)
        self.search_paths_destination_select = ttk.Combobox(
            self.search_paths, state="readonly", values=self.select_values(True), font=("", 12))
        self.search_paths_destination_select.grid(column=0, row=4, sticky=NSEW)
        self.search_paths_button = Button(self.search_paths, width=30, text="BUSCAR", font=(
            "bold", 12), command=self.show_paths)
        self.search_paths_button.grid(column=0, row=5, sticky=N)
        # boton cambiar peso
        self.change_button = Button(self.nav, text="CAMBIAR PESO", font=(
            "", 12), command=self.change_weight)
        self.change_button.grid(row=4, column=0, sticky=EW)

        self.window.mainloop()

    def change_weight(self):
        if self.distance == True:
            self.create_graphic(self.graphic, self.window, None, None, False)
            self.distance = False
        else:
            self.create_graphic(self.graphic, self.window, None, None, True)
            self.distance = True
        return

    def update_edge_content(self, event):
        if self.create_edge_destination_select.get() and self.create_edge_origin_select.get():
            origin = self.graph.get_node(self.create_edge_origin_select.get())
            destination = self.graph.get_node(
                self.create_edge_destination_select.get())
            if self.graph.get_edge(origin.name, destination.name):
                temp_edge = self.graph.get_edge(origin.name, destination.name)
                self.distance_entry.delete(0, END)
                self.distance_entry.insert(0, temp_edge.distance)
                self.flying_time_entry.delete(0, END)
                self.flying_time_entry.insert(0, temp_edge.flying_time)
            else:
                self.distance_entry.delete(0, END)
                self.flying_time_entry.delete(0, END)

    def add_node(self):
        if self.create_node_select.get():
            temp_node = None
            for location in self.locations:
                if location[1] == self.create_node_select.get():
                    temp_node = GraphNode(location[0], location[1], [
                                          location[2], location[3]])
                    break

            self.current_nodes[temp_node.name] = temp_node.index
            self.graph.create_node(temp_node)
            self.update_content()

    def delete_node(self):
        if self.delete_node_select.get():
            temp_node = None
            for location in self.locations:
                if location[1] == self.delete_node_select.get():
                    temp_node = GraphNode(location[0], location[1], [
                                          location[2], location[3]])
                    break
            if self.graph.delete_node(temp_node):
                del self.current_nodes[temp_node.name]
                self.update_content()

    def add_edge(self):
        if (self.create_edge_origin_select.get() and self.create_edge_destination_select.get()) and (self.create_edge_origin_select.get() != self.create_edge_destination_select.get()):
            origin = self.graph.get_node(self.create_edge_origin_select.get())
            destination = self.graph.get_node(
                self.create_edge_destination_select.get())
            if self.distance_entry.get() and int(self.distance_entry.get()):
                distance = int(self.distance_entry.get())
            else:
                distance = None
            if self.flying_time_entry.get() and int(self.flying_time_entry.get()):
                flying_time = int(self.flying_time_entry.get())
            else:
                flying_time = None

            if self.graph.get_edge(origin, destination):
                self.update_edge(self.graph.get_edge(origin, destination))
            else:
                self.graph.create_edge(
                    GraphEdge(origin, destination, distance, flying_time))
            self.update_content()

    def update_edge(self, edge):
        origin = edge.origin
        destination = edge.destination
        distance = int(self.distance_entry.get())
        flying_time = int(self.flying_time_entry.get())
        self.graph.update_edge(self.graph.get_edge(
            origin, destination), distance, flying_time)

    def update_content(self):
        self.update_selects()
        self.update_listBox()
        self.create_graphic(self.graphic, self.window)

    def show_paths(self):
        if self.search_paths_origin_select.get() and self.search_paths_destination_select.get():
            origin = self.graph.get_node(self.search_paths_origin_select.get())
            destination = self.graph.get_node(
                self.search_paths_destination_select.get())
            nodes = []
            index_list = nx.dijkstra_path(
                self.graphic, origin.index, destination.index)
            edges = []
            text = "La mejor ruta desde " + origin.name + \
                " hasta " + destination.name + " es: "
            for node_index in index_list:
                text = text + " " + self.locations[node_index][1] + " - "
                nodes.append(self.graph.get_node(self.locations[node_index][1]))
            for node_index in range(0, len(index_list)-1):
                edges.append(self.graph.get_edge(
                    self.locations[index_list[node_index]][1], self.locations[index_list[node_index+1]][1]))
            distance = nx.dijkstra_path_length(
                self.graphic, origin.index, destination.index)
            if self.distance:
                text = text + " con un recorrido total de " + \
                    str(distance) + " unidades de distancia."
            else:
                text = text + " con un tiempo total de " + \
                    str(distance) + " unidades de tiempo."
            self.show_path_window = Toplevel()
            self.show_path_window.geometry("600x600")
            self.show_path_window.resizable(0, 0)
            self.show_path_window.title("Graph")
            self.path_graph = nx.Graph()
            self.create_graphic(
                self.graphic, self.show_path_window, nodes, edges,self.distance)

            self.path_label = Label(self.show_path_window,
                                    text=text, font=("", 15), wraplength=550)
            self.path_label.grid(column=1, row=1, sticky=NSEW)

    def select_values(self, current_nodes):
        values = []
        if current_nodes == True:
            for location in self.locations:
                if location[1] in self.current_nodes:
                    values.append(location[1])
        else:
            for location in self.locations:
                if location[1] not in self.current_nodes:
                    values.append(location[1])
        return values

    def update_listBox(self):
        self.names.delete(0, END)
        for location in self.locations:
            if location[1] in self.current_nodes:
                name = str(location[0]) + ": " + location[1]
                self.names.insert(END, name)
        self.names.pack(fill="both", expand=True)

    def update_selects(self):
        self.create_node_select.delete(0, END)
        self.create_node_select["values"] = self.select_values(False)
        self.create_node_select.set("")
        self.delete_node_select.delete(0, END)
        self.delete_node_select["values"] = self.select_values(True)
        self.delete_node_select.set("")
        self.create_edge_origin_select.delete(0, END)
        self.create_edge_origin_select["values"] = self.select_values(True)
        self.create_edge_origin_select.set("")
        self.create_edge_destination_select.delete(0, END)
        self.create_edge_destination_select["values"] = self.select_values(
            True)
        self.create_edge_destination_select.set("")
        self.search_paths_origin_select.delete(0, END)
        self.search_paths_origin_select["values"] = self.select_values(True)
        self.search_paths_origin_select.set("")
        self.search_paths_destination_select.delete(0, END)
        self.search_paths_destination_select["values"] = self.select_values(
            True)
        self.search_paths_destination_select.set("")
        self.distance_entry.delete(0, END)
        self.flying_time_entry.delete(0, END)

    def create_graphic(self, graphic, window, nodes=[], edges=[], distance=True):
        self.distance = distance
        plt.close()
        graphic = nx.Graph()
        if self.distance:
            if nodes and edges:
                for node in nodes:
                    graphic.add_node(node.index, pos=node.location)
                for edge in edges:
                    graphic.add_edge(
                        edge.origin.index, edge.destination.index, weight=edge.distance)
            else:
                for node in self.graph.get_nodes():
                    graphic.add_node(node.index, pos=node.location)
                for edge in self.graph.get_edges():
                    graphic.add_edge(
                        edge.origin.index, edge.destination.index, weight=edge.distance)
                self.graphic = graphic
        else:
            if nodes and edges:
                for node in nodes:
                    graphic.add_node(node.index, pos=node.location)
                for edge in edges:
                    graphic.add_edge(
                        edge.origin.index, edge.destination.index, weight=edge.flying_time)
            else:
                for node in self.graph.get_nodes():
                    graphic.add_node(node.index, pos=node.location)
                for edge in self.graph.get_edges():
                    graphic.add_edge(
                        edge.origin.index, edge.destination.index, weight=edge.flying_time)
                self.graphic = graphic

        pos = nx.get_node_attributes(graphic, 'pos')
        figure, ax = plt.subplots()
        img = plt.imread("./img/map.png")
        ax.imshow(img, extent=[0, 100, 0, 100])
        canvas = FigureCanvasTkAgg(figure, window)
        canvas.get_tk_widget().grid(column=1, row=0, sticky=NSEW)
        nx.draw(graphic, pos, with_labels=True, node_size=75,
                font_size=8, node_color="red", edge_color="red")
        labels = nx.get_edge_attributes(graphic, 'weight')
        nx.draw_networkx_edge_labels(
            graphic, pos, edge_labels=labels, rotate=False, font_size=6,)


rutas = Rutas()
