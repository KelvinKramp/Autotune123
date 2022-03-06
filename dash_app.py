import dash
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
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
import os
from dateutil.parser import parse
from datetime import timedelta

# VARIABLES
development = False
dropdown_value_old = "No filter"
autotune = Autotune()
df = pd.DataFrame()
params = [
    'Weight', 'Torque', 'Width', 'Height',
    'Efficiency', 'Power', 'Displacement'
]
assets_path = os.getcwd() + '/assets'
github_link = html.A("GitHub", href='https://github.com/KelvinKramp/Autotune123', target="_blank", style={'color': 'black'})


def init_dashboard(server):
    # START APP
    app = dash.Dash(__name__,
                    assets_folder=assets_path,
                    title="Autotune123",
                    suppress_callback_exceptions=True,
                    # external_stylesheets=[dbc.themes.FLATLY]
                    )

    # LAYOUT
    app.layout = html.Div([
        dbc.Navbar(
            html.A(
            html.Img(src=app.get_asset_url("header.png"), height="100px"),
                href="https://www.autotune123.com",
                style={"textDecoration": "none"},
            ),
            # dbc.Container(
            #     [
            #         html.A(
            #             # Use row and col to control vertical alignment of logo / brand
            #             dbc.Row(
            #                 [
            #                     dbc.Col(html.Img(src=app.get_asset_url("header.png"), height="60px")),
            #                     # dbc.Col(dbc.NavbarBrand("Configure your basals in three steps", className="ms-3")),
            #                 ],
            #                 align="center",
            #                 className="g-0",
            #             ),
            #             href="https://plotly.com",
            #             style={"textDecoration": "none"},
            #         ),
            #         # dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            #     ]
            # ),
            color="primary",
            dark=True,
            style={'textAlign':"center"},
            className='justify-content-center',
        ),

        dbc.Row(children=[html.Div(" .", id="step-0")]),
        html.H3("", id='title', style={'textAlign': 'center', }),
        html.H4("", id='subtitle', style={'textAlign': 'center'}),
        html.Br(),
        dcc.Loading(
            id="loading-1",
            fullscreen=True,
            type="circle",
            color="#2c3e50",
            style={'backgroundColor': 'transparent',
                   # 'height': '50%',
                   # 'width': '50%',
                   'text-align': 'center',
                   'margin': 'auto',
                   'justify-content':'center'
                   },
            children=
        dbc.Row([
            html.Div(children=[
                # STEP 1
                ################################################################################################################
                html.Div(id="step-1", hidden=False, children=[
                    dbc.Row([
                        dcc.Input(
                            id="input-url", type="url", placeholder="NightScout URL", required=True,
                            style={'marginBottom': '1.5em', 'text-align': 'center'},
                        ),
                        html.Br(),
                        html.Br(),
                        dcc.Input(
                            id="token", type="password", placeholder="API secret", required=False,
                            style={'text-align': 'center'},
                        ),
                    ], style={'text-align': 'center', 'margin': 'auto', 'width': '40%'},
                        className='justify-content-center'),
                    html.Div("(Only required if the NightScout url is locked)", style={'text-align': 'center'}
                             ),
                    html.Br(),
                    dbc.Row([
                        dbc.Button('Load profile', id='load-profile', n_clicks=0),
                    ], style={'text-align': 'center', 'margin': 'auto', 'width': '30%'},
                        className='justify-content-center'),
                    html.Br(),
                ]),
                ################################################################################################################

                # STEP 2
                ################################################################################################################
                html.Div(id="step-2", hidden=False, children=[
                    step2]),
                ################################################################################################################

                # STEP 3
                ################################################################################################################
                dbc.Row(children=[
                    html.Div(id="step-3", hidden=False, children=[
                    dbc.Row([
                        html.H5("3A: Apply filter to smooth calculated recommendations (optional)"),
                        dbc.Row(children=[html.Div(children=step3_graph),]),
                        html.Br(),
                        html.Hr(),
                        html.H5("3B: Review and adjust recommendations (optional)"),
                        html.H6(
                            "Always check whether the recommendations make sense based on your personal experience and "
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
                                style_header={'display': 'none'},
                                editable=True,
                            ),
                            html.Div("* The Autotune column is adjusted based on the filter selected in 3A. Scroll through the table to review all values. "),
                            html.Div("* If a correction is needed, double click on the table cells to adjust an Autotune recommendation value and press enter."),
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
                        ), ]),
                    ]),
                    html.Br(),
                    html.Hr(),
                    dbc.Row([
                        html.H5("3C: Upload to NightScout:"),
                        html.Div(children=[
                            "Enter your API secret and click the activate button. API secrets and NightScout URLs are not saved in Autotune123. "
                            "They might be saved in your browser autocomplete or password manager if you have one. If you don't want to use this website for activating recommendations, you can "
                            "download the code from ",github_link," and run it locally on your computer."
                            ]
                            ),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dcc.Input(
                            id="input-API-secret", type="password", placeholder="Nightscout API secret",
                            style={'text-align': 'center'},
                        ),
                    ], style={'text-align': 'center', 'margin': 'auto', 'width': '40%'},
                        className='justify-content-center'),
                    html.Br(),
                    dbc.Row([
                        dbc.Button('Activate', id='activate-profile', n_clicks=0, disabled=False),
                    ], style={'text-align': 'center', 'margin': 'auto', 'width': '30%'},
                        className='justify-content-center'),
                ]),]),
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
            ), ],
            justify='center'),),
        dbc.Row([
            dbc.Col([
                dcc.Link("What is Autotune123?",
                         href="https://github.com/KelvinKramp/Autotune123",
                         target="_blank",
                         style={'color': '#2c3e50'}),
            ], width={"size": 2, "order": 3, "offset": 0},
            ),
            dbc.Col([
                dcc.Link("What is Autotune?",
                         href="https://openaps.readthedocs.io/en/latest/docs/Customize-Iterate/autotune.html",
                         target="_blank",
                         style={'color': '#2c3e50'}),
            ], width={"size": 2, "order": 2, "offset": 0},
            ),
            dbc.Col([
                dcc.Link("What is NightScout?",
                         href="https://nightscout.github.io/",
                         target="_blank",
                         style={'color': '#2c3e50'}),
            ], width={"size": 2, "order": 3, "offset": 0},
            ),
            dbc.Col([
                dcc.Link("How to get glucose data from the Freestyle libre 2 to Nightscout",
                         href="https://towardsdatascience.com/how-to-hack-a-glucose-sensor-ebaaf2238170",
                         target="_blank",
                         style={'color': '#2c3e50'}),
            ], width={"size": 2, "order": 3, "offset": 0},
            ),
            dbc.Col([
                dcc.Link("Open source MIT license",
                         href="https://github.com/KelvinKramp/Autotune123/blob/master/LICENSE.txt",
                         target="_blank",
                         style={'color': '#2c3e50'}),
            ], width={"size": 2, "order": 3, "offset": 0},
            ),
        ], style={
            'position': 'relative',
            'bottom': '0',
            'text-align': 'center',
            # 'height' : '40px',
            # 'margin-top' : '40px',
            'margin-bottom': '20px',
            'width': '100%',
        }, className='justify-content-center',
        ),
        html.Div(id="empty-div-autotune"),
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
        Output("total_amounts", "children"),
        [Input('load-profile', 'n_clicks'),
         Input('run-autotune', 'n_clicks'),
         Input("dropdown", "value"),
         ],
        State("checklist", "value"),
        State('input-url', 'value'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        State('token', 'value'),
    )
    def load_profile(load, run_autotune, dropdown_value, checklist_value, NS_HOST, start_date, end_date, token):
        global dropdown_value_old
        if checklist_value == 1:
            uam = True
        else:
            uam = False
        # some extra code to prevent bug in callback when dash runs on AWS ubuntu VM
        if token == None:
            token = ""

        # check if dateperiod is not > 14 days
        diff = (parse(end_date) - parse(start_date))
        if diff.days > 14:
            start_date = (parse(end_date) - timedelta(days=14)).date().strftime("%Y-%m-%d")
            extra_text = "A date period > 14 days was chosen. To avoid excessive calculation time the Autotune input" \
                         " was restricted to input from ({} until {}).".format(parse(start_date).strftime("%d-%m-%Y"),
                                                                               parse(end_date).strftime("%d-%m-%Y"))
        else:
            extra_text = ""
        # IF CHANGE OF FILTER REFRESH GRAPH AND TABLE
        if dropdown_value != dropdown_value_old:
            dropdown_value_old = dropdown_value
            df_recommendations = get_recommendations()
            x, y1, y2 = get_filtered_data(df_recommendations, dropdown_value)
            graph = create_graph(x, y1, y2)
            y1_sum = round(sum([x for x in y1 if str(x) != 'nan']), 2)
            y2_sum = round(sum([x for x in y2 if str(x) != 'nan']), 2)
            start_row_index = 4
            df_recommendations = adjust_table(df_recommendations, [y1, y2], ["Pump", "Autotune"], start_row_index)
            return [], [], [], [], True, True, False, [{"name": i, "id": i} for i in df_recommendations.columns], \
                   df_recommendations.to_dict('records'), "Step 3: Review and upload", html.Div(children=[graph]), \
                   "* Total amount insulin currently {}. Total amount based on autotune with filter {}. {}".format(
                       y1_sum, y2_sum, extra_text)

        # RUN AUTOTUNE
        if run_autotune and start_date and end_date and NS_HOST and autotune.url_validator(NS_HOST):
            if not development:
                autotune.run(NS_HOST, start_date, end_date, uam)
            df_recommendations = get_recommendations()
            x, y1, y2 = get_filtered_data(df_recommendations, dropdown_value)
            graph = create_graph(x, y1, y2)
            y1_sum = round(sum([x for x in y1 if str(x) != 'nan']), 2)
            y2_sum = round(sum([x for x in y2 if str(x) != 'nan']), 2)
            # adjust_table()
            return [], [], [], [], True, True, False, [{"name": i, "id": i} for i in df_recommendations.columns], \
                   df_recommendations.to_dict('records'), "Step 3: Review and upload", html.Div(children=[graph]), \
                   "* Total amount insulin currently {}. Total amount based on autotune with filter {}. {}".format(
                       y1_sum, y2_sum, extra_text)
        else:
            df = pd.DataFrame()

        # GET PROFILE
        if load > 0:
            df_basals, df_non_basals, _ = autotune.get(NS_HOST, token)
            return [{"name": i, "id": i} for i in df_non_basals.columns], df_non_basals.to_dict('records'), \
                   [{"name": i, "id": i} for i in df_basals.columns], df_basals.to_dict('records'), \
                   True, False, True, [], [], "Step 2: Pick time period", html.Div(children=[]), ""
        else:
            return [], [], [], [], False, True, True, [{"name": i, "id": i} for i in df.columns], df.to_dict('records'), \
                   "Step 1: Get your current profile", html.Div(children=[]), ""

    # UPLOAD PROFILE
    @app.callback(
        Output('result-alert', 'children'),
        Output('result-alert', 'is_open'),
        Output('activate-profile', 'disabled'),
        [Input('activate-profile', 'n_clicks')],
        State('input-url', 'value'),
        State('input-API-secret', 'value'),
        State('table-recommendations', 'data'),
        State('result-alert', 'is_open'),
    )
    def activate_profile(click, NS_HOST, token, json_data, is_open):
        if click and NS_HOST and token and json_data:
            _, _, profile = autotune.get(NS_HOST, token)
            new_profile = autotune.create_adjusted_profile(json_data, profile)
            if not development:
                result = autotune.upload(NS_HOST, new_profile, token)
            else:
                result = True
            if result:
                return "New profile activated. Check your phone to see if the activation was successful." \
                       'The new profile should be visible under the name "OpenAPS Autosync".', \
                       not is_open, True
            else:
                return "Profile activation was unsuccessful. You can try to [run the Autotune script on your computer](https://openaps.readthedocs.io/en/latest/docs/Customize-Iterate/autotune.html)" \
                       " and/or [report an issue](https://github.com/KelvinKramp/Autotune123/issues).", not is_open, True
        else:
            return "", is_open, False

    @app.callback(
        Output("info", "is_open"),
        [Input("more-info", "n_clicks")],
        [State("info", "is_open")],
    )
    def toggle_alert_no_fade(n, is_open):
        if n:
            return not is_open
        return is_open

    return app.server
