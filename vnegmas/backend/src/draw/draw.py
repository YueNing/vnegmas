from networkx import DiGraph

from vnegmas.backend.src.pyecharts import options as opts
from vnegmas.backend.src.pyecharts.charts import Bar, Bar3D, Graph, Grid, Line, Liquid, Page
from vnegmas.backend.src.pyecharts.commons.utils import JsCode


def _graph_contracted_signed(config: dict = None, nodes: DiGraph = None) -> Graph:
    nodes_show = [
        opts.GraphNode(
            name=node,
            x=nodes[node]["pos"][0],
            y=nodes[node]["pos"][1],
            symbol_size=10,
            category="level_" + str(nodes[node]["color"]),
        )
        for node in nodes
    ]

    links = []

    def _get_categories():
        try:
            _categories = {nodes[node]["color"] for node in nodes}
            categories = [
                opts.GraphCategory(name="level_" + str(category))
                for category in _categories
            ]
        except:
            categories = [
                opts.GraphCategory(name="c_" + str(index))
                for index in range(len(nodes))
            ]
        finally:
            return categories

    print(_get_categories())
    c = (
        Graph()
        .add(
            "",
            nodes_show,
            links,
            _get_categories(),
            edge_symbol=["", "arrow"],
            edge_symbol_size=10,
            layout=config["layout"] if "layout" in config else "none",
            repulsion=4000,
            emphasis_itemstyle_opts=config["emphasis_linestyleopts"]
            if "emphasis_linestyleopts" in config
            else None,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=config["title"] if "title" in config else ""
            ),
            legend_opts=opts.LegendOpts(
                orient="vertical", type_="scroll", pos_left="right"
            ),
        )
    )
    return c


def _liquid_process() -> Liquid:
    c = (
        Liquid()
        .add(
            "lq", [0.0, 0.0], label_opts=opts.LabelOpts(font_size=12, position="inside")
        )
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
    )
    return c


def _bar_product_produce(products, factories, data, config: dict = None) -> Bar:
    b = Bar().add_xaxis(products)
    for index, f in enumerate(factories):
        b = b.add_yaxis(f, data[index], stack="stack1")
    c = (
        b.set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            legend_opts=opts.LegendOpts(
                orient="vertical", type_="scroll", pos_left="right"
            ),
        )
    )
    return c


def _bar3d_agent_activation(steps, factories, data) -> Bar3D:
    import random
    from ..pyecharts import options as opts
    from ..pyecharts.charts import Bar3D

    c = (
        Bar3D()
        .add(
            "",
            [[d[1], d[0], d[2]] for d in data],
            xaxis3d_opts=opts.Axis3DOpts(steps, type_="category"),
            yaxis3d_opts=opts.Axis3DOpts(factories, type_="category"),
            zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=20),
            title_opts=opts.TitleOpts(title=""),
        )
    )
    return c

def _grid_buyer_seller(factories, products, data) -> Grid:
    c: Grid = None
    b = Bar().add_xaxis(factories) 
    for index, p in enumerate(products):
        b = b.add_yaxis(p, data['buyer'][index], stack="buyer")
        b = b.add_yaxis(p, data['seller'][index], stack="seller")
    
    bar = (
        b
    )
    buyer_volume = []
    seller_volume = []
    for index, f in enumerate(factories):
        _buyer_volume = 0
        for p in data['buyer']:
            _buyer_volume += p[index]
        buyer_volume.append(_buyer_volume)

    for index, f in enumerate(factories):
        _seller_volume = 0
        for p in data['seller']:
            _seller_volume += p[index]
        seller_volume.append(_seller_volume)    
        
    line = (
        Line()
        .add_xaxis(
            factories
        )
        .add_yaxis(
            "Buyer Volume",
            buyer_volume,
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
        .add_yaxis(
            "Seller Volume",
            seller_volume,
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
    )
    bar.overlap(line)
    return bar

def _get_specific_type_chart(data, type):
    if type == 'line':
        c = (
            Line()
            .add_xaxis(data['xaxis_data'])
            .add_yaxis("", data["yaxis_data"], label_opts=opts.LabelOpts(is_show=False))
        )
    return c

class VNemgasCharts:
    """
        ..versionadd: v0.2.1
        Used For Register and Unregister for all charts that can be used in VNEGMAS COME FROM NEGMAS STATS
        The Details, please see the config file, root path, settings, parameter: DEFAULT_CHARTS
    """
    
if __name__ == "__main__":
    c = _liquid_process()
    c.render()
