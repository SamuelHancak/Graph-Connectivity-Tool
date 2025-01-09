import time
from scipy.spatial import KDTree
import numpy as np


# https://www.geeksforgeeks.org/strongly-connected-components/
class Graph:
    """
    A class to represent a graph using adjacency list representation.

    Attributes
    ----------
    adjusted_vertices : dict
        A dictionary where keys are vertices and values are lists of connected vertices.
    graph_vertices : set
        A set containing all unique vertices in the graph.

    Methods
    -------
    __init__(file_name):
        Initializes the graph from a file containing edges.
    __initialise_graph(file_name):
        Reads the file and initializes the graph's vertices and edges.
    __add_edge(start_vertex, end_vertex):
        Adds an edge between two vertices in the graph.
    __DFS_util(temp, vertex, visited):
        A utility function for performing depth-first search (DFS).
    find_connected_groups():
        Finds and returns all connected groups (components) in the graph.
    """

    def __init__(self, file_name):
        """
        Initializes the graph from a file containing edges.

        Parameters
        ----------
        file_name : str
            The name of the file containing the graph edges.
        """
        # dictionary of all graph vertices connections with the others vertices `vertex: [connected_1, connected_2, connected_3, ...]`
        self.adjusted_vertices = {}
        # all vertices in a graph - using set to contain only unique values and time complexity of find is O(1)
        self.graph_vertices = set()
        self.__initialise_graph(file_name)

    def __initialise_graph(self, file_name):
        """
        Reads the file and initializes the graph's vertices and edges.

        Parameters
        ----------
        file_name : str
            The name of the file containing the graph edges.
        """
        with open(file_name, "r") as file:
            lines = file.readlines()

            for line in lines:
                points = line.strip().replace("[", "").replace("]", "").split(" ")
                x1, y1 = points[0].split(",")
                x2, y2 = points[1].split(",")

                self.__add_edge((int(x1), int(y1)), (int(x2), int(y2)))

        file.close()

    def __add_edge(self, start_vertex, end_vertex):
        """
        Adds an edge between two vertices in the graph.

        Parameters
        ----------
        start_vertex : tuple
            The starting vertex of the edge.
        end_vertex : tuple
            The ending vertex of the edge.
        """
        self.adjusted_vertices.setdefault(start_vertex, []).append(end_vertex)
        self.adjusted_vertices.setdefault(end_vertex, []).append(start_vertex)
        self.graph_vertices.add(start_vertex)
        self.graph_vertices.add(end_vertex)

    def __DFS_util(self, temp, vertex, visited):
        """
        A utility function for performing depth-first search (DFS).

        Parameters
        ----------
        temp : list
            A list to store the connected component.
        vertex : tuple
            The current vertex being visited.
        visited : dict
            A dictionary to keep track of visited vertices.

        Returns
        -------
        list
            The connected component containing the vertex.
        """
        visited[vertex] = True
        temp.append(vertex)

        for connected_vertex in self.adjusted_vertices[vertex]:
            if not visited[connected_vertex]:
                temp = self.__DFS_util(temp, connected_vertex, visited)

        return temp

    def find_connected_groups(self):
        """
        Finds and returns all connected groups (components) in the graph.

        Returns
        -------
        dict
            A dictionary where keys are group indices and values are lists of vertices in each group.
        """
        visited = {vertex: False for vertex in self.graph_vertices}
        unions = []

        for vertex in self.graph_vertices:
            if not visited[vertex]:
                unions.append(self.__DFS_util([], vertex, visited))

        return {
            i: [{"group": i, "root": vertex} for j, vertex in enumerate(union)]
            for i, union in enumerate(unions)
        }


def connect_groups(groups):
    """
    Connects the groups by finding the nearest points between them and adding edges.

    Parameters
    ----------
    groups : dict
        A dictionary where keys are group indices and values are lists of vertices in each group.

    Returns
    -------
    list
        A list of added edges to connect the groups.
    """
    added_edges = []
    dist_overall = 0
    find_in = {0: groups.pop(0)}

    while groups:
        tree_base_data = [values for group in groups.values() for values in group]
        tree_data = [values["root"] for group in groups.values() for values in group]
        find_in_data = [
            values["root"] for group in find_in.values() for values in group
        ]

        tree = KDTree(tree_data)

        distances, indices = tree.query(find_in_data, workers=-1)
        index_min = np.argmin(distances)
        tree_nearest_vertex_id = indices[index_min]

        tree_nearest_vertex = tree_base_data[tree_nearest_vertex_id]

        best_group_id = tree_nearest_vertex["group"]
        find_in[best_group_id] = groups.pop(best_group_id)

        dist_overall += distances[index_min]
        added_edges.append((tree_nearest_vertex["root"], find_in_data[index_min]))
        print(len(added_edges))

    print(f"Total distance: {dist_overall}")

    return added_edges


def write_to_file(edges):
    """
    Writes the added edges to a file.

    Parameters
    ----------
    edges : list
        A list of added edges to be written to the file.
    """
    with open("out_60203.txt", "w+") as output_file:
        for edge in edges:
            output_file.write(
                f"[{str(edge[0][0])},{str(edge[0][1])}] [{str(edge[1][0])},{str(edge[1][1])}]"
                + "\n"
            )


if __name__ == "__main__":
    FILE_NAME = "test_data/graph_60203.txt"

    graph = Graph(FILE_NAME)  # graph initialisation
    groups = graph.find_connected_groups()  # find connected groups
    print("Graphs count: ", len(groups))

    start_time = time.time()
    added_edges = connect_groups(
        groups
    )  # find the nearest points between groups and connect them
    end_time = time.time()

    write_to_file(added_edges)  # write added edges to the output file

    print(f"\nTime: {end_time - start_time}s", end="\n")
