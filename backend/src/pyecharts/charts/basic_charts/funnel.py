from ... import options as opts
from ...charts.chart import Chart
from ...commons.types import Numeric, Optional, Sequence, Union
from ...globals import ChartType


class Funnel(Chart):
    """
    <<< Funnel >>>

    Funnel diagram is suitable for one-way analysis of single process
    with standardized business process, long cycle and multiple links.
    Through comparison of business data of each link in the funnel,
    the link where the potential problems can be found intuitively,
    and then decisions can be made.
    """

    def __init__(self, init_opts: opts.InitOpts = opts.InitOpts()):
        super().__init__(init_opts=init_opts)

    def add(
        self,
        series_name: str,
        data_pair: Sequence,
        *,
        is_selected: bool = True,
        color: Optional[str] = None,
        sort_: str = "descending",
        gap: Numeric = 0,
        label_opts: Union[opts.LabelOpts, dict] = opts.LabelOpts(),
        tooltip_opts: Union[opts.TooltipOpts, dict, None] = None,
        itemstyle_opts: Union[opts.ItemStyleOpts, dict, None] = None,
    ):
        self._append_color(color)
        data = [{"name": n, "value": v} for n, v in data_pair]
        for a, _ in data_pair:
            self._append_legend(a, is_selected)

        _dset = set(self.options.get("legend")[0].get("data"))
        self.options.get("legend")[0].update(data=list(_dset))

        self.options.get("series").append(
            {
                "type": ChartType.FUNNEL,
                "name": series_name,
                "data": data,
                "sort": sort_,
                "gap": gap,
                "label": label_opts,
                "tooltip": tooltip_opts,
                "itemStyle": itemstyle_opts,
            }
        )
        return self
