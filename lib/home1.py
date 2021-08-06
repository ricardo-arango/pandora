import dash_html_components as html
import dash_bootstrap_components as dbc
import folium
import pandas as pd
import geopandas
import branca

# Temporal cleaning up here
crime_df = pd.read_csv("data/2010-2021.csv", delimiter=",")
crime_df["GRUPO_ETARIO_VICTIMA"] = crime_df["GRUPO_ETARIO_VICTIMA"].fillna("00. Sin Información")

# Read the geojson for map plotting
barrio_geojson = geopandas.read_file("data/barrios_bucaramanga.geojson", driver="GeoJSON")

card = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Feminicidios", className="card-title"),
            html.P(
                "Some quick example text to build on the card title and make "
                "up the bulk of the card's content.",
                className="card-text",
            )
        ]
    ),
    style={"width": "18rem"},
)

def create_map():
    year = 2020
    cases_df = crime_df[crime_df["AÑO"] == year]
    barrio_cn = cases_df.groupby("BARRIO")["CRIMEN_ID"].count().reset_index(name="casos")
    min_cn, max_cn = barrio_cn['casos'].quantile([0.01, 0.99]).apply(round, 2)

    colormap = branca.colormap.LinearColormap(
        colors=['white', 'yellow', 'orange', 'red', 'darkred'],
        vmin=min_cn,
        vmax=max_cn
    )

    colormap.caption = "Número total de casos por barrio"

    barrios_df = barrio_geojson.join(barrio_cn.set_index("BARRIO"), how="left", on="NOMBRE")
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
    map_renderer = html.Iframe(id="polygonmap", srcDoc=open("assets/bucaramanga-polygon.html", "r").read(), width="100%",
                         height="100%")
    return map_renderer


home_container = dbc.Container(
    [
        html.Br(),
        html.Div(
            [
                dbc.Row(
                    [
                        card
                    ]
                ),
                dbc.Row(
                    [
                        html.Div(create_map(), id="map-content", className="mapcontent")
                    ]
                ),
            ],
            id="cards-content"
        ),
    ],
    id="home-content",
    className='tabscontainer'
)