import dash
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
FA = "https://use.fontawesome.com/releases/v5.15.3/css/all.css"

#external_stylesheets = ["{% static 'fontawesomefree/js/all.min.js' %}"]
request_path_prefix = None

app = dash.Dash(
    __name__,
    requests_pathname_prefix = request_path_prefix,
    external_stylesheets = [dbc.themes.BOOTSTRAP, FA]
)

# We need this for function callbacks not present in the app.layout
app.config.suppress_callback_exceptions = True