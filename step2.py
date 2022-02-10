from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import dcc
from datetime import date
from datetime import datetime as dt
from datetime import timedelta
from styles import table_style, cell_style, header_style

step2 = html.Div(children=[
    html.Br(),
    dbc.Row([
        html.Div([
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=date(2000, 8, 5),
                max_date_allowed=dt.now().date(),
                initial_visible_month=dt.now().date(),
                display_format='D-M-Y',
                start_date=(dt.now() - timedelta(7)).date(),
                end_date=dt.now().date(),
                # end_date=dt.now().date()
            ),
        ], style={'text-align': 'center', 'margin': 'auto', 'width': '70%'}, className='justify-content-center'),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Button('Run autotune', id='run-autotune', n_clicks=0),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '30%'}, className='justify-content-center'),
    html.Br(),
    html.Hr(),
    html.Br(),
    dbc.Row([
        html.H4("Current NightScout profile"),
    ], style={'text-align': 'center', 'margin': 'auto', 'width': '100%'}, className='justify-content-center'),
    html.Br(),
    dash_table.DataTable(
            id='table-current-non-basals',
            columns=[],
            data=[],
            style_table=table_style,
            # style cell
            style_cell=cell_style,
            # style header
            style_header=header_style,
            editable=False,
            ),
            html.Br(),
            dash_table.DataTable(
                id='title-table-current-basals',
                columns=[{"name": i, "id": i} for i in ["Start time", "Unit/hour"]],
                data=[],
                style_table=table_style,
                # style cell
                style_cell=cell_style,
                # style header
                style_header=header_style,
                editable=False,
            ),
            dash_table.DataTable(
                id='table-current-basals',
                columns=[],
                data=[],
                style_table=table_style,
                # style cell
                style_cell=cell_style,
                # style header
                style_header={'display':'none'},
                editable=False,
            ),
        html.Div("* Scroll through the table to see all values."),
        html.Div("* The timestamps that did not have a basal rate "
                 "where autocompleted with the basal rate of the previous timestamp."),
        html.Br(),
    ])