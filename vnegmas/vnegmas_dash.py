import dash
import dash_bootstrap_components as dbc
import dash_html_components as html 
import dash_core_components as dcc

class VNegmasDash(object):
    
    """
        VNegmas based on dash to design a new interactive web application
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self._layout()
        

    def _layout(self):
        
        """
            Used for layout the page
        """
        # global app
        self.app.layout = html.Div(
            dbc.Row(
                [
                    dbc.Col(
                            [
                                dbc.Row(
                                        [
                                            dbc.Button("Run New", outline=True, color="secondary", className="mr-1"),
                                            dbc.Button("Run From Checkpoint", outline=True, color="secondary", className="mr-1"),
                                            dbc.Button("Tournament", outline=True, color="secondary", className="mr-1"),
                                            dbc.Button("Setting", outline=True, color="secondary", className="mr-1"),
                                    ],
                                ),
                                html.Br(),
                                html.Div(
                                    [
                                        dbc.Row(
                                            dbc.Col(
                                                [
                                                dbc.DropdownMenu(
                                                    label="Component Type",

                                                    children=
                                                        [
                                                                dbc.DropdownMenuItem("SAOMechanism"),
                                                                dbc.DropdownMenuItem("SCMLWorld"),
                                                                dbc.DropdownMenuItem("etc"),
                                                                html.P(
                                                                    "You can select component type here.",
                                                                    className="text-muted px-4 mt-4",
                                                                ),
                                                            ],
                                                        bs_size="lg",
                                                        className="mb-3",
                                                        right=False,
                                                    ),
                                                ],
                                            )
                                        ),
                                        html.Br(),
                                        dbc.Row(
                                            dbc.Col(
                                                [   
                                                        dbc.InputGroup(
                                                            [
                                                                dbc.Input(placeholder="Configuration File Path"),
                                                                dbc.Button("load"),
                                                            ]
                                                        ),
                                                ],
                                                width='auto',
                                            )
                                        ),
                                    ]
                                )
                            ],
                        width={"size": 4, "offset": 1}
                        ),
                    dbc.Col()
                ],
            )
       )

if __name__ == "__main__":
    vnegmas_dash = VNegmasDash()
    vnegmas_dash.app.run_server(debug=True)