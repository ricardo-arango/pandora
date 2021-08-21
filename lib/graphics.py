import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import branca
import folium
from app import app
from dataloading import crime_df, barrio_geojson, spunit_db, spunit_js

# Year Dropdown option to display all year's information
allYears = "Todos"
anoDropdownOptions = np.append([allYears], crime_df["AÑO"].unique())

tabs_container = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Mapa Folium", tab_id="mapfolium"),
                dbc.Tab(label="Mapa Plotly", tab_id="mapplotly"),
                dbc.Tab(label="Línea", tab_id="line"),
                dbc.Tab(label="Barras", tab_id="barplot"),
                dbc.Tab(label="Dispersión", tab_id="scatter"),
                dbc.Tab(label="Histogramas", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="mapfolium",
        ),
        html.Div(id="tab-content", className="p-4"),
    ],
    className="tabscontainer"
)

lineCard = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Año"),
                dcc.Dropdown(
                    id="year",
                    options=[
                        {"label": col, "value": col} for col in anoDropdownOptions
                    ],
                    value=allYears,
                    clearable=False
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Día de la Semana"),
                dcc.Dropdown(
                    id="diasemana",
                    options=[
                        {"label": col, "value": col} for col in crime_df["DIA_SEMANA"].unique()
                    ],
                    clearable=False
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Barrio"),
                dcc.Dropdown(
                    id="barrio",
                    options=[
                        {"label": col, "value": col} for col in crime_df[spunit_db].unique()
                    ],
                    placeholder="Seleccione el barrio...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Tipo Lesión"),
                dcc.Dropdown(
                    id="tipolesion",
                    options=[
                        {"label": col, "value": col} for col in crime_df["TIPO_LESION"].unique()
                    ],
                    placeholder="Seleccione el tipo de lesión...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Tipo Delito"),
                dcc.Dropdown(
                    id="tipodelito",
                    options=[
                        {"label": col, "value": col} for col in crime_df["TIPO_DELITO_ARTICULO"].unique()
                    ],
                    placeholder="Seleccione el tipo de delito...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Grupo Etario Víctima"),
                dcc.Dropdown(
                    id="grupoetario",
                    options=[
                        {"label": col, "value": col} for col in crime_df["GRUPO_ETARIO_VICTIMA"].unique()
                    ],
                    placeholder="Seleccione el grupo etario de la víctima...",
                ),
            ]
        ),
    ],
    body=True,
)

lineContainer = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(lineCard, md=4),
                dbc.Col(dcc.Graph(id="line-plot"), md=8),
            ]
        ),
    ],
    fluid=True,
)

mapFoliumCard = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Año"),
                dcc.Dropdown(
                    id="map-fol-year",
                    options=[
                        {"label": col, "value": col} for col in crime_df["AÑO"].unique()
                    ],
                    value=2010,
                    clearable=False
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Barrio"),
                dcc.Dropdown(
                    id="map-fol-barrio",
                    options=[
                        {"label": col, "value": col} for col in crime_df[spunit_db].unique()
                    ],
                    placeholder="Seleccione el barrio...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Tipo Lesión"),
                dcc.Dropdown(
                    id="map-fol-tipolesion",
                    options=[
                        {"label": col, "value": col} for col in crime_df["TIPO_LESION"].unique()
                    ],
                    placeholder="Seleccione el tipo de lesión...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Tipo Delito"),
                dcc.Dropdown(
                    id="map-fol-tipodelito",
                    options=[
                        {"label": col, "value": col} for col in crime_df["TIPO_DELITO_ARTICULO"].unique()
                    ],
                    placeholder="Seleccione el tipo de delito...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Grupo Etario Víctima"),
                dcc.Dropdown(
                    id="map-fol-grupoetario",
                    options=[
                        {"label": col, "value": col} for col in crime_df["GRUPO_ETARIO_VICTIMA"].unique()
                    ],
                    placeholder="Seleccione el grupo etario de la víctima...",
                ),
            ]
        ),
    ],
    body=True,
)

mapFoliumContainer = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(mapFoliumCard, md=4),
                dbc.Col(html.Div(id="polygondiv", className="content"), md=8),
            ]
        )
    ],
    fluid=True,
)

