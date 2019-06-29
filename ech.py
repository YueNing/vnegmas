import json
import os
import datetime
from dataclasses import dataclass

from pyecharts import options as opts
from pyecharts.charts import Graph, Page, Liquid, Bar3D, Grid
from pyecharts.charts import Geo
from pyecharts.commons.types import Numeric, Optional, Sequence, Union
from pyecharts.globals import ChartType, SymbolType
from pyecharts.components import Table
from networkx import DiGraph

from flask.json import jsonify
from flask import Flask, render_template, request
from app import FlaskAppWrapper

from backend.api import draw
from backend.api import nnegmas
from backend.api.nnegmas import negmas_draw
from backend.api import web

"""
mode:   'online_memory':  receive the data when run the simulator and at the same time update the graph (memory mode)
        'online_file'  :  save the world information of simulator at the running time into json file, and read data from 
                            file and update the graph 
        'offline'      :  read data from log file(json) at the end of simulator, with the time series, dynamic update the 
                            graph
        'debug'        : debug mode
"""

mode = 'debug'


class ConfigSetUp:
    def __init__(self):
        self._config = web.get_web_config()
        self._init_my_config()
        self._init_system_config()
    
    def _init_my_config(self):
        self.my_config = {}
    
    def _init_system_config(self):
        # print(self._config._sections)
        # import pdb; pdb.set_trace()
        self.system_config = {'system_general':{'content':self._config._sections['system_general'], 'path':{}}, 
                            'system_competitors':{'content':self._config._sections['system_competitors'], 'path':{}}, 
                            'system_negotiation':{'content':self._config._sections['system_negotiation'], 'path':{}}
                            }
    
    @property
    def get_my_config(self):
        return self.my_config 
    
    @property
    def get_system_config(self):
        return self.system_config

    def save_my_config(self, content):
        print('my config {}'.format(content))
    
    def save_system_config(self, content):
        print('system config {}'.format(content))
        
@dataclass
class Setup_Graph:
    name: str
    linestyleopts: Union[Sequence[Union[opts.LineStyleOpts, dict]], None]
    graph: Union[DiGraph, dict]
    layer_sizes: list
    node_name: list

