import matplotlib.pyplot as plt
import sys
sys.path.append('../../')
import dynetx as dnx
# import seaborn as sns
G = dnx.DynDiGraph(edge_removal=True)
G.add_node(1)
G.add_interaction(1, 2, t=0)
G.add_interaction(2, 5, t=0)
G.add_interaction(2, 3, t=1)
G.add_interaction(3, 4, t=2)

dnx.draw(G)
