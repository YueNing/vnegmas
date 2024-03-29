import datetime, time
import json
import os
from dataclasses import dataclass

from flask import Flask, render_template, request
from flask.json import jsonify
from networkx import DiGraph

from vnegmas.app import FlaskAppWrapper
from vnegmas.backend.api import draw, nnegmas, web
from vnegmas.backend.api.nnegmas import negmas_draw, watch_fs
from vnegmas.backend.src.pyecharts import options as opts
from vnegmas.backend.src.pyecharts.charts import Bar3D, Geo, Graph, Grid, Liquid, Page
from vnegmas.backend.src.pyecharts.commons.types import (Numeric, Optional, Sequence,
                                                 Union)
from vnegmas.backend.src.pyecharts.components import Table
from vnegmas.backend.src.pyecharts.globals import ChartType, SymbolType
import asyncio
from multiprocessing import Process

"""
mode:   'online_memory':  receive the data when run the simulator and at the same time update the graph (memory mode)
        'online_file'  :  save the world information of simulator at the running time into json file, and read data from 
                            file and update the graph 
        'offline'      :  read data from log file(json) at the end of simulator, with the time series, dynamic update the 
                            graph
        'debug'        : debug mode
"""

mode = "debug"


class ConfigSetUp:
    """
        Class used for
        All information about config 
    """
    def __init__(self):
        self._config = web.get_web_config()
        self._real_time_config = web.get_real_time_config()
        self._init_my_config()
        self._init_system_config()

    def _init_my_config(self):
        self.my_config = {}

    def _init_system_config(self):
        # print(self._config._sections)
        # import pdb; pdb.set_trace()
        self.system_config = {
            "system_general": {
                "content": self._config._sections["system_general"],
                "path": {},
            },
            "system_competitors": {
                "content": self._config._sections["system_competitors"],
                "path": {},
            },
            "system_negotiation": {
                "content": self._config._sections["system_negotiation"],
                "path": {},
            },
        }

    @property
    def get_my_config(self):
        return self.my_config

    @property
    def get_system_config(self):
        return self.system_config

    def save_my_config(self, content):
        print(f"my config {content}")

    # TODO: system config update
    def save_system_config(self, content):
        print(f"system config {content}")
    
    def save_real_time_config(self, content):
        self._real_time_config.update(content)
    
    def get_real_time_config(self):
        return self._real_time_config.config


@dataclass
class Setup_Graph:
    name: str
    linestyleopts: Union[Sequence[Union[opts.LineStyleOpts, dict]], None]
    graph: Union[DiGraph, dict]
    layer_sizes: list
    node_name: list


