from dash import html, Input, Output, State
from dash import dcc
from app.app import app
import dash_bootstrap_components as dbc
import requests


counter = html.Div([
        dbc.Button("testing",id="count",n_clicks=0),
        dcc.Input(
            id="input-url", type="url", placeholder="NightScout URL", required=True,
            style={'marginBottom': '1.5em', 'text-align': 'center'},
        ),
        html.Div(id="empyt-output"),
    ])


@app.callback(
    Output("empty-output", "is_open"),
    [Input("count", "n_clicks")],
    State("input-url","value")
)
def toggle_alert_no_fade(n):
    print(2)
    if n:
        return None
    return None

if __name__ == '__main__':
    app.layout = counter
    app.run_server(host='0.0.0.0', port=8000, debug=True, use_reloader=True)