import dash_bootstrap_components as dbc
from dash import html
import dash

app = dash.Dash(__name__,
                # assets_folder=assets_path,
                title="Autotune123",
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.FLATLY]
                )


app.layout = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="http:/"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8000, debug=False, use_reloader=True)