class VNegmas(object):
    """
        The main Class of VNEGMAS, router and interaction between backend of frontend
        
        .. versionadd:: v0.1.1
            ...
        
        .. versionadd:: v0.2.1
            function offline_demo is added, parameter check_init_graph is added into __init__

        : param check_init_graph: checked the status in the `real_time` mode
    """
    def __init__(
        self,
        g: Union[DiGraph, None] = None,
        node_name=None,
        name=__name__,
        template_folder="./templates",
        static_folder="./stats",
        mode="debug",
    ):
        if mode == "debug":
            # from backend.src.nnegmas.negmas_draw import negmas_node_colors
            g = DiGraph()
            nodes = [
                ["m_1", "m_2", "m_3"],
                ["f_1", "f_2"],
                ["g_1", "g_2"],
                ["c_1", "c_2"],
            ]
            self.node_name = nodes
            self.layer_sizes = self._get_layer_sizes()
            g = negmas_draw.negmas_add_nodes(g, self.layer_sizes, self.node_name)
            self.g = g
            self.name = name
            self._init()
            self.config = Setup_Graph(
                self.name, self.linestyleopts, self.g, self.layer_sizes, self.node_name
            )
        self.current_step = -1
        self.result = {
            "liquid_chart_dyn": [0.0, 0.0],
            "bar3d_activation_agents_dyn": [],
            "graph_result": [],
        }
        a = nnegmas.ShowProcess(
            world_recall_reuslt_dict=nnegmas.glovar.world_recall_reuslt_dict,
            draw_backend="pyecharts_flask",
        )
        self.show = a
        self.frame = self.show.iter_frame()
        self.worldname = "None"
        self.template_dir = os.path.join(os.path.dirname(__file__), template_folder)
        self.stats_dir = os.path.join(os.path.dirname(__file__), static_folder)
        self.check_init_graph = False
        # import pdb; pdb.set_trace()
        # import pdb; pdb.set_trace()
        self.a = FlaskAppWrapper(self.name, template_folder=self.template_dir, static_folder=self.stats_dir)
        self._endpoints()
        self._init_configSetup()
        # self.a.run()

    def run(self):
        self.server = Process(target=self.a.run)
        self.server.start()
        self.server.join()
        import threading
        
        print('vnegmas threading is {}'. format(threading.current_thread()))
        import os

        print("vnegmas process id is {}".format(os.getpid()))
        # self.a.run()
    
    def stop(self):
        self.server.terminate()
        self.server.join()
    
    def _init(self):
        self.linestyleopts = [opts.LineStyleOpts(width=5)]

    def _endpoints(self):
        self.a.add_endpoint(rule="/", endpoint="home", view_func=self.index)
        self.a.add_endpoint(rule="/my", endpoint="my", view_func=self.my_config)
        self.a.add_endpoint(
            rule="/system", endpoint="system", view_func=self.system_config
        )
        self.a.add_endpoint(
            rule="/config_general",
            endpoint="config_general",
            view_func=self.system_config_general,
        )
        self.a.add_endpoint(
            rule="/config_competitors",
            endpoint="config_competitors",
            view_func=self.system_config_competitors,
        )
        self.a.add_endpoint(
            rule="/config_negotiation",
            endpoint="config_negotiation",
            view_func=self.system_config_negotiation,
        )
        self.a.add_endpoint(
            rule="/real_time", endpoint="real_time", view_func=self.real_time
        )
        self.a.add_endpoint(
            rule="/offline",  endpoint="offline", view_func=self.offline_demo
        )
        self.a.add_endpoint(
            rule="/GraphChart", endpoint="GraphChart", view_func=self._graph_with_opts
        )
        self.a.add_endpoint(
            rule="/Liquid", endpoint="Liquid", view_func=self._get_liquid_chart
        )
        self.a.add_endpoint(
            rule="/RealTimeDynamicData",
            endpoint="RealTimeDynamicData",
            view_func=self.dynamic_real_time,
        )
        # self.a.add_endpoint(rule='/GraphDynamicData', endpoint='GraphDynamicData', view_func=self._graph_with_opts_dyn)
        self.a.add_endpoint(rule="/run", endpoint="run", view_func=self._run_negmas)
        self.a.add_endpoint(
            rule="/saveSystemConfig",
            endpoint="savesystemconfig",
            view_func=self.save_system_config,
            methods=["POST", "GET"],
        )
        self.a.add_endpoint(
            rule="/config/save_real_time",
            endpoint="saverealtimeconfig",
            view_func=self.save_real_time_config,
            methods=["POST", "GET"],
        )

    def index(self):
        return render_template("index.html")

    #TODO need to define the charts layout, size, position, name, and so on
    def _selected_charts(self, charts):
        """
         define the row, size, name and so on information about charts
        """
        selected_charts = [{"name":"", "position":"", "size":"", "description":""}, {}, {}, {}]
        return selected_charts
    
    def _get_real_time_config(self):
        real_time_config = self.configSetUp.get_real_time_config()
        self.real_time_selected_charts = []
        for mode in real_time_config._sections['mode']:
            if real_time_config._sections['mode'][mode] == 'True':
                self.real_time_mode = mode
        for chart in real_time_config._sections['charts']:
            if real_time_config._sections['charts'][chart] == "True":
                self.real_time_selected_charts.append(chart)
        content = {'type':"real time config", "mode": real_time_config._sections['mode'], 
                        "charts": real_time_config._sections['charts'], "charts_size":len(real_time_config._sections['charts']) // 2, "selected_mode":self.real_time_mode, "selected_charts":self.real_time_selected_charts}
        return content
    
    def real_time(self):
        content = self._get_real_time_config()
        return render_template("_real_time.html", content=content)

    #TODO offline demo for ijcai, receive data from the log and related statistic files
    #TODO Use demo file from NEGMAS
    def offline_demo(self):
        """
            Just a offline demo that used for shown at the conference IJCAI
            .. versionadd:: v0.2.1
                the function offline_demo is added
        """
        from vnegmas.backend.api.data import OfflineData
        from vnegmas.settings import OFFLINE_DEFAULT_CHARTS
        from vnegmas.backend.api.draw import get_specific_type_chart
        offline_data = OfflineData()
        offline_data._loads()
        selected_charts = {key: offline_data.stats[key]  for key in OFFLINE_DEFAULT_CHARTS}
        #print(f"selected charts {selected_charts}")
        
        data = {}
        content=[]
        for key in selected_charts:
            data["yaxis_data"] = selected_charts[key]
            data["title"] = key
            data["xaxis_data"] = [s+1 for s in range(len(selected_charts[key]))]
            content.insert(0, {"title":key, "value":get_specific_type_chart(data=data, type="line").render_embed()})
        # content = [c.render_embed() for c in charts]
        # content = {c.render_embed() for c in charts]
        return render_template("_offline_demo.html", content=content)

    def my_config(self):
        return render_template("_config_my.html")

    def system_config(self):
        content = self._get_system_config()["system_general"]["content"]
        return render_template(
            "_config_system.html", title="General Setting", content=content
        )

    def system_config_general(self):
        content = self._get_system_config()["system_general"]["content"]
        return render_template(
            "_config_system_basic.html", title="General Setting", content=content
        )

    def system_config_competitors(self):
        content = self._get_system_config()["system_competitors"]["content"]
        return render_template(
            "_config_system_basic.html", title="Competitors Setting", content=content
        )

    def system_config_negotiation(self):
        content = self._get_system_config()["system_negotiation"]["content"]
        return render_template(
            "_config_system_basic.html", title="Negotiation Setting", content=content
        )

    def save_system_config(self):
        if not hasattr(self, "configSetUp"):
            self._init_configSetup()
        self.configSetUp.save_system_config(request.form)
        content = self._get_system_config()[request.form.get("sub")]["content"]
        print(request.form.getlist("competitors"))
        content = self._get_system_config()["system_general"]["content"]
        # return render_template("result.html", content=content)
        return render_template(
            "_config_system.html", title="General Setting", content=content
        )

    def save_real_time_config(self):
        if not hasattr(self, "configSetUp"):
            self._init_configSetup()
        self.configSetUp.save_real_time_config(request.form)
        # new_content = self.configSetUp.get_real_time_config()
        content = self._get_real_time_config()
        return jsonify(content)

    def save_my_config(self):
        if not hasattr(self, "configSetUp"):
            self._init_configSetup()
        self.configSetUp.save_my_config(request.data)

    def dynamic_real_time(self):
        """
            update the charts in the `real time` mode
        """
        def send_result(contracts=None):
            g = negmas_draw.negmas_add_edges(
                self.config.graph,
                self.config.layer_sizes,
                node_name=self.config.node_name,
                contracts=contracts,
            )
            edges = [(edge[0], edge[1]) for edge in g.edges]
            links = [opts.GraphLink(source=edge[0], target=edge[1]) for edge in edges]
            result = []
            for link in links:
                result.append(
                    {"source": link.opts["source"], "target": link.opts["target"]}
                )
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

        if hasattr(self, "check_init_graph") and self.check_init_graph:
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
                result = {
                    "liquid_chart_dyn": _get_liquid_chart_dyn(step),
                    "bar3d_activation_agents_dyn": _get_bar3d_activation_agents_dyn(
                        contracts
                    ),
                }
                self.current_step = data[0]
                self.result = update_key_value(result)
                self.runningtime = datetime.datetime.now() - self.starttime
        else:
            result = update_key_value(self.result)
            graph_result = send_result()
            self.runningtime = -1
            self.worldname = "None"
            self.current_step = -1
            self.market_size_total = -1
        result["graph_result"] = graph_result
        result["worldname"] = self.worldname
        result["market_size_total"] = self.market_size_total
        result["current_step"] = self.current_step
        result["runningtime"] = str(self.runningtime)
          # DEMO USED FOR IJCAI
        if self.check_init_graph:
            print(f"node names are {self.node_name}")
            from vnegmas.backend.api.data import Faker
            result["product_produce"] = Faker.get_product_factories_produce_dynamic(factories=self.factories)
            # result["buyer_and_seller"] = Faker.get_buy_and_sell_data_dynamic(factories=self.factories)
            result["activation_level"] = Faker.get_activations_level_dynamic(factories=self.factories)
        
        return jsonify(result)

    def _run_negmas(self):
        # TODO set up negmas task use web api
        # from backend.src import nnegmas
        from multiprocessing import Process

        self.mode = "online_serial"
        self.starttime = datetime.datetime.now()
        ### Negmas
        negmas = Process(target=nnegmas.run_negmas)
        negmas.start()

        # a.show()
        return jsonify({"message": "set run task"})

    @staticmethod
    def _get_bar_product_produce(products, factories, data):
        c = draw.bar_product_produce(products, factories, data)
        return c.dump_options()

    @staticmethod
    def _get_liquid_chart():
        c = draw.liquid_process()
        return c.dump_options()

    @staticmethod
    def _activation_level(steps, factories, data):
        c = draw.bar3d_agent_activation(steps, factories, data)
        return c.dump_options()

    @staticmethod
    def _get_buyer_seller(factories, products, data):
        c = draw.grid_buyer_seller(factories, products, data)
        return c .dump_options()

    def _get_layer_sizes(self):
        return [len(node) for node in self.node_name]

    def _graph_with_opts(self):
        """
                .. versionadded: v0.1.1
                    used for just initial the Graph (contract signed)
                
                .. versionadded: v0.2.1
                    not just used for Graph, also intial for all of the charts in the page of real time, 
                    product, activation_level, buy_and_sell, breach, negotiations and so on.
        """
        nnegmas.glovar.event.wait()
        #print("receive result {}".format(nnegmas.glovar.world_recall_reuslt_dict))
        self.check_init_graph = True
        #  get a list of of all nodes
        nodes = self.show.get_nodes()
        # print('nodes:{}'.format(nodes))
        g = DiGraph()
        self.node_name = nodes
        self.layer_sizes = self._get_layer_sizes()
        g = negmas_draw.negmas_add_nodes(g, self.layer_sizes, self.node_name)
        self.g = g
        self._init()
        self.config = Setup_Graph(
            self.name, self.linestyleopts, self.g, self.layer_sizes, self.node_name
        )

        # print('nodes:{}'.format(self.config.graph.nodes))
        config = {"emphasis_linestyleopts": self.config.linestyleopts[0]}
        c = draw.graph_contracted_signed(config, self.config.graph.nodes)


        # DEMO USED FOR IJCAI
        from vnegmas.backend.api.data import Faker
        factories = []
        for layer in self.node_name[1:-1]:
            factories +=layer
        print(f"factories is {factories}")
        self.factories = factories
        self.products = Faker.products
        self.total_step = Faker.total_step

        # Product Demo
        p =self. _get_bar_product_produce(self.products, factories, Faker.get_product_factories_produce(factories=factories))
        # Activation level Demo
        a_l = self._activation_level(self.total_step, factories, Faker.get_activations_level(factories=factories))

        # Buy and Sell Demo
        b_a_s = self._get_buyer_seller(factories, self.products, Faker.get_buy_and_sell_data(factories=factories))

        # TODO Breach

        # TODO Negotiation

        content = {"graph": c.dump_options(), "product": p, "activation_level":a_l, "buy_and_sell":b_a_s, "breach":[], "negotiations":[]}
        print(f"Graph content is {content}") 
        return json.dumps(content)

    def _graph_with_opts_dyn(self):
        def send_result(contracts=None):
            g = negmas_draw.negmas_add_edges(
                self.config.graph,
                self.config.layer_sizes,
                node_name=self.config.node_name,
                contracts=contracts,
            )
            edges = [(edge[0], edge[1]) for edge in g.edges]
            links = [opts.GraphLink(source=edge[0], target=edge[1]) for edge in edges]
            result = []
            for link in links:
                result.append(
                    {"source": link.opts["source"], "target": link.opts["target"]}
                )
            return result

        if hasattr(self, "check_init_graph") and self.check_init_graph:
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
        if not hasattr(self, "configSetUp"):
            self._init_configSetup()
        return self.configSetUp.get_my_config

    def _get_system_config(self) -> dict:
        if not hasattr(self, "configSetUp"):
            self._init_configSetup()
        return self.configSetUp.get_system_config


async def vnegmas():
    vnegmas = VNegmas(name="VNegmas")
    vnegmas.run()
    await asyncio.sleep(100)
    vnegmas.stop()
    print("Finish vnegmas task!")

if __name__ == "__main__":
    start = time.time()
    tasks = [vnegmas(), watch_fs('../log_folder')]
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait(tasks))
    finally:
        loop.close()
    # table_base().render()
    print("finished all tasks! time %.5f" % float(time.time()-start))
