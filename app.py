import dash
import dash_bootstrap_components as dbc
#import pandas as pd
#import geopandas
import os



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
FA = "https://use.fontawesome.com/releases/v5.15.3/css/all.css"

#external_stylesheets = ["{% static 'fontawesomefree/js/all.min.js' %}"]
request_path_prefix = None
workspace_user = os.getenv('JUPYTERHUB_USER')  # Get DS4A Workspace user name
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'

app = dash.Dash(
    __name__,
    requests_pathname_prefix = request_path_prefix,
    external_stylesheets = [dbc.themes.BOOTSTRAP, FA]
)

'''
# ################################################################################
# Loading the data
# ################################################################################
global crime_df
global barrio_geojson
crime_df = pd.read_csv("data/2010-2021.csv", delimiter=",")
barrio_geojson = geopandas.read_file("data/barrios_bucaramanga.geojson", driver="GeoJSON")
'''

# We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True