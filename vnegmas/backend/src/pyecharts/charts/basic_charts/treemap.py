from ... import options as opts
from ...charts.chart import Chart
from ...commons.types import Numeric, Optional, Sequence, Union
from ...globals import ChartType


class TreeMap(Chart):
    """
    <<< TreeMap >>>

    TreeMap are a common visual representation of "hierarchical data" and "tree data".
    It mainly uses area to highlight the important nodes in the hierarchy of "tree".
    """

    def __init__(self, init_opts: opts.InitOpts = opts.InitOpts()):
        super().__init__(init_opts=init_opts)

    def add(
        self,
        series_name: str,
        data: Sequence[Union[opts.TreeItem, dict]],
        *,
        is_selected: bool = True,
        leaf_depth: Optional[Numeric] = None,
        pos_left: Optional[str] = None,
        pos_right: Optional[str] = None,
        pos_top: Optional[str] = None,
        pos_bottom: Optional[str] = None,
        drilldown_icon: str = "▶",
        visual_min: Optional[Numeric] = None,
        visual_max: Optional[Numeric] = None,
        label_opts: Union[opts.LabelOpts, dict] = opts.LabelOpts(),
        tooltip_opts: Union[opts.TooltipOpts, dict, None] = None,
        itemstyle_opts: Union[opts.ItemStyleOpts, dict, None] = None,
    ):
        self._append_legend(series_name, is_selected)
        self.options.get("series").append(
            {
                "type": ChartType.TREEMAP,
                "name": series_name,
                "data": data,
                "left": pos_left,
                "right": pos_right,
                "top": pos_top,
                "bottom": pos_bottom,
                "label": label_opts,
                "leafDepth": leaf_depth,
                "drillDownIcon": drilldown_icon,
                "visualMin": visual_min,
                "visualMax": visual_max,
                "tooltip": tooltip_opts,
                "itemStyle": itemstyle_opts,
            }
        )
        return self
