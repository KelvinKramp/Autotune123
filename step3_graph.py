from dash import html
from dash import dcc
from app.app import app
import dash_bootstrap_components as dbc

step3_graph = html.Div([
    html.Div(id='graph'),
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
            dcc.Markdown(
                'The dropdown list shows [Savitzky-Golay filters](https://www.delftstack.com/howto/python/smooth-data-in-python/#use-the-numpy-convolve-method-to-smooth-data-in-python) '
                'with different parameters. The filter is used to smooth the OpenAPS Autotune results. Flattening the curve like this will lead to basal rate recommendations that are more closely aligned with physiological values.'
                ' As Gary Scheiner [writes](https://diatribe.org/rules-engagement-basal-insulin-adjustment-or-avoiding-basal-blunders): "When setting up a 24-hour basal program, our objective is to mimic normal physiology as closely as '
                'possible."  '
            ),
            dcc.Markdown(
                'The primary cause of the biological circadian rhythm in insulin needs is cortisol. Cortisol is a stress hormone that decreases insulin sensitivity.'
                ' Cortisol levels are highest in the morning when waking up and lowest in '
                ' [late in the evening to the night](https://www.psychologyinaction.org/psychology-in-action-1/2020/6/11/diurnal-patterns-of-cortisol). '
                'The variation in sensitivity can lead to unexpectedly high glucose levels, especially in the morning.'
                ' '
            ),
            dcc.Markdown(
                'The resulting curve after applying the filter should preferably display one peak and one valley in insulin levels. You can find examples of how a curve should look per age range in [this picture](https://www.google.com/url?sa=i&url=https%3A%2F%2Fdiatribe.org%2Frules-engagement-basal-insulin-adjustment-or-avoiding-basal-blunders&psig=AOvVaw1PKkYKJnVsuPQL-q1E45gq&ust=1644599934138000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCNDM0KnS9fUCFQAAAAAdAAAAABAD). '
                'A basal profile that has multiple peaks and valleys is often incorrect or '
                'compensating for some other aspect of the insulin administration that is [not set up properly](https://diatribe.org/rules-engagement-basal-insulin-adjustment-or-avoiding-basal-blunders).'
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
    app.layout = step3_graph
    app.run_server(host='0.0.0.0', port=8000, debug=True, use_reloader=True)