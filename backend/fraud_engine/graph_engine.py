import networkx as nx

class GraphEngine:
    def __init__(self):
        self.G = nx.Graph()

    def add_tx(self, s, r):
        self.G.add_edge(s, r)

    def edges(self):
        return [{"from":u,"to":v} for u,v in self.G.edges()]

graph_engine = GraphEngine()
