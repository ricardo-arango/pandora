# ################################################################################
# Module      : tools.py
# Description : Enable the user to upload a new crime database in csv format
#               Describe user database minimum requirements
#               Spatilly join user database with spatial units nnd police stations
# ################################################################################

# ################################################################################
# Load/invoke required libraries/modules
# ################################################################################
import base64
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_table
import datetime
import io
import geopandas
from geopandas.tools import sjoin
from geopy import distance
import pandas as pd
import numpy as np
from sklearn.neighbors import BallTree

from app import app
import dataloading

# ################################################################################
# Declare and define variables/objects
# ################################################################################
db_requirements = pd.DataFrame(data={"COLUMNA": range(1,27),
                                     "NOMBRE": ["CRIMEN_ID", "FECHA", "AÑO", "MES", "MES_num", "DIA", "DIA_SEMANA", "DIA_SEMANA_num", "LATITUD", "LONGITUD", "ZONA", "COMUNA", "COMUNA_num", "BARRIO", "TIPO_DELITO_ARTICULO", "TIPO_DELITO", "TIPO_CONDUCTA", "TIPO_LESION", "GENERO_VICTIMA", "EDAD_VICTIMA", "GRUPO_ETARIO_VICTIMA", "GRUPO_ETARIO_VICTIMA_num", "ESTADO_CIVIL_VICTIMA", "MEDIO_TRANSPORTE_VICTIMA", "MEDIO_TRANSPORTE_VICTIMARIO", "TIPO_ARMA"],
                                     "FORMATO": ["dd/mm/aaaa", "Entero", "Entero", "Texto", "Entero", "Entero", "Texto", "Entero", "Decimal", "Decimal", "Texto", "Texto", "Entero", "Texto", "Texto", "Texto", "Texto", "Texto", "Texto", "Entero", "Texto", "Entero", "Texto", "Texto", "Texto", "Texto"],
                                     "VALOR FALTANTE": ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "En blanco", "En blanco", "NO REPORTA", "NO REPORTA", "0", "NO REPORTA", "NO REPORTA", "NO REPORTA", "NO REPORTA", "NO REPORTA", "NO REPORTA", "-1", "NO REPORTA", "0", "NO REPORTA", "NO REPORTA", "NO REPORTA", "NO REPORTA"]})

# ################################################################################
# Declare container components
# ################################################################################
tools_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("Herramientas", className="card-title panel-title"),
                                html.Hr()
                        ])
                    ], width=12,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H4("El aplicativo usa por defecto una versión ajustada y enriquecida de la base de datos "
                                        "de delitos registrados en Bucaramanga entre enero de 2010 a febrero de 2021 del "
                                        "repositorio de Datos Abiertos del Gobierno de Colombia. El enriquecimiento de los datos "
                                        "consiste en la union espacial de la base de datos con los polígonos de barrios, comunas y "
                                        "corregimientos y y el cálculo de la distancia de cada delito a la estación de policía más "
                                        "cercana. Si el usuario desea considerar una base de datos diferente para el análisis, debe "
                                        "preparar un archivo en formato csv con los campos y formatos que se enlistan a continuación. "
                                        " Los campos relacionados con la fecha de cada delito no puedne tener datos faltantes."
                                        , className="card-title panel-title"),
                                html.Hr(),
                        ])
                    ], width=12,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                 dash_table.DataTable(
                                     data=db_requirements.to_dict('records'),
                                     columns=[{'name': i, 'id': i} for i in db_requirements.columns],
                                     style_cell={'textAlign': 'left'},
                                     style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
                                 ),
                                html.Hr(),
                        ])
                    ], width=12,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H4("Arrastre y sulte en el recuadro de abajo o seleccione el archivo que desea "
                                        "considerar para el análisis. Tenga en cuenta que el procesamiento y enriquecimiento "
                                        "de los datos puede tardar varios minutos. Una vez procesados, el aplicativo "
                                        "mostrará el nombre del archivo subido y la fecha de la última vez "
                                        "que fue modificado."
                                        , className="card-title panel-title"),
                                html.Hr(),
                        ])
                    ], width=12,
                ),
                dbc.Col(
                    [
                        html.Div([
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Arrastrar y Soltar o ',
                                    html.A('Seleccionar Archivo', style={'color': 'blue'})
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '60px',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                multiple=False
                            ),
                            html.Div(id='output-data-upload'),
                        ])
                    ], width=12,
                )
            ]
        ),
    ],
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)

