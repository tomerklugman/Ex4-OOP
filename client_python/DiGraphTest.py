import unittest
from DiGraph import DiGraph


class DiGraphTest(unittest.TestCase):

    def test_v_size(self):
        a = DiGraph()
        a.add_node(1)
        a.add_node(2)
        a.add_node(3)
        a.add_node(4)

        self.assertEqual(a.v_size(), 4)  # 4 nodes added

    def test_e_size(self):
        a = DiGraph()
        a.add_node(1)
        a.add_node(2)
        a.add_node(3)
        a.add_node(4)

        a.add_edge(1, 2, 1)
        a.add_edge(2, 3, 2)
        a.add_edge(3, 4, 3)

        self.assertEqual(a.e_size(), 3)  # 3 edges added

    def test_get_all_v(self):
        a = DiGraph()
        a.add_node(1)
        a.add_node(2)
        a.add_node(3)
        a.add_node(4)

        self.assertEqual(a.get_all_v(), {1: '1: |edges_out| 0 |edges in| 0',
                                         2: '2: |edges_out| 0 |edges in| 0',
                                         3: '3: |edges_out| 0 |edges in| 0',
                                         4: '4: |edges_out| 0 |edges in| 0'})  # 4 nodes

    def test_all_in_edges_of_node(self):
        a = DiGraph()
        a.add_node(1)
        a.add_node(2)
        a.add_node(3)
        a.add_node(4)

        a.add_edge(2, 1, 1)
        a.add_edge(3, 1, 2)
        a.add_edge(4, 1, 3)

        self.assertEqual(a.all_in_edges_of_node(1), {2: 1, 3: 2, 4: 3})  # src:weight -- node 1 is dest

    def test_all_out_edges_of_node(self):
        a = DiGraph()
        a.add_node(1)
        a.add_node(2)
        a.add_node(3)
        a.add_node(4)

        a.add_edge(1, 2, 1)
        a.add_edge(1, 3, 2)
        a.add_edge(1, 4, 3)

        self.assertEqual(a.all_out_edges_of_node(1), {2: 1, 3: 2, 4: 3})  # dest:weight -- node1 is src

    def test_get_mc(self):
        a = DiGraph()
        a.add_node(1)  # 1
        a.add_node(2)  # 2
        a.add_node(3)  # 3
        a.add_node(4)  # 4

        a.add_edge(1, 2, 1)  # 5
        a.add_edge(1, 3, 2)  # 6
        a.add_edge(1, 4, 3)  # 7
        a.remove_edge(1, 4)  # 8

        self.assertEqual(a.get_mc(), 8)  # 8 changes

    def test_add_edge(self):
        a = DiGraph()
        a.add_node(1)
        a.add_node(2)
        a.add_node(3)
        a.add_node(4)

        self.assertTrue(a.add_edge(1, 2, 1))
        self.assertTrue(a.add_edge(1, 3, 2))
        self.assertTrue(a.add_edge(1, 4, 3))
        self.assertFalse(a.add_edge(1, 5, 2))  # no node 5

    def test_add_node(self):
        a = DiGraph()

        self.assertTrue(a.add_node(1))
        self.assertTrue(a.add_node(2))
        self.assertTrue(a.add_node(3))
        self.assertFalse(a.add_node(1))  # node 1 already added

    def test_remove_node(self):
        a = DiGraph()
        a.add_node(1)
        a.add_node(2)
        a.add_node(3)
        a.add_node(4)

        a.add_edge(1, 2, 1)
        a.add_edge(1, 3, 2)
        a.add_edge(1, 4, 3)

        self.assertTrue(a.remove_node(1))
        self.assertEqual(a.e_size(), 0)  # edges removed
        self.assertEqual(a.all_out_edges_of_node(1), {})  # no edges from node 1
        self.assertFalse(a.remove_node(5))  # no such node

    def test_remove_edge(self):
        a = DiGraph()
        a.add_node(1)
        a.add_node(2)
        a.add_node(3)
        a.add_node(4)

        a.add_edge(1, 2, 1)
        a.add_edge(1, 3, 2)
        a.add_edge(1, 4, 3)

        self.assertTrue(a.remove_edge(1, 2))
        self.assertFalse(a.remove_edge(1, 2))  # already removed
        self.assertFalse(a.remove_edge(2, 1))  # no such edge
        self.assertTrue(a.remove_edge(1, 3))
        self.assertTrue(a.remove_edge(1, 4))
        self.assertEqual(a.e_size(), 0)  # edges removed
