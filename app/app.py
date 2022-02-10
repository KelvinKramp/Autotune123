import dash
import dash_bootstrap_components as dbc
import os

assets_path = os.getcwd() +'/assets'

# START APP
app = dash.Dash(__name__,assets_folder=assets_path, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

