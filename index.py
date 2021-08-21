# ################################################################################
# Load/invoke required libraries/modules
# ################################################################################
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from lib import sidebar, content, graphics, navbar, home

# ################################################################################
# XXXXXXX
# ################################################################################
app.layout = html.Div([dcc.Location(id="url"), navbar.navbar, sidebar.sidebar, content.content])

# ################################################################################
# starting the main map
# ################################################################################



# ################################################################################
# Callbacks
# ################################################################################
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/" or pathname == "":
        return home.home_container
    elif pathname == "/graficas":
        return graphics.tabs_container
    elif pathname == "/reportes":
        return profile_data
    elif pathname == "/resumen":
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