mapPlotlyCard = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Año"),
                dcc.Dropdown(
                    id="map-plo-year",
                    options=[
                        {"label": col, "value": col} for col in crime_df["AÑO"].unique()
                    ],
                    value=2010,
                    clearable=False
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Barrio"),
                dcc.Dropdown(
                    id="map-plo-barrio",
                    options=[
                        {"label": col, "value": col} for col in crime_df[spunit_db].unique()
                    ],
                    placeholder="Seleccione el barrio...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Tipo Lesión"),
                dcc.Dropdown(
                    id="map-plo-tipolesion",
                    options=[
                        {"label": col, "value": col} for col in crime_df["TIPO_LESION"].unique()
                    ],
                    placeholder="Seleccione el tipo de lesión...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Tipo Delito"),
                dcc.Dropdown(
                    id="map-plo-tipodelito",
                    options=[
                        {"label": col, "value": col} for col in crime_df["TIPO_DELITO_ARTICULO"].unique()
                    ],
                    placeholder="Seleccione el tipo de delito...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Grupo Etario Víctima"),
                dcc.Dropdown(
                    id="map-plo-grupoetario",
                    options=[
                        {"label": col, "value": col} for col in crime_df["GRUPO_ETARIO_VICTIMA"].unique()
                    ],
                    placeholder="Seleccione el grupo etario de la víctima...",
                ),
            ]
        ),
    ],
    body=True,
)

mapPlotlyContainer = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(mapPlotlyCard, md=4),
                dbc.Col(dcc.Graph(id="map-plot-im", className="content"), md=8),
            ]
        )
    ],
    fluid=True,
)

barCard = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Año"),
                dcc.Dropdown(
                    id="bar-year",
                    options=[
                        {"label": col, "value": col} for col in anoDropdownOptions
                    ],
                    value=allYears,
                    clearable=False
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Barrio"),
                dcc.Dropdown(
                    id="bar-barrio",
                    options=[
                        {"label": col, "value": col} for col in crime_df[spunit_db].unique()
                    ],
                    placeholder="Seleccione el barrio...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Tipo Lesión"),
                dcc.Dropdown(
                    id="bar-tipolesion",
                    options=[
                        {"label": col, "value": col} for col in crime_df["TIPO_LESION"].unique()
                    ],
                    placeholder="Seleccione el tipo de lesión...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Tipo Delito"),
                dcc.Dropdown(
                    id="bar-tipodelito",
                    options=[
                        {"label": col, "value": col} for col in crime_df["TIPO_DELITO_ARTICULO"].unique()
                    ],
                    placeholder="Seleccione el tipo de delito...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Grupo Etario Víctima"),
                dcc.Dropdown(
                    id="bar-grupoetario",
                    options=[
                        {"label": col, "value": col} for col in crime_df["GRUPO_ETARIO_VICTIMA"].unique()
                    ],
                    placeholder="Seleccione el grupo etario de la víctima...",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Checklist(
                    id="bar-diasemana-toggle",
                    value=[0],
                    switch=True,
                ),
            ]
        )
    ],
    body=True,
)

barContainer = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(barCard, md=4),
                dbc.Col(dcc.Graph(id="bar-plot"), md=8),
            ]
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("bar-diasemana-toggle", "options"),
    [Input("bar-year", "value")],
)
def disable_disasemanab_toggle(year):
    return [{"label": "Mostrar por día de la semana", "value": 1, "disabled": year == allYears}]


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab is not None:
        if active_tab == "line":
            return lineContainer
        elif active_tab == "mapfolium":
            return mapFoliumContainer
        elif active_tab == "mapplotly":
            return mapPlotlyContainer
        elif active_tab == 'barplot':
            return barContainer
        elif active_tab == "histogram":
            return html.H1("Histogram en construcción...")
        elif active_tab == "scatter":
            return html.H1("Scatter en construcción...")
    return "Seleccione un tab..."


