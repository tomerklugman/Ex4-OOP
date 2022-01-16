import unittest
from GraphAlgo import *


class GraphAlgoTest(unittest.TestCase):

    def test_get_graph(self):
        a = DiGraph()
        a.add_node(1)
        a.add_node(2)
        a.add_node(3)
        a.add_node(4)
        algo=GraphAlgo(a)

        self.assertEqual(algo.get_graph(), a)

    def test_load_from_json(self):
        algo=GraphAlgo()
        algo.load_from_json("../data/100000Nodes.json") #load file
        #a = algo.get_graph() #get graph will get it loaded succesfully

        #self.assertEqual(algo.get_graph(), a)

    def test_save_to_json(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/100000Nodes.json") # load file
        a = algo.get_graph() # save it at a
        algo.save_to_json("../data/100000Nodes.json" + '_saved') # create "saved" file
        #algo.load_from_json("../data/A5.json_saved") # load it to algo

        self.assertEqual(algo.get_graph(), a) # check if both graphs equal then saved succesfully

    def test_shortest_path(self): # and dijkstras algorithm check
        algo = GraphAlgo()
        algo.load_from_json("../data/10000Nodes.json") # load file
        dist, path = algo.shortest_path(0, 999)
        #self.assertEqual(dist, 2.062180280059253)
        #self.assertEqual(path, [1, 10, 7])

    def test_TSP(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/1000Nodes.json") # load file
        list=[]
        for i in algo.algo.nodes:
            list.append(i)

        algo.TSP(list)

        #self.assertEqual(dist, 2.370613295323088)
        #self.assertEqual(path, [1, 9, 2, 3])

    def test_centerPoint(self): # and isConnected check
        algo = GraphAlgo()
        algo.load_from_json("../data/1000Nodes.json") # load file

        algo.centerPoint()




