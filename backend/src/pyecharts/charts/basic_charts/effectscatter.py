from ... import options as opts
from ...charts.chart import RectChart
from ...commons.types import Numeric, Optional, Sequence, Union
from ...globals import ChartType


class EffectScatter(RectChart):
    """
    <<< Scatter plots with ripple effects animation >>>

    Use animation effects to visually highlight designated data set.
    """

    def __init__(self, init_opts: opts.InitOpts = opts.InitOpts()):
        super().__init__(init_opts=init_opts)

    def add_yaxis(
        self,
        series_name: str,
        y_axis: Sequence,
        *,
        is_selected: bool = True,
        xaxis_index: Optional[Numeric] = None,
        yaxis_index: Optional[Numeric] = None,
        color: Optional[str] = None,
        symbol: Optional[str] = None,
        symbol_size: Numeric = 10,
        label_opts: Union[opts.LabelOpts, dict] = opts.LabelOpts(),
        effect_opts: Union[opts.EffectOpts, dict] = opts.EffectOpts(),
        tooltip_opts: Union[opts.TooltipOpts, dict, None] = None,
        itemstyle_opts: Union[opts.ItemStyleOpts, dict, None] = None,
    ):
        self._append_color(color)
        self._append_legend(series_name, is_selected)
        self.options.get("series").append(
            {
                "type": ChartType.EFFECT_SCATTER,
                "name": series_name,
                "xAxisIndex": xaxis_index,
                "yAxisIndex": yaxis_index,
                "showEffectOn": "render",
                "rippleEffect": effect_opts,
                "symbol": symbol,
                "symbolSize": symbol_size,
                "data": [list(z) for z in zip(self._xaxis_data, y_axis)],
                "label": label_opts,
                "tooltip": tooltip_opts,
                "itemStyle": itemstyle_opts,
            }
        )
        return self
