from pyecharts.charts import Graph, Page, Liquid, Bar3D, Grid
from pyecharts import options as opts

def _graph_contracted_signed(config:dict=None, nodes:list=None) -> Graph:
    nodes_show = [opts.GraphNode(name=node, 
            x=nodes[node]['pos'][0], 
            y=nodes[node]['pos'][1], 
            symbol_size=10, category='level_'+str(nodes[node]['color']))
            for node in nodes]
    
    links = []
    def _get_categories():
        try:
            _categories ={nodes[node]['color'] for node in nodes}
            categories = [opts.GraphCategory(name='level_'+str(category)) for category in _categories]
        except:
            categories = [
                opts.GraphCategory(name='c_'+ str(index)) for index in range(len(nodes))
            ]
        finally:
            return categories
    print(_get_categories())
    c = (
        Graph()
        .add("", nodes_show, links, _get_categories(), edge_symbol=['', 'arrow'], edge_symbol_size=10,
                    layout=config['layout'] if 'layout' in config else 'none', repulsion=4000,
                        emphasis_itemstyle_opts=config['emphasis_linestyleopts'] 
                            if 'emphasis_linestyleopts' in config else None
            )
        .set_global_opts(title_opts=opts.TitleOpts(title=config['title'] if 'title' in config else ""))
    )
    return c

def _liquid_process() -> Liquid:
    c = (
        Liquid()
        .add("lq", [0.0, 0.0])
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
    )
    return c

def _bar3d_agent_activation() -> Bar3D:
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

def _grid_breach_contract_balance() -> Grid:
    c: Grid = None
    return c