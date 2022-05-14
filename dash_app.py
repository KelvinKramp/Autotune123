import dash
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dcc
from autotune import Autotune
from layout.step2 import step2
from layout.step3_graph import step3_graph
from data_processing.table_calculations import sum_column
from layout.styles import table_style, cell_style, header_style
import os
from dateutil.parser import parse
from datetime import timedelta
from data_processing.data_preperation import data_preperation
from datetime import datetime as dt
from definitions import development, assets_path, github_link
from log import logging
# VARIABLES

autotune = Autotune()
df = pd.DataFrame()


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
        dbc.NavbarSimple(
            children=[
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Autotune123", id="about", href="#"),
                        dbc.DropdownMenuItem("Savitzky-Golay filter", id="info-savgol_filter", href="#"),
                        dbc.DropdownMenuItem("About me", href="https://www.kelvinkramp.com/",  target="_blank"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label="About",
                ),
                dbc.NavItem(dbc.NavLink("Report an issue", href="https://github.com/KelvinKramp/Autotune123/issues", target="_blank")),
                # dbc.NavItem(dbc.NavLink("About", id='about', n_clicks=0)),
                dbc.NavItem(dbc.NavLink("GitHub", href="https://github.com/KelvinKramp/Autotune123", target="_blank")),
            ],
            brand="Autotune123",
            brand_href="http://autotune123.com/",
            color="primary",
            dark=True,
            sticky="top",
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
                    html.Div(
                        [
                            dbc.Label("Insulin type"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "Rapid Acting (Humalog/Novolog/Novorapid) 1", "value": "rapid-acting"},
                                    {"label": "Ultra Rapid (Fiasp)", "value": "ultra-rapid"},
                                ],
                                value="rapid-acting",
                                id="radioitems-insulin",
                            ),
                        ],
                        style={'text-align': 'center', 'margin': 'auto', 'width': '40%'}, className='justify-content-center'),
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
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(""),
                                        width={"size": 8, "offset": 0},
                                    ),
                                    dbc.Col(
                                        [
                                        dbc.Button("Download CSV", id="btn_csv"),
                                        dcc.Download(id="download-dataframe-csv"),
                                        ],
                                        width={"size": "auto", "offset": 0},
                                    ),
                                    dbc.Col(
                                        [
                                        dbc.Button("Download Excel", id="btn_xlsx"),
                                        dcc.Download(id="download-dataframe-xlsx"),
                                        ],
                                        width={"size": "auto", "offset": 0},
                                    ),
                                ]
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
                        ), ]),
                    ]),
                    html.Br(),
                    html.Hr(),
                    dbc.Row([
                        html.H5("3C: Upload to NightScout:"),
                        html.Div(children=[
                            "Enter your API secret and click the activate button. The API secret is not saved on the server. "
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
        dbc.Modal(
            [
                dbc.ModalBody(
                    dcc.Markdown("""
                #### What is Autotune?
                Autotune is a tool to help calculate potential adjustments to ISF, carb ratio, and basal rates.
                \n\n
                "Autotune is a work in progress tool. Do not blindly make changes to your pump settings without careful 
                consideration. You may want to print the output of this tool and discuss any particular changes with your 
                care team. Make note that you probably do not want to make long-term changes based on short term (i.e. 24 hour) data. 
                Most people will choose to make long term changes after reviewing carefully autotune output of 3-4 weeks 
                worth of data." \n
                [Open APS - Understanding Autotune page](https://openaps.readthedocs.io/en/latest/docs/Customize-Iterate/understanding-autotune.html)

                #### What is Autotune123?
                Autotune123 is a web application for type 1 diabetics to configure their insuline pump basal rate
                in three steps. It relies on the open source OpenAPS Autotune algorithm, the Savitzky-Golay filter, and uses
                 data from a personal NightScout websites as input to propose a 24-hour basal curve.\n\n

                Autotune123 only works if:
                - You have a NightScout account properly setup.
                - You have logged your carbs accurately in amount and time.
                - You digitally disconnect your pump when your pump is physically disconnected (e.g. during showering or blockage of infusion set).
                
                The profile activation in step 3 only works if (in preferences->NS settings -> synchronisation): 
                - "Upload data to nightscout" is turned on.
                - "Receive profile store" is turned on.
                - "Receive profile switches" is turned on.
                """)),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            size="xl",  # "sm", "lg", "xl" = small, large or extra large
            backdrop=True,  # Modal to not be closed by clicking on backdrop
            scrollable=True,  # Scrollable in case of large amount of text
            centered=True,  # Vertically center modal
            keyboard=True,  # Close modal when escape is pressed
            fade=True,  # True, False
            # style={"max-width": "none", "width": "50%",}
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
         Input("radioitems-insulin", "value"),
         Input("dropdown", "value"),
         Input('table-recommendations', 'data'),
         ],
        State("checklist", "value"),
        State('input-url', 'value'),
        State('date-picker-range', 'start_date'),
        State('date-picker-range', 'end_date'),
        State('token', 'value'),
    )
    def load_profile(load, run_autotune, insulin_type, dropdown_value, table_data, checklist_value, NS_HOST, start_date, end_date, token):
        # identify the trigger of the callback and define as interaction_id
        ctx = dash.callback_context
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
        # if interactino id = button increase or decrease
        # use state of % and time to increase values
        # df_recommendations, graph, y1_sum_graph, y2_sum_graph = data_preperation(dropdown_value, dropdown_value2 = .. , time= .. , percentage = ...)

        if interaction_id == "dropdown":
            df_recommendations, graph, y1_sum_graph, y2_sum_graph = data_preperation(dropdown_value)
            text_under_graph = "* Total amount insulin currently {}. Total amount based on autotune with filter {}. {}".format(
                y1_sum_graph, y2_sum_graph, extra_text),
            text_under_table = text_under_graph
            return [], [], [], [], True, True, False, [{"name": i, "id": i} for i in df_recommendations.columns], \
                   df_recommendations.to_dict('records'), "Step 3: Review and upload", html.Div(children=[graph]), \
                   text_under_graph, text_under_table

        # STEP 3b: IF CHANGE IN TABLE REFRESH GRAPH AND TABLE
        if interaction_id == "table-recommendations":
            df_recommendations, graph, y1_sum_graph, y2_sum_graph = data_preperation(dropdown_value)
            text_under_graph = "* Total amount insulin currently {}. Total amount based on autotune with filter {}. {}".format(
                y1_sum_graph, y2_sum_graph, extra_text),
            y1_sum_table = sum_column(table_data, "Pump")
            y2_sum_table = sum_column(table_data, "Autotune")
            text_under_table = "* Total amount insulin currently {}. Total amount based on autotune with filter and changes in table {}. {}".format(
                round(y1_sum_table, 2), round(y2_sum_table, 2), extra_text),
            # convert user adjusted table into new recommendations pandas dataframe
            df_recommendations = pd.DataFrame(table_data)
            return [], [], [], [], True, True, False, [{"name": i, "id": i} for i in df_recommendations.columns], \
                   df_recommendations.to_dict('records'), "Step 3: Review and upload", html.Div(children=[graph]), \
                   text_under_graph, text_under_table

        # STEP 2: RUN AUTOTUNE
        if run_autotune and start_date and end_date and NS_HOST and autotune.url_validator(NS_HOST):
            autotune.run(NS_HOST, start_date, end_date, uam)
            df_recommendations, graph, y1_sum_graph, y2_sum_graph = data_preperation(dropdown_value)
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
            df_basals, df_non_basals, _ = autotune.get(NS_HOST, token, insulin_type)
            return [{"name": i, "id": i} for i in df_non_basals.columns], df_non_basals.to_dict('records'), \
                   [{"name": i, "id": i} for i in df_basals.columns], df_basals.to_dict('records'), \
                   True, False, True, [], [], "Step 2: Pick time period", html.Div(children=[]), "", ""
        else:
            return [], [], [], [], False, True, True, [{"name": i, "id": i} for i in df.columns], df.to_dict('records'), \
                   "Step 1: Get your current profile", html.Div(children=[]), "", ""

    # STEP 3C
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
                return "New profile activated. Check your phone in a couple of 5-30 minutes to see if the activation was successful. " \
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
        Output("modal", "is_open"),
        [Input("about", "n_clicks"), Input("close", "n_clicks")],
        [State("modal", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open

    @app.callback(
        Output("download-dataframe-csv", "data"),
        Input("btn_csv", "n_clicks"),
        State('table-recommendations', 'data'),
        prevent_initial_call=True,
    )
    def download_csv(n_clicks, table_data):
        datetime_string = dt.now().strftime("(%d-%m-%Y-%H-%S)")
        df = pd.DataFrame(table_data)
        return dcc.send_data_frame(df.to_csv, "AutoRec"+datetime_string+".csv")

    @app.callback(
        Output("download-dataframe-xlsx", "data"),
        Input("btn_xlsx", "n_clicks"),
        State('table-recommendations', 'data'),
        prevent_initial_call=True,
    )
    def download_excel(n_clicks, table_data):
        datetime_string = dt.now().strftime("(%d-%m-%Y-%H-%S)")
        df = pd.DataFrame(table_data)
        return dcc.send_data_frame(df.to_excel, "AutoRec"+datetime_string+".csv", sheet_name=datetime_string)

    @app.callback(
        Output("info", "is_open"),
        [Input("more-info", "n_clicks"),
         Input("info-savgol_filter", "n_clicks"),
         Input("close-savgol_filter", "n_clicks"),
         ],
        [State("info", "is_open")],
    )
    def toggle_alert_no_fade(n1, n2, close, is_open):
        if n1 or n2 or close:
            return not is_open
        return is_open

    return app.server