class DrawPyechart(object):
    def __init__(self, g: Union[DiGraph, None] = None, 
                    node_name=None, name=__name__, 
                    static_folder="templates", 
                    mode='debug'
        ):
        if mode == 'debug':
            # from backend.src.nnegmas.negmas_draw import negmas_node_colors
            g = DiGraph()
            nodes = [['m_1', 'm_2', 'm_3'], ['f_1', 'f_2'], ['g_1', 'g_2'], ['c_1', 'c_2']]
            self.node_name = nodes
            self.layer_sizes = self._get_layer_sizes()
            g = negmas_draw.negmas_add_nodes(g, self.layer_sizes, self.node_name)
            self.g = g
            self.name = name
            self._init()
            self.config = Setup_Graph(self.name, self.linestyleopts, self.g, self.layer_sizes, self.node_name)
        self.current_step = -1
        self.result = {'liquid_chart_dyn':[0.0, 0.0], 'bar3d_activation_agents_dyn':[], 'graph_result':[]}
        a = nnegmas.ShowProcess(world_recall_reuslt_dict=nnegmas.glovar.world_recall_reuslt_dict,draw_backend="pyecharts_flask")
        self.show = a
        self.frame = self.show.iter_frame()
        self.worldname = 'None'
        self.a = FlaskAppWrapper(self.name, static_folder=static_folder)
        self._endpoints()
        # self.a.run()
    
    def run(self):
        self.a.run()

    def _init(self):
        self.linestyleopts = [
            opts.LineStyleOpts(width=5),
        ]


    def _endpoints(self):
        self.a.add_endpoint(rule='/', endpoint='home', view_func=self.index)
        self.a.add_endpoint(rule='/my', endpoint='my', view_func=self.my_config)
        self.a.add_endpoint(rule='/system', endpoint='system', view_func=self.system_config)
        self.a.add_endpoint(rule='/config_general', endpoint='config_general', view_func=self.system_config_general)
        self.a.add_endpoint(rule='/config_competitors', endpoint='config_competitors', view_func=self.system_config_competitors)
        self.a.add_endpoint(rule='/config_negotiation', endpoint='config_negotiation', view_func=self.system_config_negotiation)
        self.a.add_endpoint(rule='/real_time', endpoint='real_time', view_func=self.real_time)
        self.a.add_endpoint(rule='/GraphChart', endpoint='GraphChart', view_func=self._graph_with_opts)
        self.a.add_endpoint(rule='/Liquid', endpoint='Liquid', view_func=self._get_liquid_chart)
        self.a.add_endpoint(rule='/BarProcutProduce', endpoint='BarProcutProduce', view_func=self._get_bar_product_produce)
        self.a.add_endpoint(rule='/RealTimeDynamicData', endpoint='RealTimeDynamicData', view_func=self.dynamic_real_time)
        # self.a.add_endpoint(rule='/GraphDynamicData', endpoint='GraphDynamicData', view_func=self._graph_with_opts_dyn)
        self.a.add_endpoint(rule='/Bar3dData', endpoint='Bar3dData', view_func=self._bar3d_with_opts)
        self.a.add_endpoint(rule='/Grid', endpoint='Grid', view_func=self._get_buyer_seller)
        self.a.add_endpoint(rule='/run', endpoint='run', view_func=self._run_negmas)
        self.a.add_endpoint(rule='/saveSystemConfig', endpoint='savesystemconfig', view_func=self.save_system_config, methods=['POST', 'GET'])

    def index(self):
        return render_template("index.html")

    def real_time(self):
        return render_template("_real_time.html")
    
    def my_config(self):
        return render_template("_config_my.html")

    def system_config(self):
        content = self._get_system_config()['system_general']['content']
        return render_template("_config_system.html", title='General Setting', content=content)
    
    def system_config_general(self):
        content = self._get_system_config()['system_general']['content']
        return render_template("_config_system_basic.html", title='General Setting', content=content)
    
    def system_config_competitors(self):
        content = self._get_system_config()['system_competitors']['content']
        return render_template("_config_system_basic.html", title='Competitors Setting', content=content)
    
    def system_config_negotiation(self):
        content = self._get_system_config()['system_negotiation']['content']
        return render_template("_config_system_basic.html", title='Negotiation Setting', content=content)
    
    def save_system_config(self):
        if not hasattr(self, 'configSetUp'):
            self._init_configSetup()
        self.configSetUp.save_system_config(request.form)
        content = self._get_system_config()[request.form.get('sub')]['content']
        print(request.form.getlist('competitors'))
        return render_template("result.html", content=content)
    
    def save_my_config(self):
        if not hasattr(self, 'configSetUp'):
            self._init_configSetup()
        self.configSetUp.save_my_config(request.data)

    def dynamic_real_time(self):
        def send_result(contracts=None):
            g = negmas_draw.negmas_add_edges(self.config.graph, self.config.layer_sizes, node_name=self.config.node_name, contracts=contracts)
            edges = [(edge[0], edge[1]) for edge in g.edges]
            links = [opts.GraphLink(source=edge[0], target=edge[1]) for edge in edges]
            result = []
            for link in links:
                result.append({"source": link.opts['source'], "target": link.opts['target']})
            return result
        
        def update_key_value(data):
            result = {}
            for key, value in data.items():
                result[key] = value
            return result

        def _get_liquid_chart_dyn(step):
            liquid_dyn_data = [step / 100.0, step / 100.0]
            return liquid_dyn_data
        
        def _get_bar3d_activation_agents_dyn(data):
            bar3d_activation_agents_data = []
            return bar3d_activation_agents_data
        
        if hasattr(self, 'check_init_graph') and self.check_init_graph:
            data = next(self.frame)
            # print(data)
            if data[0] == self.current_step:
                result = update_key_value(self.result)
                graph_result = [{}]
                self.runningtime = datetime.datetime.now() - self.starttime
            else:
                step = data[0]
                contracts = data[1]
                self.worldname = data[2]
                self.market_size_total = data[3]
                graph_result = send_result(contracts=contracts)
                # print(graph_result)
                self.current_step = data[0]
                graph_result = send_result(contracts=contracts)
                result = {'liquid_chart_dyn':_get_liquid_chart_dyn(step), 'bar3d_activation_agents_dyn':_get_bar3d_activation_agents_dyn(contracts)}
                self.current_step = data[0]
                self.result = update_key_value(result)
                self.runningtime = datetime.datetime.now() - self.starttime
        else:
            result = update_key_value(self.result)
            graph_result = send_result()
            self.runningtime = -1
            self.worldname = 'None'
            self.current_step = -1
            self.market_size_total = -1
        result['graph_result'] = graph_result
        result['worldname'] = self.worldname
        result['market_size_total'] = self.market_size_total
        result['current_step'] = self.current_step
        result['runningtime'] = str(self.runningtime)
        return jsonify(result)
    
    def _run_negmas(self):
        #TODO set up negmas task
        # from backend.src import nnegmas
        from multiprocessing import Process

        self.mode  = 'online_memory'
        self.starttime = datetime.datetime.now()
        ### Negmas 
        negmas = Process(target=nnegmas.run_negmas)
        negmas.start()
        
        # a.show()
        return jsonify({'message':'set run task'})

    @staticmethod
    def _get_bar_product_produce():
        c = draw.bar_product_produce()
        return c.dump_options()
    
    @staticmethod
    def _get_liquid_chart():
        c = draw.liquid_process()
        return c.dump_options()
    
    @staticmethod
    def _bar3d_with_opts():
        c = draw.bar3d_agent_activation()
        return c.dump_options()
    
    @staticmethod
    def _get_buyer_seller():
        return draw.grid_buyer_seller().dump_options()
    
    def _get_layer_sizes(self):
        return [len(node) for node in self.node_name]
    
    def _graph_with_opts(self):
        # print('_graph_with_opts')

        nnegmas.glovar.event.wait()
        # print("receive result {}".format(nnegmas.glovar.world_recall_reuslt_dict))
        self.check_init_graph = True
        nodes = self.show.get_nodes()
        # print('nodes:{}'.format(nodes))
        g = DiGraph()
        self.node_name = nodes
        self.layer_sizes = self._get_layer_sizes()
        g = negmas_draw.negmas_add_nodes(g, self.layer_sizes, self.node_name)
        self.g = g
        self._init()
        self.config = Setup_Graph(self.name, self.linestyleopts, self.g, self.layer_sizes, self.node_name)

        # print('nodes:{}'.format(self.config.graph.nodes))
        config = {'emphasis_linestyleopts': self.config.linestyleopts[0]}
        c = draw.graph_contracted_signed(config, self.config.graph.nodes)
        return c.dump_options()
    
    def init_bar3d_base(self):
        from example.commons import Faker
        from pyecharts import options as opts
        from pyecharts.charts import Bar3D
        c = (
            Bar3D()
            .add(
                "",
                [],
                xaxis3d_opts=opts.Axis3DOpts(Faker.clock, type_="category"),
                yaxis3d_opts=opts.Axis3DOpts(Faker.week_en, type_="category"),
                zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            )
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=20),
                title_opts=opts.TitleOpts(title=""),
            )
        )
        return c

    def _graph_with_opts_dyn(self):
        def send_result(contracts=None):
            g = negmas_draw.negmas_add_edges(self.config.graph, self.config.layer_sizes, node_name=self.config.node_name, contracts=contracts)
            edges = [(edge[0], edge[1]) for edge in g.edges]
            links = [opts.GraphLink(source=edge[0], target=edge[1]) for edge in edges]
            result = []
            for link in links:
                result.append({"source": link.opts['source'], "target": link.opts['target']})
            return result
    
        if hasattr(self, 'check_init_graph') and self.check_init_graph:
            # data = next(self.frame)
            if data[0] == self.current_step:
                result = [{}]
            else:
                contracts = data[1]
                result = send_result(contracts=contracts)
                self.current_step = data[0]
        else:
            result = send_result()
        # print('dynamic data {}'.format(nnegmas.glovar.world_recall_reuslt_dict))
        # return jsonify(result)
        return result

    def _init_configSetup(self):
        self.configSetUp = ConfigSetUp()
    
    def _get_my_config(self) -> dict:
        if not hasattr(self, 'configSetUp'):
            self._init_configSetup()
        return self.configSetUp.get_my_config

    def _get_system_config(self) -> dict:
        if not hasattr(self, 'configSetUp'):
            self._init_configSetup()
        return self.configSetUp.get_system_config

