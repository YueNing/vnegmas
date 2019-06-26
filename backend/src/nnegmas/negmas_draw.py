import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def negmas_layout(G, layer_sizes):
    import numpy as np
    left, right, bottom, top, layer_sizes = .1, .9, .3, .9, layer_sizes
    v_spacing = (top - bottom)/float(max(layer_sizes))
    h_spacing = (right - left)/float(len(layer_sizes) - 1)
    node_count = 0
    if not isinstance(G, list):
        A = nx.to_numpy_array(G)
    pos = []
    for i, v in enumerate(layer_sizes):
        layer_top = v_spacing*(v-1)/2. + (top + bottom)/2.
        for j in range(v):
            pos.append(np.array([left + i*h_spacing, layer_top - j*v_spacing], dtype='float64'))
            node_count += 1
    if isinstance(G, list):
        return pos
    else:
        for node in G.nodes:
            if 'pos' in G.nodes[node]:
                pos = []
                poss = nx.get_node_attributes(G, 'pos')
                for node in G.nodes:
                    pos.append(poss[node])
                break
            else:
                break
        pos = dict(zip(G, pos))
        return pos

def negmas_add_nodes(G, layer_sizes, node_name=None):
    import numpy as np
    left, right, bottom, top, layer_sizes = .1, .9, .27, .73, layer_sizes
    v_spacing = (top - bottom)/float(max(layer_sizes))
    h_spacing = (right - left)/float(len(layer_sizes) - 1)
    node_count = 0
    A = nx.to_numpy_array(G)
    color=0
    for i, v in enumerate(layer_sizes):
        layer_top = v_spacing*(v-1)/2. + (top + bottom)/2.
        for j in range(v):
            if node_name is not None:
                G.add_node(node_name[i][j], color=color, pos=np.array([left + i*h_spacing, layer_top - j*v_spacing], dtype='float64'))
            else:
                G.add_node(node_count)
                node_count+=1
        color +=1
    return G

def negmas_add_edges(G, layer_sizes, node_name=None, contracts=None):
    for x, (left_nodes, right_nodes) in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        for i in range(left_nodes):
            for j in range(right_nodes):
                if node_name is not None:
                    if contracts is not None:
                        G.add_edges_from(contracts)
                    else:
                        G.add_edge(node_name[x][i], node_name[x+1][j])
                else:
                    G.add_edge(i+sum(layer_sizes[:x]), j+sum(layer_sizes[:x+1]))    
    return G

def negmas_node_colors(G, layer_sizes=None, dic_mode=False):
    color = 0
    node_colors = []
    if locals['layer_sizes'] is None:
        try:
            if globals['layer_sizes'] is not None:
                locals['layer_sizes'] = globals['layer_sizes']
        except:
            print('layer_sizes is not defined')
    
    for node in G.nodes:
        if 'color' in G.nodes[node]:
            for node in G.nodes:
                node_colors.append(nx.get_node_attributes(G, 'color')[node])
            break
        else:
            for layer in layer_sizes:
                for node in range(layer):
                    node_colors.append(color)
                color +=1
            break
    if dic_mode:
        return dict(zip(G, node_colors))
    else:
        return node_colors

def negmas_edge_colors(G):
    return ['black' for i in range(len(G.edges))]

def negmas_draw(G, edge_colors, node_colors=None, pos=None, ax=None, **kwargs):
    if pos is not None:
        pos = pos
    else:
        pos = nx.get_node_attributes(G, 'pos')
    if node_colors is not None:
        if callable(node_colors):
            node_color = node_colors(G)
        if isinstance(node_colors, list):
            node_color = node_colors
    else:
        node_color = []
        colors = nx.get_node_attributes(G, 'color')
        for node in G.nodes:
            node_color.append(colors[node])
    
    nx.draw(G, pos, ax=ax,
        node_color= node_color, 
        with_labels=True,
        node_size=200, 
        edge_color=edge_colors(G), 
        width=1, 
        cmap=plt.cm.Dark2,
        edge_cmap=plt.cm.Blues
       )
    plt.draw_if_interactive()
    

    
if __name__ == '__main__':    
#     layer_sizes = [3, 3, 3]
    node_name = [['m_1', 'm_2', 'm_3'], 
                    ['my@1_2', 'my@1_3', '_df@1_4'],['_df_1', '_df_2', '_df_3'], ['greedy@2_2', 'greedy@1_2', 'greedy@2_3'], 
                     ['c_0','c_1','c_2']]

    layer_sizes = [len(layer) for layer in node_name]
    contracts = [(node_name[0][0], node_name[1][0]), (node_name[1][0], node_name[2][2]), 
                (node_name[2][2], node_name[3][0]), (node_name[3][0], node_name[4][2])]
    import random
    G = nx.DiGraph()
    G = negmas_add_nodes(G, layer_sizes, node_name)
    G = negmas_add_edges(G, layer_sizes, node_name=node_name, contracts=contracts)
    pos = negmas_layout(G, layer_sizes)
    # print(G.nodes)
    # print(pos)
    # pos = nx.get_node_attributes(G, 'pos')
    negmas_draw(G, negmas_edge_colors, node_colors=negmas_node_colors, pos=pos)
    plt.show()