@app.callback(
    Output("line-plot", "figure"),
    [Input("year", "value"),
     Input("diasemana", "value"),
     Input("barrio", "value"),
     Input("tipolesion", "value"),
     Input("tipodelito", "value"),
     Input("grupoetario", "value")
     ],
)
def line_plot_monthly_cases_by_year(year, diaSemana, barrio, tipoLesion, tipoDelito, grupoEtario):
    if not year:
        year = 2010

    if year != allYears:
        cases_df = crime_df[crime_df["AÑO"] == int(year)]
    else:
        cases_df = crime_df.copy()

    if diaSemana:
        cases_df = cases_df[cases_df["DIA_SEMANA"] == diaSemana]
    if barrio:
        cases_df = cases_df[cases_df[spunit_db] == barrio]
    if tipoLesion:
        cases_df = cases_df[cases_df["TIPO_LESION"] == tipoLesion]
    if tipoDelito:
        cases_df = cases_df[cases_df["TIPO_DELITO_ARTICULO"] == tipoDelito]
    if grupoEtario:
        cases_df = cases_df[cases_df["GRUPO_ETARIO_VICTIMA"] == grupoEtario]

    if (year == allYears):
        filtered_cases = cases_df.groupby('AÑO').size().reset_index(name="Casos")
        plot_title = 'Número de casos por año'
        linePlot = px.line(
            filtered_cases,
            x="AÑO",
            y="Casos",
            title=plot_title,
            labels={"AÑO": "Año", "value": "Número de casos"}
        )
    else:
        filtered_cases = cases_df.groupby('MES_num').size().reset_index(name="Casos")
        plot_title = 'Número de casos en el año {}'.format(year)
        linePlot = px.line(
            filtered_cases,
            x="MES_num",
            y="Casos",
            title=plot_title,
            labels={"MES_num": "Mes", "value": "Número de casos"}
        )

    linePlot.update_xaxes(dtick="FECHA", ticklabelmode="period")
    linePlot.update_layout(title=plot_title, paper_bgcolor="#F8F9F9")
    return linePlot


@app.callback(
    Output("polygondiv", "children"),
    [
        Input("map-fol-year", "value"),
        Input("map-fol-barrio", "value"),
        Input("map-fol-tipolesion", "value"),
        Input("map-fol-tipodelito", "value"),
        Input("map-fol-grupoetario", "value")
    ],
)
def map_plot_cases(year, barrio, tipoLesion, tipoDelito, grupoEtario):
    if not year:
        year = 2010

    cases_df = crime_df[crime_df["AÑO"] == year]
    if barrio:
        cases_df = cases_df[cases_df[spunit_db] == barrio]
    if tipoLesion:
        cases_df = cases_df[cases_df["TIPO_LESION"] == tipoLesion]
    if tipoDelito:
        cases_df = cases_df[cases_df["TIPO_DELITO_ARTICULO"] == tipoDelito]
    if grupoEtario:
        cases_df = cases_df[cases_df["GRUPO_ETARIO_VICTIMA"] == grupoEtario]

    barrio_cn = cases_df.groupby(spunit_db)["CRIMEN_ID"].count().reset_index(name="casos")
    min_cn, max_cn = barrio_cn['casos'].quantile([0.01, 0.99]).apply(round, 2)

    colormap = branca.colormap.LinearColormap(
        colors=['white', 'yellow', 'orange', 'red', 'darkred'],
        vmin=min_cn,
        vmax=max_cn
    )

    colormap.caption = "Número total de casos por barrio"

    barrios_df = barrio_geojson.join(barrio_cn.set_index(spunit_db), how="left", on=spunit_js)
    barrios_df.fillna(0, inplace=True)

    bucaramangaPolygonMap = folium.Map(location=[7.11392, -73.1198], zoom_start=14, tiles="OpenStreetMap")

    style_function = lambda x: {
        'fillColor': colormap(x['properties']['casos']),
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5
    }

    folium.Marker(
        location=[7.118434983424289, -73.12493392800395],
        popup="<b>Centro</b>",
        icon=folium.Icon(color="red", icon="info-sign"),
        tooltip='Click acá'
    ).add_to(bucaramangaPolygonMap)

    folium.CircleMarker(
        location=[7.1300280499455075, -73.12479539095695],
        radius=10,
        popup="San Francisco",
        color="#007bff",
        fill=True,
        fill_color="#3186cc",
    ).add_to(bucaramangaPolygonMap)

    folium.GeoJson(
        barrios_df.to_json(),
        name='Casos en Bucaramanga en {}'.format(year),
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['NOMBRE', 'casos'],
            aliases=['Barrio', 'Total casos'],
            localize=True
        )
    ).add_to(bucaramangaPolygonMap)

    colormap.add_to(bucaramangaPolygonMap)
    bucaramangaPolygonMap.save("assets/bucaramanga-polygon.html")
    iframe = html.Iframe(id="polygonmap", srcDoc=open("assets/bucaramanga-polygon.html", "r").read(), width="100%",
                         height="100%")
    return iframe


