import json
import random

from GraphAlgoInterface import *
from DiGraph import *

import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, graph: DiGraph = {}):
        self.algo: DiGraph = graph

    def get_graph(self) -> GraphInterface:
        return self.algo

    def load_from_json(self, file_name: str) -> bool:
        try:
            if file_name.endswith('.json') == False:
                file_name = file_name + ".json"
            with open(file_name, "r") as jsonfile:

                file = json.load(jsonfile)
            self.algo = DiGraph()
            for node in file["Nodes"]:  # add nodes
                if 'pos' not in node:
                    self.get_graph().add_node(node["id"], (0, 0))
                else:
                    sp = str(node['pos']).split(',')
                    self.get_graph().add_node(node['id'], (float(sp[0]), float(sp[1])))

            for edge in file["Edges"]:  # add edges
                self.get_graph().add_edge(edge['src'], edge['dest'], edge['w'])
            return True

        except IOError as e:
            print(e)

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "w") as jsonfile:
                nodes = []
                edges = []

                for node in self.algo.nodes:  # add nodes
                    (x, y) = self.algo.nodes[node]
                    nodes.append({"pos": str(x) + "," + str(y) + "," + str(0.0), "id": node})

                for edge in self.algo.edges:  # add edges
                    for dest in self.algo.edges[edge]:
                        edges.append({"src": edge, "w": self.algo.edges[edge][dest], "dest": dest})

                SaveFile = {"Edges": edges, "Nodes": nodes}  # dict for json send file dump
                json.dump(SaveFile, jsonfile, indent=2)
                return True

        except IOError as e:
            print(e)

    def djs(self, src):  # dijkstras algorithm

        nodes = list(self.get_graph().get_all_v())  # add all nodes to list
        FinalShortestPath = {}  # final shortest path after visiting all neighbour nodes
        neighbourNodes = {}  # neighbour nodes for each node

        for node in nodes:
            FinalShortestPath[node] = float('inf')  # unvisited node will be infinity and then will be updated to weight

        FinalShortestPath[src] = 0  # start node will be 0 as visited
        while nodes:  # lets check all nodes
            curr = None
            for node in nodes:
                if curr is None:
                    curr = node
                elif FinalShortestPath[node] < FinalShortestPath[curr]:  # lets find lowest weight to node
                    curr = node

            neighbours = self.get_graph().all_out_edges_of_node(curr)  # get all neighbours
            for neighbour in neighbours:
                weight = FinalShortestPath[curr] + self.algo.edges[curr][neighbour]  # weight between nodes
                if weight < FinalShortestPath[neighbour]:  # lowest weight
                    FinalShortestPath[neighbour] = weight
                    neighbourNodes[neighbour] = curr
            nodes.remove(curr)

        return neighbourNodes, FinalShortestPath

    def shortest_path(self, id1: int, id2: int) -> (float, list):  # return weight,path

        neighbourNodes, FinalShortestPath = self.djs(id1)
        if FinalShortestPath[id2] == float('inf'):  # no path distance infinite
            return float('inf'), []
        else:
            path = []
            reverselist = []
            pathNode = id2
            while pathNode != id1:  # lets find path in neighbour nodes
                path.append(neighbourNodes[pathNode])
                pathNode = neighbourNodes[pathNode]  # next in path

            path.insert(0, id2)  # add last node
            for node in path:  # lets reverse list
                reverselist.insert(0, node)

        return FinalShortestPath[id2], reverselist

    def TSP(self, node_lst: List[int]) -> (List[int], float):

        minList = []  # min path between nodes
        shortestpathDist = 0  # the weight from the path
        minList.append(node_lst[0])  # add first node
        startNode = node_lst[0]  # starting node

        for node in node_lst[1:]:  # add path to next node without first node
            dist, shortPath = self.shortest_path(startNode,
                                                 node)  # calculate dist between each two nodes and shortest path between them
            shortestpathDist = shortestpathDist + dist  # add dist
            startNode = node  # next node

            for shortNode in shortPath[1:]:  # add path to next node without first node
                minList.append(shortNode)

        return minList, shortestpathDist

    def centerPoint(self) -> (int, float):
        for node in self.algo.nodes:
            if self.djs(node)[1][1] == float('inf'):
                return None, float('inf')

        nodes = {}
        for node in self.algo.nodes:
            weight = 0  # reset max weight
            shortestpathDist = self.djs(node)[1]  # list of shortest paths from dijkstras algo
            for j in shortestpathDist:  # compare each node distance
                if shortestpathDist[j] > weight:
                    weight = shortestpathDist[j]
            nodes.update({node: weight})  # lets update max weight of this node

        minWeight = float('inf')
        for node in nodes:  # lets get center node with min weight
            if minWeight > nodes[node]:
                minWeight = nodes[node]
                CenterNode = node

        return CenterNode, minWeight


    def plot_graph(self) -> None:  # draw graph
        plt.style.use('dark_background')
        plt.rcParams['toolbar'] = 'None'
        plt.figure("Graph", figsize=(10, 6))
        plt.axis('off')
        for node in self.algo.nodes:  # draw nodes
            (x, y) = self.algo.nodes[node]
            if x == 0.0 or x == None and y == 0.0 or y == None:  # no pos
                x = random.uniform(35, 36)
                y = random.uniform(32, 33)
                self.algo.nodes.update({node: (x, y)})
            else:
                (x, y) = self.algo.nodes[node]
            plt.plot(float(x), float(y), markersize=5, marker="o", color="blue")
            plt.text(float(x), float(y), str(node), color="yellow", fontsize=10)

        for edge in self.algo.edges:  # draw edges
            for edge1 in self.algo.edges[edge]:
                (x1, y1) = self.algo.nodes[edge]
                (x2, y2) = self.algo.nodes[edge1]
                plt.annotate("", (float(x1), float(y1)), (float(x2), float(y2)),
                             arrowprops=dict(arrowstyle="->", edgecolor="green", lw=1))

        plt.show()
