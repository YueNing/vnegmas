from . import glovar
from .. import dynetx as dnx
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider
# from threading import Event
import itertools
from . import negmas_draw
import time
class ShowProcess:
    """
    ax, fig: Union[,None], when use matplotlib this parameter are needed
    draw_backend: Union['matplotlib', 'pyecharts']
    mode: Union['online_memory', 'online_file', 'offline'], different mode the process are different
    function:
            used for pyecharts as backend of draw
            get_nodes: call function init to setup the initial nodes of agents, and return a list containt different levels agents
                        for example: [miners, level1s, level2s, level3s, consumers]
            iter_frame: generator return information of every step of every world, change the code here to get different informaton about world, 
            but must confirm that eventengine has save this information into shared dict that between different process (world_recall_reuslt_dict)
    """
    def __init__(self, ax=None, fig=None, world_recall_reuslt_dict=None, 
                    draw_backend='matplotlib', mode='online_memory', *args, **kwargs):
        self.ax = ax
        self.fig = fig
        self.world_recall = 0
        self.iterf = self.iter_frame()
        self._world_recall_reuslt_dict = world_recall_reuslt_dict
        self.draw_backend = draw_backend
        self.mode = mode
        if 'scmlworld' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['scmlworld'] = 'None'
        if 'current_step' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['current_step'] = -1
        if 'factories_managers' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['factories_managers'] = 'None'
        if 'consumers' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['consumers'] = 'None'
        if 'miners' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['miners'] = 'None'
        if 'market_size_total' not in self._world_recall_reuslt_dict:
            self._world_recall_reuslt_dict['market_size_total'] = 'None'

    def iter_frame(self):
        step = 0
        step_information = 0
        while True:
            step_information = self._world_recall_reuslt_dict['current_step'] if 'current_step' in self._world_recall_reuslt_dict else 0
            scmlworld = self._world_recall_reuslt_dict['scmlworld']
            factories_managers = self._world_recall_reuslt_dict['factories_managers']
            consumers = self._world_recall_reuslt_dict['consumers']
            miners = self._world_recall_reuslt_dict['miners']
            contracts = self._world_recall_reuslt_dict['contracts']
            market_size_total = self._world_recall_reuslt_dict['market_size_total']
            yield [step_information, contracts, scmlworld, market_size_total]
            step +=1

    def get_nodes(self):
        self.init()
        return self.init_nodes

    def init(self):
        # if self.draw_backend == 'matplotlib':
        glovar.event.wait()
        step_information = self._world_recall_reuslt_dict['current_step'] if 'current_step' in self._world_recall_reuslt_dict else 0
        scmlworld = self._world_recall_reuslt_dict['scmlworld']
        factories_managers = self._world_recall_reuslt_dict['factories_managers']
        consumers = self._world_recall_reuslt_dict['consumers']
        miners = self._world_recall_reuslt_dict['miners']

        node_name = [miners, consumers]
        
        # print('world {}'.format(self._world_recall_reuslt_dict))
        # todo:
        def _factories_managers_levels(f_ms):
            # print('f_ms {}'.format(f_ms))
            factories_managers_with_level = []
            for f_m in f_ms:
                level = f_m.split('_')[-2][-1]
                try:
                    if f_m not in factories_managers_with_level[int(level) - 1]:
                        factories_managers_with_level[int(level)-1].append(f_m)
                except:
                    for l in range(int(level)-len(factories_managers_with_level)):
                        factories_managers_with_level.append([])
                    factories_managers_with_level[int(level)-1].append(f_m)                    
            # print(factories_managers_with_level)
            return factories_managers_with_level
    
        index = 1
        g = _factories_managers_levels(factories_managers)
        # print('g:{}'.format(g))
        for f_m in _factories_managers_levels(factories_managers):
            node_name.insert(index, f_m)
            index+=1
        print()
        # print('node_name:{}'.format(node_name))
        self.init_nodes = node_name

        layer_sizes = [len(layer) for layer in node_name]
        self.g = nx.DiGraph()
        self.g = negmas_draw.negmas_add_nodes(self.g, layer_sizes, node_name)
        self.pos = negmas_draw.negmas_layout(self.g, layer_sizes)
        if self.draw_backend == 'matplotlib':
            plt.title('world:{}'.format(scmlworld), fontsize='large', fontweight='bold')
            self.text_step = plt.text(0.48, 0, 'step: 0',fontsize=20)
            self.text_contracts = plt.text(0, 0, 'contracts singed information')
            negmas_draw.negmas_draw(self.g, negmas_draw.negmas_edge_colors, node_colors=negmas_draw.negmas_node_colors, pos=self.pos)
        elif self.draw_backend == 'pyecharts_flask':
            pass


    def update(self,frame):
        step_information = 'step:{}'.format(frame[0])
        contracts_singed_information = 'contracts:\nseller:buyer\n'
        for contract in frame[1]:
            contracts_singed_information+=contract[0] + ':' + contract[1] + '\n'
        self.text_step.set_text(step_information)
        self.text_contracts.set_text(contracts_singed_information)
        self.current_frame = frame
        self.g.add_edges_from(frame[1])
        # dnx.draw_networkx_nodes(self.g, node_color='black', pos=self.pos)
        # sc = AnimatedScatter(self)
        dnx.draw_networkx_edges(self.g, pos=self.pos, arrows=True)
        print('update a step')
        # return scat,

    def show(self):
        ai = FuncAnimation(self.fig, self.update, frames=self.iterf, interval=100, init_func=self.init)
        plt.get_current_fig_manager().full_screen_toggle()
        plt.show(block = True)


