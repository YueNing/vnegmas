from dash.dependencies import Input, Output
from app import dash_app

@dash_app.callback(
    Output('progress', 'value'),
    [ Input("interval", "n_intervals")]
)
def update_progress(n):
    """
        used for test the progress
    """
    return min(n%100, 100)

