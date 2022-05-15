from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from definitions import text_links

link1, link2, link3, link4, link5 = text_links


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
    dbc.Modal(
        [
        dbc.ModalBody(children=[
            html.H4("The Savitzky-Golay filter"),
            html.Div([
                'As Gary Scheiner ',link2, ': "When setting up a 24-hour basal program, our objective is to mimic normal physiology as closely as '
                'possible." The dropdown list in step 3 shows ',link1,
                ' with different parameters. The filter is used to smooth the OpenAPS Autotune results. Flattening the curve like this will lead to basal rate recommendations that are more closely aligned with physiological values.'
                ' '
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
                'The resulting curve after applying the filter should preferably display one peak and one valley in insulin levels. You can find examples of how a curve could look per age range in', link4,
                '. A basal profile that has multiple peaks and valleys is often incorrect or compensating for some other aspect of the insulin administration that is incorrectly configured.'
                ]
            ),
            ]),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-savgol_filter", className="ml-auto")
        )],
        id="info",
        size="xl",  # "sm", "lg", "xl" = small, large or extra large
        backdrop=True,  # Modal to not be closed by clicking on backdrop
        scrollable=True,  # Scrollable in case of large amount of text
        centered=True,  # Vertically center modal
        keyboard=True,  # Close modal when escape is pressed
        fade=True,  # True, False
        # style={"max-width": "none", "width": "50%",}
    ),
    html.Br()
    ])



if __name__ == '__main__':
    from main import app
    app.layout = step3_graph
    app.run_server()