from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from app.app import app
from dash.dependencies import Input, Output, State
from dash import dcc
from autotune import Autotune
from step2 import step2
from step3_graph import step3_graph
from get_recommendations import get_recommendations
from get_filtered_data import get_filtered_data
import plotly.graph_objs as go
from create_graph import create_graph
from adjust_table import adjust_table
from styles import table_style, cell_style, header_style

# VARIABLES
development = True
dropdown_value_old = "No filter"
autotune = Autotune()
df = pd.DataFrame()
params = [
    'Weight', 'Torque', 'Width', 'Height',
    'Efficiency', 'Power', 'Displacement'
]


# LAYOUT
layout = html.Div([
    html.Img(src=app.get_asset_url("header.png"), style={'width':'100%'}),
    dbc.Row(children=[html.Div(" .",id="step-0")]),
    html.H3("", id='title', style={'textAlign': 'center',}),
    html.H4("", id='subtitle', style={'textAlign': 'center'}),
    html.Br(),
    dbc.Row([
    html.Div(children=[
        # STEP 1
        ################################################################################################################
        html.Div(id="step-1", hidden=False, children=[
        dbc.Row([
            dcc.Input(
                id="input-url", type="url", placeholder="NightScout URL", required=True, style={'marginBottom': '1.5em', 'text-align': 'center'},
            ),
            html.Br(),
            html.Br(),
            dcc.Input(
                id="token", type="password", placeholder="API secret", required=False, style={'text-align': 'center'},
            ),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '40%'}, className='justify-content-center'),
        html.Div("(Only required if the NightScout url is locked)",style={'text-align': 'center'}
                 ),
        html.Br(),
        dbc.Row([
            dbc.Button('Load profile', id='load-profile', n_clicks=0),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '30%'}, className='justify-content-center'),
        html.Br(),
        ]),
        ################################################################################################################


        # STEP 2
        ################################################################################################################
        html.Div(id="step-2", hidden=False, children=[
            step2
        ]),
        ################################################################################################################


        # STEP 3
        ################################################################################################################
        html.Div(id="step-3", hidden=False, children=[
        dbc.Row([
            html.H5("3A: Apply filter to smooth of calculated recommendations (optional)"),
            dbc.Row(children=[html.Div(children=step3_graph)
            ]
            ),
            html.Br(),
            html.Hr(),
            html.H5("3B: Review and adjust recommendations (optional)"),
            html.H6("Always check whether the recommendations make sense based on your personal experience and "
                    "knowledge about what is acceptable."),
            dbc.Row(children=[html.Div(children=[
                dash_table.DataTable(
                    id='title-table-recommendations',
                    columns=[{"name": i, "id": i} for i in ["Time", "Current", "Autotune", "Days Missing"]],
                    data=[],
                    style_table=table_style,
                    # style cell
                    style_cell=cell_style,
                    # style header
                    style_header=header_style,
                    editable=False,
                ),

                dash_table.DataTable(
                    id='table-recommendations',
                    columns=[],
                    data=[],
                    style_table=table_style,
                    # style cell
                    style_cell=cell_style,
                    # style header
                    style_header={'display':'none'},
                    editable=True,
                ),
                html.Div("* Scroll through the table to see all values. "
                         "* You can change the values by double clicking on the table cells, adjusting the value and pressing enter."
                         ),
                dbc.Row([
                    html.Div([
                        dbc.Alert(
                            id="alert-auto-autotune",
                            is_open=False,
                            duration=2000,
                            color="success",
                            style={'textAlign': 'center', }
                        ),
                    ],
                        style={"width": "50%", 'justify-content': 'center'}
                    ), ],
                    justify='center'),
                        ]
                    ),]),
        ]),
        html.Br(),
        html.Hr(),
        dbc.Row([
            html.H5("3C: Upload to NightScout:"),
            dcc.Markdown("Enter your API secret and click the upload button. API secrets are not saved anywhere, only in your browser "
                         "if you use a password manager. If you don't want to use this website for uploading recommendations, you can "
                         "download the code from [Github](https://github.com/KelvinKramp/AutotuneAPI) and run it locally on your computer."
                         ),
            dcc.Markdown(
                "After uploading you need to activate the uploaded profile on your phone."
                ),
        ]),
        dbc.Row([
            dcc.Input(
                id="input-API-secret", type="password", placeholder="Nightscout API secret",style={'text-align': 'center'},
            ),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '40%'}, className='justify-content-center'),
        html.Br(),
        dbc.Row([
            dbc.Button('Upload', id='activate-profile', n_clicks=0),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '30%'}, className='justify-content-center'),
        ]),
        ################################################################################################################
    html.Br(),
    dbc.Alert(id="result-alert",
              color="success",
              dismissable=True,
              fade=False,
              is_open=False,
              ),
    ],
        style={"width": "70%", 'justify-content': 'center'}
    ),],
        justify='center'),
    # html.Br(),
    # html.Br(),
    # html.Br(),
    # html.Br(),
    # html.Br(),
    dbc.Row([
        # dbc.Col([
        # html.Div("Documentation"),
        # ], width={"size": 2, "order": 1, "offset": 0},
        # ),
        dbc.Col([
            dcc.Link("What is Autotune?",
                     href="https://openaps.readthedocs.io/en/latest/docs/Customize-Iterate/autotune.html",
                     target="_blank",
                     style={'color': 'darkgrey'}),
        ],width={"size": 2, "order": 2, "offset": 0},
        ),
        dbc.Col([
            dcc.Link("What is Autotune123?",
                     href="https://github.com/KelvinKramp/Autotune123",
                     target="_blank",
                     style={'color': 'darkgrey'}),
        ], width={"size": 2, "order": 3, "offset": 0},
        ),
        dbc.Col([
            dcc.Link("What is NightScout?",
                     href="https://nightscout.github.io/",
                     target="_blank",
                     style={'color': 'darkgrey'}),
        ], width={"size": 2, "order": 3, "offset": 0},
        ),
        dbc.Col([
            dcc.Link("How to get glucose data from the Freestyle libre 2 to Nightscout ",
                     href="https://towardsdatascience.com/how-to-hack-a-glucose-sensor-ebaaf2238170",
                     target="_blank",
                     style={'color': 'darkgrey'}),
        ], width={"size": 2, "order": 3, "offset": 0},
        ),
    ], style={
            'position' : 'absolute',
            'bottom' : '0',
            'text-align':'center',
            # 'height' : '40px',
            # 'margin-top' : '40px',
            'margin-bottom' : '20px',
            'width':'100%',
            }, className='justify-content-center',
    ),
    html.Div(id="empty-div-autotune"),
    dcc.Loading(
        id="loading-1",
        type="default",
        fullscreen=True,
        color='#2c3e50',
        children=[
            html.Div(id='empty-div2-autotune'),
        ]
    )
    ])