def get_layer_sizes(nodes):
    return [len(node) for node in nodes]

def index():
    # liquid = graph_with_opts()
    # return render_template("index.html", myechart=liquid.render_embed())
    return 'hello'

def bar3d_base() -> Bar3D:
        import random
        from example.commons import Faker
        from pyecharts import options as opts
        from pyecharts.charts import Bar3D
        data = [(i, j, random.randint(0, 12)) for i in range(6) for j in range(24)]
        c = (
            Bar3D()
            .add(
                "",
                [[d[1], d[0], d[2]] for d in data],
                xaxis3d_opts=opts.Axis3DOpts(Faker.clock, type_="category"),
                yaxis3d_opts=opts.Axis3DOpts(Faker.week_en, type_="category"),
                zaxis3d_opts=opts.Axis3DOpts(type_="value"),
            )
            .set_global_opts(
                visualmap_opts=opts.VisualMapOpts(max_=20),
                title_opts=opts.TitleOpts(title=""),
            )
        )
        return c

def draw_with_pyecharts():
    """
     use pyecharts to generate the echarts graph, and show the interactive graph with flask
     `pip install flask pyecharts networkx`
    """
    app = Flask(__name__, static_folder="templates")

def geo_base() -> Geo:
    c = (
        Geo()
        .add_schema(maptype="china")
        .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title=""),
        )
    )
    return c

