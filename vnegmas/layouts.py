import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

"""
    Used for layout the page，
    different page need to design a different layout, extract  and save the same module as separate.
    Separate the different parts and finally combine them
"""
# left up button group compose of four buttons,  Run New, Run From Checkpoint, Tournament, Setting
_left_up_button_group = dbc.Row(
                                [
                                    dbc.Button("Run New", outline=True, color="secondary", className="mr-1"),
                                    dbc.Button("Run From Checkpoint", outline=True, color="secondary", className="mr-1"),
                                    dbc.Button("Tournament", outline=True, color="secondary", className="mr-1"),
                                    dbc.Button("Setting", outline=True, color="secondary", className="mr-1"),
                            ],
                    
)
# left middle group , has different version of every page, run new page, 
# load page , run from checkpoints, runnable component and not-runnable component
_left_middle_group_run_new = html.Div(
                            [
                                dbc.Row(
                                    dbc.Col(
                                        [
                                        dcc.Dropdown(
                                            options=[
                                                {'label': 'SAOMechanism','value':'SAOM'},
                                                {'label':'SCMLWorld', 'value':'SCMLW'},
                                                {'label':'etc', 'value':'ETC'},
                                                {'label':'You can select component type here.', 'value':'INFO', 'disabled': True},

                                            ],
                                            value='SAOM',
                                            clearable=False,
                                        ),
                                        ],
                                        width='9'
                                    )
                                ),
                                html.Br(),
                                dbc.Row(
                                    dbc.Col(
                                        [   
                                                dcc.Upload(
                                                        id='upload-data',
                                                        children=html.Div([
                                                            'Drag and Drop or ',
                                                            html.A('Select Configuration Files')
                                                        ]),
                                                        style={
                                                            'width': '70%',
                                                            'height': '60px',
                                                            'lineHeight': '60px',
                                                            'borderWidth': '1px',
                                                            'borderStyle': 'dashed',
                                                            'borderRadius': '5px',
                                                            'textAlign': 'center',
                                                            'margin': '10px'
                                                        },
                                                        # Allow multiple files to be uploaded
                                                        multiple=True
                                                    ),
                                                    html.Div(id='output-data-upload'),
                                        ],
                                        # width='auto',
                                    )
                                ),
                            ]
                        )
_left_middle_group_load = None
_left_middle_group_run_from_checkpoint = None
_left_middle_group_runnable_component = None
_left_middle_group_not_runnable_component = None

# left bottom group
# right up group
# right bottom group
run_new = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                                [
                                    html.Br(),
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
                                                    dcc.Dropdown(
                                                        options=[
                                                            {'label': 'SAOMechanism','value':'SAOM'},
                                                            {'label':'SCMLWorld', 'value':'SCMLW'},
                                                            {'label':'etc', 'value':'ETC'},
                                                            {'label':'You can select component type here.', 'value':'INFO', 'disabled': True},

                                                        ],
                                                        value='SAOM',
                                                        clearable=False,
                                                    ),
                                                    ],
                                                    width='9'
                                                )
                                            ),
                                            html.Br(),
                                            dbc.Row(
                                                dbc.Col(
                                                    [   
                                                            dcc.Upload(
                                                                    id='upload-data',
                                                                    children=html.Div([
                                                                        'Drag and Drop or ',
                                                                        html.A('Select Configuration Files')
                                                                    ]),
                                                                    style={
                                                                        'width': '70%',
                                                                        'height': '60px',
                                                                        'lineHeight': '60px',
                                                                        'borderWidth': '1px',
                                                                        'borderStyle': 'dashed',
                                                                        'borderRadius': '5px',
                                                                        'textAlign': 'center',
                                                                        'margin': '10px'
                                                                    },
                                                                    # Allow multiple files to be uploaded
                                                                    multiple=True
                                                                ),
                                                                html.Div(id='output-data-upload'),
                                                    ],
                                                    # width='auto',
                                                )
                                            ),
                                        ]
                                    )
                                ],
                            width={"size": 4, "offset": 1}
                            ),
                        dbc.Col(
                            [
                                html.Br(),
                                dbc.Row(
                                    
                                    [
                                    dbc.Col(
                                        [
                                            dbc.Progress(id="progress", value=0, striped=True, animated=True),
                                            dcc.Interval(id="interval", interval=250, n_intervals=0),
                                            html.I(id="step_backward", n_clicks=0, className='fa fa-step-backward fa-lg'),
                                            html.I(id="play", n_clicks=0, className='fa fa-play'),
                                            html.I(id="step_forward", n_clicks=0, className='fa fa-step-forward')
                                        ]
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Button('test'),
                                        ]
                                    ),
                                ]),
                                html.Br(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=go.Figure(
                                                    data = [
                                                                go.Bar(
                                                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                                                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                                                    350, 430, 474, 526, 488, 537, 500, 439],
                                                                    name='Rest of world',
                                                                    marker=go.bar.Marker(
                                                                        color='rgb(55, 83, 109)'
                                                                    )
                                                                ),
                                                    ],
                                                    layout=go.Layout(
                                                        title='US Export of Plastic Scrap',
                                                        showlegend=True,
                                                        legend=go.layout.Legend(
                                                            x=0,
                                                            y=1.0
                                                        ),
                                                        margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                                                ),

                                                ),
                                                style={'height': 300},
                                                id='my-graph'
                                            )
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=go.Figure(
                                                    data = [
                                                                go.Bar(
                                                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                                                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                                                    350, 430, 474, 526, 488, 537, 500, 439],
                                                                    name='Rest of world',
                                                                    marker=go.bar.Marker(
                                                                        color='rgb(55, 83, 109)'
                                                                    )
                                                                ),
                                                    ],
                                                    layout=go.Layout(
                                                        title='US Export of Plastic Scrap',
                                                        showlegend=True,
                                                        legend=go.layout.Legend(
                                                            x=0,
                                                            y=1.0
                                                        ),
                                                        margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                                                ),

                                                ),
                                                style={'height': 300},
                                                id='my-graph2'
                                            )
                                        ),
                                    ]
                                ),
                                html.Br(),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=go.Figure(
                                                    data = [
                                                                go.Bar(
                                                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                                                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                                                    350, 430, 474, 526, 488, 537, 500, 439],
                                                                    name='Rest of world',
                                                                    marker=go.bar.Marker(
                                                                        color='rgb(55, 83, 109)'
                                                                    )
                                                                ),
                                                    ],
                                                    layout=go.Layout(
                                                        title='US Export of Plastic Scrap',
                                                        showlegend=True,
                                                        legend=go.layout.Legend(
                                                            x=0,
                                                            y=1.0
                                                        ),
                                                        margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                                                ),

                                                ),
                                                style={'height': 300},
                                                id='my-graph3'
                                            )
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=go.Figure(
                                                    data = [
                                                                go.Bar(
                                                                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                                                                    2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                                                                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                                                    350, 430, 474, 526, 488, 537, 500, 439],
                                                                    name='Rest of world',
                                                                    marker=go.bar.Marker(
                                                                        color='rgb(55, 83, 109)'
                                                                    )
                                                                ),
                                                    ],
                                                    layout=go.Layout(
                                                        title='US Export of Plastic Scrap',
                                                        showlegend=True,
                                                        legend=go.layout.Legend(
                                                            x=0,
                                                            y=1.0
                                                        ),
                                                        margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                                                ),

                                                ),
                                                style={'height': 300},
                                                id='my-graph4'
                                            )
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ],
                ),
            ]
        )