# AUTOTUNE CALLBACKS
@app.callback(
    Output('table-current-non-basals', 'columns'),
    Output('table-current-non-basals', 'data'),
    Output('table-current-basals', 'columns'),
    Output('table-current-basals', 'data'),
    Output('step-1', 'hidden'),
    Output('step-2', 'hidden'),
    Output('step-3', 'hidden'),
    Output('table-recommendations', 'columns'),
    Output('table-recommendations', 'data'),
    Output('subtitle', 'children'),
    Output("graph", "children"),
    [Input('load-profile', 'n_clicks'),
    Input('run-autotune', 'n_clicks'),
    Input("dropdown", "value")],
    State('input-url', 'value'),
    State('token', 'value'),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date'),
)
def load_profile(load, run_autotune, dropdown_value, NS_HOST, start_date, end_date, token):
    global dropdown_value_old
    print("startdate", start_date)
    print("enddate", end_date)
    # IF CHANGE OF FILTER REFRESH GRAPH AND TABLE
    if dropdown_value != dropdown_value_old:
        dropdown_value_old = dropdown_value
        df_recommendations = get_recommendations()
        x, y1, y2 = get_filtered_data(df_recommendations, dropdown_value)
        graph = create_graph(x, y1, y2)
        start_row_index = 4
        df_recommendations = adjust_table(df_recommendations,[y1,y2],["Pump","Autotune"],start_row_index)
        return [], [], [], [], False, False, False, [{"name": i, "id": i} for i in df_recommendations.columns], \
               df_recommendations.to_dict('records'), "Step 3: Review and upload", html.Div(children=[graph])

    # RUN AUTOTUNE
    if run_autotune and start_date and end_date and NS_HOST and autotune.url_validator(NS_HOST):
        if not development:
            autotune.run(NS_HOST, start_date, end_date)
        df_recommendations = get_recommendations()
        x, y1, y2 = get_filtered_data(df_recommendations, dropdown_value)
        graph = create_graph(x, y1, y2)
        # adjust_table()

        return [], [], [], [], True, True, False, [{"name": i, "id": i} for i in df_recommendations.columns], \
               df_recommendations.to_dict('records'), "Step 3: Review and upload", html.Div(children=[graph])
    else:
        df = pd.DataFrame()

    # GET PROFILE
    if load>0:
        df_basals, df_non_basals, _ = autotune.get(NS_HOST, token)
        return  [{"name": i, "id": i} for i in df_non_basals.columns], df_non_basals.to_dict('records'), \
                [{"name": i, "id": i} for i in df_basals.columns], df_basals.to_dict('records'),\
                True, False, True,[], [], "Step 2: Pick time period", html.Div(children=[])
    else:
        return [],[],[],[], False, True, True,[{"name": i, "id": i} for i in df.columns], df.to_dict('records'), \
               "Step 1: Get your current profile", html.Div(children=[])

# UPLOAD PROFILE
@app.callback(
    Output('result-alert','children'),
    Output('result-alert', 'is_open'),
    [Input('activate-profile', 'n_clicks')],
    State('input-url', 'value'),
    State('input-API-secret', 'value'),
    State('table-recommendations', 'data'),
    State('result-alert','is_open')
)
def activate_profile(click, NS_HOST, API_SECRET, json_data, is_open):
    if click and NS_HOST and API_SECRET and json_data:
        _, _, profile = autotune.get(NS_HOST)
        new_profile = autotune.create_adjusted_profile(json_data, profile)
        if not development:
            result = autotune.upload(NS_HOST, new_profile, API_SECRET)
        else:
            result = True
        if result:
            return "New profile activated. Check your profile over 15 min. to see if the activation was successful." \
                   'The new profile is visible under the name "OpenAPS Autosync"', \
                   not is_open
        else:
            return "Profile activation was unsuccessful. You can try to [run the script on your computer](https://openaps.readthedocs.io/en/latest/docs/Customize-Iterate/autotune.html)" \
                   " or [report a bug](k.h.kramp@gmail.com).", not is_open
    else:
        return "", is_open

@app.callback(
    Output("info", "is_open"),
    [Input("more-info", "n_clicks")],
    [State("info", "is_open")],
)
def toggle_alert_no_fade(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.layout = layout
    app.run_server(host='0.0.0.0', port=8000, debug=True, use_reloader=True)