import os
import sys

from vnegmas.backend.src.draw import (_bar3d_agent_activation, _bar_product_produce,
                         _graph_contracted_signed, _grid_buyer_seller,
                         _liquid_process)
from vnegmas.backend.src.pyecharts.charts import Bar3D, Graph, Grid, Liquid, Page


def graph_contracted_signed(config: dict = None, nodes: list = None) -> Graph:
    c = _graph_contracted_signed(config, nodes)
    return c


def liquid_process():
    c = _liquid_process()
    return c


def bar3d_agent_activation():
    c = _bar3d_agent_activation()
    return c


def bar_product_produce():
    c: Bar = _bar_product_produce()
    return c


def grid_buyer_seller():
    c: Grid = _grid_buyer_seller()
    return c
