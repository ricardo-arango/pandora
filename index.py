# ################################################################################
# Load/invoke required libraries/modules
# ################################################################################
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from lib import sidebar, content, navbar, home, sexualviolence, predictions, tools, about

# ################################################################################
# Set app layout
# ################################################################################
app.layout = html.Div([dcc.Location(id="url"), navbar.navbar, sidebar.sidebar, content.content])

# ################################################################################
# Declare callbacks
# ################################################################################
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/" or pathname == "":
        return home.home_container
    elif pathname == "/sexualviolence":
        return sexualviolence.sexual_violence_container
    elif pathname == "/predictions":
        return predictions.predictions_container
    elif pathname == "/tools":
        return tools.tools_container
    elif pathname == "/about":
        return about.about_container
    elif pathname == "/charts":
        return html.h5()
    else:
        return home.home_container


# Initiate the server where the app will work
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port='8050', debug=True)
