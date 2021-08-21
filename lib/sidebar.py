import dash_html_components as html
import dash_bootstrap_components as dbc

sidebar = html.Div(
    [
        dbc.Nav(
            [
                dbc.NavLink(children=[html.I(className="fas fa-tachometer-alt fa-2x"), html.H6("Dashboard")], href="/", active="exact", className="sidebar-icons"),
                dbc.NavLink(children=[html.I(className="fas fa-venus-double fa-2x"), html.H6("Violencia sexual")], href="/graficas", active="exact", className="sidebar-icons"),
                dbc.NavLink(children=[html.I(className="fas fa-chart-pie fa-2x"), html.H6("Reportes")], href="/reportes", active="exact", className="sidebar-icons"),
                dbc.NavLink(children=[html.I(className="far fa-chart-bar fa-2x"), html.H6("Resumen")], href="/resumen", active="exact", className="sidebar-icons"),
                dbc.NavLink(html.Hr())
            ],
            vertical=True,
            fill=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


