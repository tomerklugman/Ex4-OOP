from GraphInterface import *


class DiGraph(GraphInterface):

    def __init__(self):
        self.nodes = {}  # nodes dict <key,pos> pos is (x,y)
        self.edges = {}  # nested dictionary of edges -- edges = {src:{dest:weight,dest2:weight} nextnode:{}}
        self.mc = 0

    def __repr__(self):
        return f"Graph: |V|={self.v_size()}, |E|={self.e_size()}"

    def v_size(self) -> int:
        return len(self.nodes)

    def e_size(self) -> int:
        edges = 0
        for count in self.edges.values():  # get each value and get length
            edges = edges + len(count)
        return edges

    def get_all_v(self) -> dict:
        nodesPrint={}
        for node in self.nodes:
            nodesPrint.update({node:f"{node}: |edges_out| {len(self.all_out_edges_of_node(node))} |edges in| {len(self.all_in_edges_of_node(node))}"})
        return nodesPrint

    def all_in_edges_of_node(self, id1: int) -> dict:
        # connect to node -- node is dest
        # edges dict is [src{dest:weight}
        edgesIn = {}
        if id1 in self.nodes:
            for nodeid in self.nodes and self.edges:
                for destEdge in self.edges[nodeid]:
                    if destEdge == id1:
                        edgesIn.update({nodeid: self.edges[nodeid][destEdge]})

        return edgesIn

    def all_out_edges_of_node(self, id1: int) -> dict:
        # connect from node -- node is src
        # {1:{ {2:3} }, 2:{ {3:4} }

        edgesOut = {}

        if id1 in self.nodes and id1 in self.edges:
            for srcEdge in self.edges[id1]:
                edgesOut.update({srcEdge: self.edges[id1][srcEdge]})

        return edgesOut

    def get_mc(self) -> int:
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 in self.nodes and id2 in self.nodes:
            self.edges[id1][id2] = weight
            self.mc = self.mc + 1
            return True
        else:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.nodes:  # node already exists
            return False
        else:
            if (pos == None):
                pos=(0.0,0.0)
            self.nodes.update({node_id: pos})
            self.edges[node_id] = {}
            self.mc = self.mc + 1
            return True

    def remove_node(self, node_id: int) -> bool:
        if node_id in self.nodes:
            for id in self.edges:
                self.remove_edge(id, node_id)
            del self.nodes[node_id]
            del self.edges[node_id]
            self.mc = self.mc + 1
            return True
        else:
            return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id2 in self.edges[node_id1]:
            del self.edges[node_id1][node_id2]
            self.mc = self.mc + 1
            return True
        else:
            return False