def geo_visualmap_piecewise() -> Geo:
    c = (
        Geo()
        .add_schema(maptype="europe")
        # .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=True),
            title_opts=opts.TitleOpts(title=""),
        )
    )
    return c

def graph_with_opts_dyn() -> Sequence[Union[opts.GraphLink, dict]]:
    
    links = [
        opts.GraphLink(source="n2", target="n4"),
    ]
    return links

def graph_with_opts() -> Graph:
    g = []
    layer_sizes = [2, 2, 1]
    pos = negmas_draw.negmas_layout(g, layer_sizes)
    nodes = [
        opts.GraphNode(name="n1", x=pos[0][0], y=pos[0][1], symbol_size=10, category='c1'),
        opts.GraphNode(name="n2", x=pos[1][0], y=pos[1][1], symbol_size=20, category='c2'),
        opts.GraphNode(name="n3", x=pos[2][0], y=pos[2][1], symbol_size=30, category='c3'),
        opts.GraphNode(name="n4", x=pos[3][0], y=pos[3][1], symbol_size=40, category='c1'),
        opts.GraphNode(name="n5", x=pos[4][0], y=pos[4][1], symbol_size=50, category='c1'),
    ]
    
    linestyleopts = [
        opts.LineStyleOpts(width=5),
        ]
    
    links = [
        opts.GraphLink(source="n1", target="n2"),
        opts.GraphLink(source="n2", target="n3"),
        opts.GraphLink(source="n3", target="n4"),
        opts.GraphLink(source="n4", target="n5"),
        opts.GraphLink(source="n5", target="n1"),
    ]

    categories = [
        opts.GraphCategory(name='c1'),
        opts.GraphCategory(name='c2'),
        opts.GraphCategory(name='c3'),
        opts.GraphCategory(name='c4'),
        opts.GraphCategory(name='c5'),
        ]
    
    c = (
        Graph()
        .add("", nodes, links, categories, edge_symbol=['', 'arrow'], edge_symbol_size=10,layout='none', repulsion=4000,
        emphasis_itemstyle_opts=linestyleopts[0])
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
    )
    return c

def liquid_base() -> Liquid:
    c = (
        Liquid()
        .add("lq", [0.6, 0.7])
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
    )
    return c


def table_base() -> Table:
    from pyecharts.options import ComponentTitleOpts

    table = Table()

    headers = ["Agent name", "Balance", "Signed Contracts", "Executed Contracts"]
    rows = [
        ["Brisbane", 5905, 1857594, 1146.4],
        ["Adelaide", 1295, 1158259, 600.5],
        ["Darwin", 112, 120900, 1714.7],
        ["Hobart", 1357, 205556, 619.5],
        ["Sydney", 2058, 4336374, 1214.8],
        ["Melbourne", 1566, 3806092, 646.9],
        ["Perth", 5386, 1554769, 869.4],
    ]
    table.add(headers, rows).set_global_opts(
        title_opts=ComponentTitleOpts(title="", 
                title_style={"style": "font-size: 18px; font-weight:bold;"})
    )
    return table

if __name__ == '__main__':
    dp = DrawPyechart(name='DrawPyecharts')
    dp.run()
    # table_base().render()
