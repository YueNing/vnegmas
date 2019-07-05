from networkx import DiGraph

from ..pyecharts import options as opts
from ..pyecharts.charts import Bar, Bar3D, Graph, Grid, Line, Liquid, Page
from ..pyecharts.commons.utils import JsCode


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


def _bar_product_produce(config: dict = None) -> Bar:
    c = (
        Bar()
        .add_xaxis(
            [
                "Product 1",
                "Product 2",
                "Product 3",
                "Product 4",
                "Product 5",
                "Product 6",
            ]
        )
        .add_yaxis("Factory 1", [10, 10, 10, 10, 50, 10], stack="stack1")
        .add_yaxis("Factory 2", [10, 10, 10, 100, 100, 10], stack="stack1")
        .add_yaxis("Factory 3", [100, 10, 10, 10, 50, 10], stack="stack1")
        .add_yaxis("Factory 4", [10, 10, 100, 10, 50, 10], stack="stack1")
        .add_yaxis("Factory 5", [10, 100, 10, 10, 50, 10], stack="stack1")
        .add_yaxis("Factory 6", [10, 10, 10, 10, 50, 10], stack="stack1")
        .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            legend_opts=opts.LegendOpts(
                orient="vertical", type_="scroll", pos_left="right"
            ),
        )
    )
    return c


def _bar3d_agent_activation() -> Bar3D:
    import random
    from ..pyecharts import options as opts
    from ..pyecharts.charts import Bar3D

    step = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24".split()
    factories = (
        "factory_1 factory_2 factory_3 factory_4 factory_5 factory_6 factory_7".split()
    )
    data = [(i, j, random.randint(0, 12)) for i in range(7) for j in range(24)]
    c = (
        Bar3D()
        .add(
            "",
            [[d[1], d[0], d[2]] for d in data],
            xaxis3d_opts=opts.Axis3DOpts(step, type_="category"),
            yaxis3d_opts=opts.Axis3DOpts(factories, type_="category"),
            zaxis3d_opts=opts.Axis3DOpts(type_="value"),
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=20),
            title_opts=opts.TitleOpts(title=""),
        )
    )
    return c


def _grid_buyer_seller() -> Grid:
    c: Grid = None
    bar = (
        Bar()
        .add_xaxis(
            [
                "Factory 1",
                "Factory 2",
                "Factory 3",
                "Factory 4",
                "Factory 5",
                "Factory 6",
            ]
        )
        .add_yaxis("product 1", [10, 100, 10, 10, 50, 10], stack="buyer")
        .add_yaxis("product 2", [10, 100, 10, 10, 50, 10], stack="buyer")
        .add_yaxis("product 3", [10, 100, 10, 10, 50, 10], stack="buyer")
        .add_yaxis("product 4", [10, 100, 10, 10, 50, 10], stack="buyer")
        .add_yaxis("product 1", [10, 10, 10, 10, 50, 10], stack="seller")
        .add_yaxis("product 2", [10, 10, 10, 10, 50, 10], stack="seller")
        .add_yaxis("product 3", [10, 10, 10, 10, 50, 10], stack="seller")
        .add_yaxis("product 4", [10, 10, 10, 10, 50, 10], stack="seller")
    )
    line = (
        Line()
        .add_xaxis(
            [
                "Factory 1",
                "Factory 2",
                "Factory 3",
                "Factory 4",
                "Factory 5",
                "Factory 6",
            ]
        )
        .add_yaxis(
            "Buyer Volume",
            [10 * 4, 100 * 4, 10 * 4, 10 * 4, 50 * 4, 10 * 4],
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
        .add_yaxis(
            "Seller Volume",
            [10 * 4, 10 * 4, 10 * 4, 10 * 4, 50 * 4, 10 * 4],
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
    )
    # c = (
    #     Grid()
    #     .add(buyer, grid_opts=opts.GridOpts(pos_left="55%"))
    #     .add(seller, grid_opts=opts.GridOpts(pos_right="55%"))
    # )
    bar.overlap(line)
    return bar


if __name__ == "__main__":
    c = _liquid_process()
    c.render()
