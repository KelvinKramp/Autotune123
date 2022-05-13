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
from table_calculations import adjust_table, sum_column
from styles import table_style, cell_style, header_style
import os
from dateutil.parser import parse
from datetime import timedelta

# VARIABLES
development = False
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
                    # assets_folder=assets_path,
                    title="Autotune123",
                    suppress_callback_exceptions=True,
                    external_stylesheets=[dbc.themes.FLATLY]
                    )

    # LAYOUT
    app.layout = html.Div([
        dbc.Navbar(
            # html.A(
            # html.Img(src=app.get_asset_url("header.png"), height="100px"),
            #     href="https://www.autotune123.com",
            #     style={"textDecoration": "none"},
            # ),  # used to have this header, but later thought it as ugly
            html.H2("Autotune 123", style={'color':'white'}),
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
                            "Scroll through the table to review all values. The Autotune column is automatically adjusted based on the filter selected in 3A. "
                            "Always check whether the recommendations make sense based on your personal experience. "
                            "If a correction is needed, double click on the table cells to adjust an Autotune recommendation value and press enter."),
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
                            html.Div(id="total_amounts_2"),
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
        dbc.Row([
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
            dbc.Col([
                dcc.Link("About me",
                         href="https://www.kelvinkramp.com",
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
        Output("total_amounts_2", "children"),
        [Input('load-profile', 'n_clicks'),
         Input('run-autotune', 'n_clicks'),
         Input("dropdown", "value"),
         Input('table-recommendations', 'data'),
         ],
        State("checklist", "value"),
        State('input-url', 'value'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        State('token', 'value'),
    )
    def load_profile(load, run_autotune, dropdown_value, table_data, checklist_value, NS_HOST, start_date, end_date, token):
        # identify the trigger of the callback and define as ctx
        ctx = dash.callback_context
        # print(ctx.triggered)
        interaction_id = ctx.triggered[0]['prop_id'].split('.')[0]
        # check uam checkbox
        if checklist_value == 1:
            uam = True
        else:
            uam = False
        # some extra code to prevent bug in callback when dash runs on AWS ubuntu VM
        if token == None:
            token = ""
        # check if dateperiod is not > 14 days to prevent server overload
        diff = (parse(end_date) - parse(start_date))
        if diff.days > 14:
            start_date = (parse(end_date) - timedelta(days=14)).date().strftime("%Y-%m-%d")
            extra_text = "A date period > 14 days was chosen. To avoid excessive calculation time the Autotune input" \
                         " was restricted to input from ({} until {}).".format(parse(start_date).strftime("%d-%m-%Y"),
                                                                               parse(end_date).strftime("%d-%m-%Y"))
        else:
            extra_text = ""

        # STEP 3a: IF CHANGE OF FILTER REFRESH GRAPH AND TABLE
        if interaction_id == "dropdown":
            # convert Autotune recommendationns file into pd df
            df_recommendations = get_recommendations()
            # get the lists x, y1 and y2 from the pd df based on dropdown value
            x, y1, y2 = get_filtered_data(df_recommendations, dropdown_value)
            # create graph from lists
            graph = create_graph(x, y1, y2)
            # replace the pump and autotune column with y1 and y2 from the start_row_index
            df_recommendations = adjust_table(df_recommendations, [y1, y2], ["Pump", "Autotune"],
                                              4)  # 4 is startrowindex for changing of df
            # calculate totals
            y1_sum_graph = round((sum([x for x in y1 if str(x) != 'nan'])), 2)
            y2_sum_graph = round(sum([x for x in y2 if str(x) != 'nan']), 2)
            # create sentence for under the graph
            text_under_graph = "* Total amount insulin currently {}. Total amount based on autotune with filter {}. {}".format(
                y1_sum_graph, y2_sum_graph, extra_text),
            # create sentence for under the table
            text_under_table = text_under_graph
            return [], [], [], [], True, True, False, [{"name": i, "id": i} for i in df_recommendations.columns], \
                   df_recommendations.to_dict('records'), "Step 3: Review and upload", html.Div(children=[graph]), \
                   text_under_graph, text_under_table

        # STEP 3b: IF CHANGE IN TABLE REFRESH GRAPH AND TABLE
        if interaction_id == "table-recommendations":
            # convert Autotune recommendationns file into pd df
            df_recommendations = get_recommendations()
            # get the lists x, y1 and y2 from the pd df based on dropdown value
            x, y1, y2 = get_filtered_data(df_recommendations, dropdown_value)
            # create graph from lists
            graph = create_graph(x, y1, y2)
            # replace the pump and autotune column with y1 and y2 from the start_row_index
            df_recommendations = adjust_table(df_recommendations, [y1, y2], ["Pump", "Autotune"],
                                              4)  # 4 is startrowindex for changing of df
            # calculate totals
            y1_sum_graph = round((sum([x for x in y1 if str(x) != 'nan'])), 2)
            y2_sum_graph = round(sum([x for x in y2 if str(x) != 'nan']), 2)
            # create sentence for under graph
            text_under_graph = "* Total amount insulin currently {}. Total amount based on autotune with filter {}. {}".format(
                y1_sum_graph, y2_sum_graph, extra_text),
            # sum the data from the adjustable table
            y1_sum_table = sum_column(table_data, "Pump")
            y2_sum_table = sum_column(table_data, "Autotune")
            # create sentence for under the table
            text_under_table = "* Total amount insulin currently {}. Total amount based on autotune with filter and changes in table {}. {}".format(
                round(y1_sum_table, 2), round(y2_sum_table, 2), extra_text),
            # convert adjusted table into new recommendations pandas dataframe
            df_recommendations = pd.DataFrame(table_data)
            return [], [], [], [], True, True, False, [{"name": i, "id": i} for i in df_recommendations.columns], \
                   df_recommendations.to_dict('records'), "Step 3: Review and upload", html.Div(children=[graph]), \
                   text_under_graph, text_under_table

        # STEP 2: RUN AUTOTUNE
        if run_autotune and start_date and end_date and NS_HOST and autotune.url_validator(NS_HOST):
            if not development:
                autotune.run(NS_HOST, start_date, end_date, uam)
            # convert Autotune recommendationns file into pd df
            df_recommendations = get_recommendations()
            # get the lists x, y1 and y2 from the pd df based on dropdown value
            x, y1, y2 = get_filtered_data(df_recommendations, dropdown_value)
            # create graph from lists
            graph = create_graph(x, y1, y2)
            # replace the pump and autotune column with y1 and y2 from the start_row_index
            df_recommendations = adjust_table(df_recommendations, [y1, y2], ["Pump", "Autotune"],
                                              4)  # 4 is startrowindex for changing of df
            # calculate totals
            y1_sum_graph = round((sum([x for x in y1 if str(x) != 'nan'])), 2)
            y2_sum_graph = round(sum([x for x in y2 if str(x) != 'nan']), 2)
            # create sentence for under graph
            text_under_graph = "* Total amount insulin currently {}. Total amount based on autotune with filter {}. {}".format(
                y1_sum_graph, y2_sum_graph, extra_text),
            text_under_table = text_under_graph
            return [], [], [], [], True, True, False, [{"name": i, "id": i} for i in df_recommendations.columns], \
                   df_recommendations.to_dict('records'), "Step 3: Review and upload", html.Div(children=[graph]), \
                   text_under_graph, text_under_table
        else:
            df = pd.DataFrame()

        # STEP 1: GET PROFILE
        if interaction_id == "load-profile":
            df_basals, df_non_basals, _ = autotune.get(NS_HOST, token)
            return [{"name": i, "id": i} for i in df_non_basals.columns], df_non_basals.to_dict('records'), \
                   [{"name": i, "id": i} for i in df_basals.columns], df_basals.to_dict('records'), \
                   True, False, True, [], [], "Step 2: Pick time period", html.Div(children=[]), "", ""
        else:
            return [], [], [], [], False, True, True, [{"name": i, "id": i} for i in df.columns], df.to_dict('records'), \
                   "Step 1: Get your current profile", html.Div(children=[]), "", ""

    #STEP 3C
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
                return "New profile activated. Check your phone in a couple of minutes to see if the activation was successful." \
                       'The new profile should be visible under the name "OpenAPS Autosync".', \
                       not is_open, True
            else:
                return "Profile activation was unsuccessful:" \
                       "- Check your API secret.\n" \
                       "- You can try to [run the Autotune script on your computer](https://openaps.readthedocs.io/en/latest/docs/Customize-Iterate/autotune.html).\n" \
                       "- And/or [report an issue](https://github.com/KelvinKramp/Autotune123/issues).", not is_open, True
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
