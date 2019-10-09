import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import dash_table

"""
    Used for layout the page，
    different page need to design a different layout, extract  and save the same module as separate.
    Separate the different parts and finally combine them
"""
# left up button group compose of four buttons,  Run New, Run From Checkpoint, Tournament, Setting
_left_up_button_group = dbc.Row(
                                [
                                    dcc.Link(dbc.Button("Run New", id="run_new", outline=True, color="secondary", className="mr-1"), href="/run_new"),
                                    dcc.Link(dbc.Button("Run From Checkpoint", outline=True, color="secondary", className="mr-1"), href="/checkpoint"),
                                    dcc.Link(dbc.Button("Tournament", outline=True, color="secondary", className="mr-1"), href="/tournament"),
                                    dcc.Link(dbc.Button("Setting", outline=True, color="secondary", className="mr-1"), href="/setting"),
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
_left_middle_group_load = html.Div(

)

_left_middle_group_run_from_checkpoint = None
_left_middle_group_runnable_component = None
_left_middle_group_not_runnable_component = None

# left bottom group
# right up group
_right_up_group_runnable_component = dbc.Row(                         
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
                                ])
# right middle group
_right_middle_group_runnable_component = [
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
# right bottom group
df = pd.DataFrame(
    {
        'Parameter Name':['Checkpoint Every', 'Checkpoint Path', 'Agents'],
        'Value': [3, '~/negmas/checkpoints/3402jisdfsfd', 'ABC, ZXY']
    }
)
table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
table_dash_table = dash_table.DataTable(
        id='load_config',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'scroll'},
    )

_right_bottom_group_load = dbc.Row(
        table
)

layout_run_new = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                                [
                                    html.Br(),
                                    _left_up_button_group,
                                    html.Br(),
                                    _left_middle_group_run_new,
                                ],
                            width={"size": 4, "offset": 1}
                            ),
                    ],
                ),
            ]
        )


layout_load = html.Div([
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Br(),
                    _left_up_button_group,
                    html.Br(),
                    _left_middle_group_load,
                ],
                width={"size":4, "offset":1}
            ),
            dbc.Col(
                [
                    html.Br(),
                    _right_bottom_group_load,
                    dbc.Button("Run", outline=True, color="secondary", className="btn-block"),
                ],

            ),
        ]
    )
])

layout_run_from_checkpoint = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.Br(),
                    _left_up_button_group,
                    html.Br(),
                    _left_middle_group_run_from_checkpoint,
                ]
            )
        ])
    ]
)

layout_runnable = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                                [
                                    html.Br(),
                                    _left_up_button_group,
                                    html.Br(),
                                    _left_middle_group_run_new,
                                ],
                            width={"size": 4, "offset": 1}
                            ),
                        dbc.Col(
                            [
                                html.Br(),
                                _right_up_group_runnable_component,

                            ] + _right_middle_group_runnable_component
                        )
                    ],
                ),
            ]
        )

layout_not_runnable = None