class AnimatedScatter(object):
    def __init__(self, show):
        self.show = show
        self.update()
    
    def update(self):
        # self.show.g.nodes(self.show.current_frame)
        # print(self.show.current_frame)
        
        def _iter_color():
            return [self.show.g.nodes[node]['color'] for node in self.show.g.nodes]

        def _iter_dict_color():
            color = {}
            for node in self.show.g.nodes:
                color[node] = self.show.g.nodes[node]['color']
            return color
        
        back_node_color = _iter_color()
        back_node_dict_color = _iter_dict_color()
        print('back_node_color: {}'.format(back_node_color))
        try:
            for contract in self.show.current_frame[1]:
                seller = contract[0]
                buyer = contract[1]
                if seller in self.show.g.nodes:
                    self.show.g.nodes[seller]['color'] = 0
                if buyer in self.show.g.nodes:
                    self.show.g.nodes[buyer]['color'] = 10
            node_color = _iter_color()
            print(node_color)
            for i in range(1):
                dnx.draw_networkx_nodes(self.show.g, node_color=node_color, pos=self.show.pos)
                # negmas_draw.negmas_draw(self.show.g, negmas_draw.negmas_edge_colors, node_colors=node_color, pos=self.show.pos)
                time.sleep(0.2)
                dnx.draw_networkx_nodes(self.show.g, node_color='red', pos=self.show.pos)
                time.sleep(0.2)
                dnx.draw_networkx_nodes(self.show.g, node_color=back_node_color, pos=self.show.pos)

            for node, color in back_node_dict_color.items():
                self.show.g.nodes[node]['color'] = color
            print('test_color: {}'.format(_iter_color()))
        except:
            print('get some error when run Animation scatter!')

if __name__ == "__main__":
    # fig, ax = plt.subplots()
    # world_recall_reuslt_dict = {'current_step':5, 'scmlworld':'test_world', 'factories_managers':['_df_1','my@1_2','greedy@2_2'],
    #                                                             'consumers':['c_0','c_1','c_2'], 'miners':['m_1', 'm_2', 'm_3']}
    # a = ShowProcess(ax=ax, fig=fig, world_recall_reuslt_dict=world_recall_reuslt_dict)
    # a.show()

    import time
    G = nx.DiGraph()
    G.add_node('test1' , color='red')
    nx.draw(G, node_color=G.nodes['test1']['color'])
    time.sleep(3)
    plt.draw_if_interactive()
    
    color = G.nodes['test1']['color']
    G.nodes['test1']['color'] = 'blue'
    nx.draw(G, node_color=G.nodes['test1']['color'])
    plt.draw_if_interactive()
    # time.sleep(1)
    # G.nodes['test1']['color'] = color
    # nx.draw(G, node_color=G.nodes['test1']['color'])
    plt.show()
    
