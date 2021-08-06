import pathlib
import dash
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
import geopandas
from app import app
from lib import sidebar, content, graphics, navbar, home
app.layout = html.Div([dcc.Location(id="url"), navbar.navbar, sidebar.sidebar, content.content])

# ################################################################################
# starting the main map
# ################################################################################



# ################################################################################
# Loading the data
# ################################################################################
# crime_df = pd.read_csv("data/2010-2021.csv", delimiter=",")
# crime_df["GRUPO_ETARIO_VICTIMA"] = crime_df["GRUPO_ETARIO_VICTIMA"].fillna("00. Sin Información")
# barrio_geojson = geopandas.read_file("data/barrios_bucaramanga.geojson", driver="GeoJSON")
# Commented out because the html report is already created and saved under de assets folder
# crime_df = pd.read_csv("data/policia-2010-2020-cleanedup.csv", delimiter=",")
# profile = pandas_profiling.ProfileReport(crime_df)
# profile.to_file("reporte-datos-policia.html")




# ################################################################################
# Callbacks
# ################################################################################
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/user/ricardoutd@gmail.com/proxy/8050/" or pathname == "/user/ricardoutd@gmail.com/proxy/8050":
        return home.home_container
    elif pathname == "/user/ricardoutd@gmail.com/proxy/8050/graficas":
        return graphics.tabs_container
    elif pathname == "/user/ricardoutd@gmail.com/proxy/8050/reportes":
        return profile_data
    elif pathname == "/user/ricardoutd@gmail.com/proxy/8050/resumen":
        return html.H2("Resumen")
    else:
        return home.home_container
        # If the user tries to reach a different page, return a 404 message
#         return dbc.Jumbotron(
#             [
#                 html.H1("404: Not found", className="text-danger"),
#                 html.Hr(),
#                 html.P(f"La URL {pathname} no existe."),
#             ]
#         )


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("positioned-toast", "is_open"),
    [Input("btn-buscar", "n_clicks")],
)
def open_toast(n):
    if n:
        return True
    return False


@app.callback(
    Output("btn-buscar", "disabled"),
    [Input("buscar-text", "value")],
)
def toggle_disabled_search_button(value):
    if not value:
        return True
    return False


# Initiate the server where the app will work
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', debug=True)