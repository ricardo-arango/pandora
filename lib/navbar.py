import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app

navbar = dbc.Navbar(
    [
        html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=app.get_asset_url("escudo-sm.svg"), className="escudo-banner")),
                        dbc.Col(dbc.NavbarBrand("P A N D O R A", className="ml-2",style={"color":"#bbbbbb"}))
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://www.bucaramanga.gov.co/Inicio/",
            )
    ],
    color="#354454",
    className="navbar"
)