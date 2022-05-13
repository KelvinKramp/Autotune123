from dash import html
from dash import dcc
import dash_bootstrap_components as dbc


# links
link1 = html.A("Savitzky-Golay filters", href='https://www.delftstack.com/howto/python/smooth-data-in-python/#use-the-numpy-convolve-method-to-smooth-data-in-python', target="_blank")
link2 = html.A("writes", href='https://diatribe.org/rules-engagement-basal-insulin-adjustment-or-avoiding-basal-blunders', target="_blank")
link3 = html.A("late in the evening to the night", href='https://www.psychologyinaction.org/psychology-in-action-1/2020/6/11/diurnal-patterns-of-cortisol', target="_blank")
link4 = html.A(" in this picture", href='https://diatribe.org/sites/default/files/images/tab-5.JPG', target="_blank")
link5 = html.A(" not set up properly", href='https://diatribe.org/rules-engagement-basal-insulin-adjustment-or-avoiding-basal-blunders', target="_blank")

step3_graph = html.Div([
    html.Div(id='graph'),
    html.Div(id="total_amounts",
             ),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(
                html.Div("Select a filter:"),
                width={"size": 2, "order": 1, "offset": 0},
                style={"textAlign":"right"},
            ),
            dbc.Col(
                dcc.Dropdown(
                    ['No filter', 'Savitzky-Golay 11.6', "Savitzky-Golay 17.5", "Savitzky-Golay 23.3"],
                    'No filter',
                    placeholder="Choose a filter",
                    id="dropdown",
                    clearable=False
                ),
                width={"size": 3, "order": 2, "offset": 0},
            ),
            dbc.Col(
                dbc.Button(
                    "More info about the filters", id="more-info", n_clicks=0
                ),
                width={"size": 3, "order": 3, "offset": 4},
            )
        ]
    ),
    html.Br(),
    dbc.Alert(
        html.Div(children=[
            html.Div([
                'The dropdown list shows ',link1,
                ' with different parameters. The filter is used to smooth the OpenAPS Autotune results. Flattening the curve like this will lead to basal rate recommendations that are more closely aligned with physiological values.'
                ' As Gary Scheiner ',link2, ': "When setting up a 24-hour basal program, our objective is to mimic normal physiology as closely as '
                'possible."  '
                ]
            ),
            html.Br(),
            html.Div(children=[
                'The primary cause of the biological circadian rhythm in insulin needs is cortisol. Cortisol is a stress hormone that decreases insulin sensitivity.'
                ' Cortisol levels are highest in the morning when waking up and lowest ', link3,
                '. This variation in sensitivity can lead to unexpectedly high glucose levels, especially in the morning.'
                ]
            ),
            html.Br(),
            html.Div(children=[
                'The resulting curve after applying the filter should preferably display one peak and one valley in insulin levels. You can find examples of how a curve should look per age range in', link4,
                '. A basal profile that has multiple peaks and valleys is often incorrect or compensating for some other aspect of the insulin administration that is', link5,'.'
                ]
            ),
            ]),
        id="info",
        color="light",
        dismissable=True,
        fade=False,
        is_open=False,
    ),
    html.Br()
    ])



if __name__ == '__main__':
    from main import app
    app.layout = step3_graph
    app.run_server()