@app.callback(
    Output("map-plot-im", "figure"),
    [
        Input("map-plo-year", "value"),
        Input("map-plo-barrio", "value"),
        Input("map-plo-tipolesion", "value"),
        Input("map-plo-tipodelito", "value"),
        Input("map-plo-grupoetario", "value")
    ],
)
def map_plot_cases(year, barrio, tipoLesion, tipoDelito, grupoEtario):
    if not year:
        year = 2010
    cases_df = crime_df[crime_df["AÑO"] == year]
    if barrio:
        cases_df = cases_df[cases_df[spunit_db] == barrio]
    if tipoLesion:
        cases_df = cases_df[cases_df["TIPO_LESION"] == tipoLesion]
    if tipoDelito:
        cases_df = cases_df[cases_df["TIPO_DELITO_ARTICULO"] == tipoDelito]
    if grupoEtario:
        cases_df = cases_df[cases_df["GRUPO_ETARIO_VICTIMA"] == grupoEtario]

    barrio_cn = cases_df.groupby(spunit_db)["CRIMEN_ID"].count().reset_index(name="casos")

    fig = px.choropleth(barrio_cn, geojson=barrio_geojson, color="casos",
                        locations=spunit_db, featureidkey="properties.NOMBRE",
                        projection="mercator"
                        )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


@app.callback(
    Output("bar-plot", "figure"),
    [Input("bar-year", "value"),
     Input("bar-barrio", "value"),
     Input("bar-tipolesion", "value"),
     Input("bar-tipodelito", "value"),
     Input("bar-grupoetario", "value"),
     Input("bar-diasemana-toggle", "value")
     ],
)
def bar_plot_monthly_cases_by_year(year, barrio, tipoLesion, tipoDelito, grupoEtario, mostrarPorDiaSemana):
    if not year:
        year = 2010

    if year != allYears:
        cases_df = crime_df[crime_df["AÑO"] == int(year)]
    else:
        cases_df = crime_df.copy()

    if barrio:
        cases_df = cases_df[cases_df[spunit_db] == barrio]
    if tipoLesion:
        cases_df = cases_df[cases_df["TIPO_LESION"] == tipoLesion]
    if tipoDelito:
        cases_df = cases_df[cases_df["TIPO_DELITO_ARTICULO"] == tipoDelito]
    if grupoEtario:
        cases_df = cases_df[cases_df["GRUPO_ETARIO_VICTIMA"] == grupoEtario]

    if (year == allYears):
        filtered_cases = cases_df.groupby('AÑO').size().reset_index(name="Casos")
        plot_title = 'Número de casos por año'
        barPlot = px.bar(
            filtered_cases,
            x="AÑO",
            y="Casos",
            title=plot_title,
            labels={"AÑO": "Año", "value": "Número de casos"}
        )
    elif len(mostrarPorDiaSemana) == 1:
        filtered_cases = cases_df.groupby('MES_num').size().reset_index(name="Casos")
        plot_title = 'Número de casos en el año {}'.format(year)
        barPlot = px.bar(
            filtered_cases,
            x="MES_num",
            y="Casos",
            title=plot_title,
            labels={"MES_num": "Mes", "value": "Número de casos"}
        )
    else:
        order = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
        filtered_cases = cases_df.groupby('DIA_SEMANA').size().reset_index(name="Casos")
        plot_title = 'Número de casos en el año'
        barPlot = px.bar(
            filtered_cases,
            x="DIA_SEMANA",
            y="Casos",
            title=plot_title,
            labels={"DIA_SEMANA": "Día de la semana", "value": "Número de casos"}
        )

    barPlot.update_xaxes(dtick="FECHA", ticklabelmode="period")
    barPlot.update_layout(title=plot_title, paper_bgcolor="#F8F9F9")
    return barPlot