# ################################################################################
# Declare functions
# ################################################################################
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if '.csv' in filename:
            # Load and adjust user crime database
            dtypes = {"CRIMEN_ID": "int64",
                      "AÑO": "int64",
                      "MES": "category",
                      "MES_num": "int64",
                      "DIA": "int64",
                      "DIA_SEMANA": "category",
                      "DIA_SEMANA_num": "int64",
                      "LATITUD": "float64",
                      "LONGITUD": "float64",
                      "ZONA": "category",
                      "COMUNA": "category",
                      "COMUNA_num": "int64",
                      "BARRIO": "category",
                      "TIPO_DELITO_ARTICULO": "category",
                      "TIPO_DELITO": "category",
                      "TIPO_CONDUCTA": "category",
                      "TIPO_LESION": "category",
                      "GENERO_VICTIMA": "category",
                      "EDAD_VICTIMA": "int64",
                      "GRUPO_ETARIO_VICTIMA": "category",
                      "GRUPO_ETARIO_VICTIMA_num": "int64",
                      "ESTADO_CIVIL_VICTIMA": "category",
                      "MEDIO_TRANSPORTE_VICTIMA": "category",
                      "MEDIO_TRANSPORTE_VICTIMARIO": "category",
                      "TIPO_ARMA": "category"}
            dataloading.crime_df = pd.read_csv(io.StringIO(decoded.decode('utf-8'))).astype(dtypes)

            # Adjust value order of several categorical fields
            column_dtype = pd.api.types.CategoricalDtype(categories=['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE'], ordered=True)
            dataloading.crime_df["MES"] = dataloading.crime_df["MES"].astype(column_dtype)
            column_dtype = pd.api.types.CategoricalDtype(categories=['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO'], ordered=True)
            dataloading.crime_df["DIA_SEMANA"] = dataloading.crime_df["DIA_SEMANA"].astype(column_dtype)
            column_dtype = pd.api.types.CategoricalDtype(categories=['PRIMERA INFANCIA', 'INFANCIA', 'ADOLESCENCIA', 'JOVENES', 'ADULTEZ', 'PERSONA MAYOR', 'NO REPORTA'], ordered=True)
            dataloading.crime_df["GRUPO_ETARIO_VICTIMA"] = dataloading.crime_df["GRUPO_ETARIO_VICTIMA"].astype(column_dtype)

            # Join spatial units with crime database
            crime_coordinates = geopandas.GeoDataFrame(dataloading.crime_df[["CRIMEN_ID", "BARRIO", "COMUNA"]], crs='epsg:4326', geometry=geopandas.points_from_xy(dataloading.crime_df.LONGITUD, dataloading.crime_df.LATITUD))
            crime_spunits = sjoin(crime_coordinates, dataloading.barrio_geojson, how="left")
            dataloading.crime_df.loc[:, dataloading.spunit_db] = np.nan
            dataloading.crime_df.loc[np.array(crime_spunits["CRIMEN_ID"] - 1), dataloading.spunit_db] = np.array(crime_spunits[dataloading.spunit_js])
            dataloading.crime_df[dataloading.spunit_db] = dataloading.crime_df[dataloading.spunit_db].fillna("NO REPORTA")

            # Convert WGS84 lat/lon coordinates (degrees) to WGS84-UTM 18N coordinates (meters)
            projected_police_station = dataloading.police_geojson.to_crs("EPSG:32618")
            projected_crime_coordinates = crime_coordinates.to_crs("EPSG:32618")

            # Identify nearest police station by lineal distance
            dist2police = pd.DataFrame()
            for i in projected_police_station.index:
                x1 = projected_police_station["geometry"].x[i]
                y1 = projected_police_station["geometry"].y[i]
                dist2police[i] = np.sqrt((projected_crime_coordinates["geometry"].x - x1) ** 2 +
                                         (projected_crime_coordinates["geometry"].y - y1) ** 2)
            mindist = dist2police.min(axis=1, skipna=True).replace(np.inf, np.nan) / 1000
            nearps = dist2police.idxmin(axis=1, skipna=True)
            dataloading.crime_df["DISTANCIA_ESTACION_POLICIA_CERCANA"] = mindist
            dataloading.crime_df["ESTACION_POLICIA_CERCANA"] = dataloading.police_geojson.loc[nearps.values, "NOMBRE"].values

            # Release memory of unnecessary objects
            del mindist, nearps, dist2police, x1, y1, projected_police_station, projected_crime_coordinates, crime_coordinates, crime_spunits

            # Reorder dataframe columns
            dataloading.crime_df = dataloading.crime_df[['CRIMEN_ID', 'FECHA', 'AÑO', 'MES', 'MES_num', 'DIA', 'DIA_SEMANA', 'DIA_SEMANA_num',
                                 'LATITUD', 'LONGITUD', 'ZONA', 'COMUNA', 'COMUNA_num', 'BARRIO', dataloading.spunit_db,
                                 'TIPO_DELITO_ARTICULO', 'TIPO_DELITO', 'TIPO_CONDUCTA', 'TIPO_LESION',
                                 'GENERO_VICTIMA', 'EDAD_VICTIMA', 'GRUPO_ETARIO_VICTIMA', 'GRUPO_ETARIO_VICTIMA_num',
                                 'ESTADO_CIVIL_VICTIMA', 'MEDIO_TRANSPORTE_VICTIMA', 'MEDIO_TRANSPORTE_VICTIMARIO', 'TIPO_ARMA',
                                 'DISTANCIA_ESTACION_POLICIA_CERCANA', 'ESTACION_POLICIA_CERCANA']]

    except Exception as e:
        print(e)
        return html.Div([
            'Hubo un error procesando el archivo. Asegúrese de que este siga los requerimientos anteriormente descritos.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
    ])

# ################################################################################
# Declare callbacks
# ################################################################################
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents, list_of_names, list_of_dates)]
        return children

