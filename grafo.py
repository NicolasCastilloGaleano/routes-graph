from math import *
import random

class GraphEdge:
    def __init__(self, origin, destination,distance = None, flying_time = None) -> None:
        self.origin = origin
        self.destination = destination
        if distance:
            self.distance = distance
        else:
            self.distance = random.randint(1,100)
        if flying_time:
            self.flying_time = flying_time
        else:
            self.flying_time = random.randint(1,100)



class GraphNode:
    def __init__(self, index, name, location) -> None:
        self.index = index
        self.name = name
        self.location = location


class Graph:
    def __init__(self, nodes, edges) -> None:
        self.nodes = nodes
        self.edges = edges

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def create_node(self, node):
        self.nodes.append(node)

    def delete_node(self, temp_node):
        for node in self.nodes:
            if (node.name == temp_node.name) and self.can_delete_node(temp_node):
                self.nodes.remove(node)
                return True
        return False

    def can_delete_node(self,node):        
        for edge in self.edges:
            if (node.name == edge.origin.name) or (node.name == edge.destination.name):
                return False
        return True


    def create_edge(self, edge):
        self.edges.append(edge)

    def get_node(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

    def get_edge(self, origin, destination):
        for edge in self.edges:
            if (edge.origin.name == origin and edge.destination.name == destination) or (edge.origin.name == destination and edge.destination.name == origin):
                return edge

    def update_edge(self,edge,new_distance,new_flying_time):
        edge.distance = new_distance
        edge.flying_time = new_flying_time
