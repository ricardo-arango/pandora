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
db_requirements = pd.DataFrame(data={"COLUMNA": range(1, 27),
                                     "NOMBRE": ["CRIMEN_ID", "FECHA", "AÑO", "MES", "MES_num", "DIA", "DIA_SEMANA", "DIA_SEMANA_num", "LATITUD", "LONGITUD", "ZONA", "COMUNA", "COMUNA_num", "BARRIO", "TIPO_DELITO_ARTICULO", "TIPO_DELITO", "TIPO_CONDUCTA", "TIPO_LESION", "GENERO_VICTIMA", "EDAD_VICTIMA", "GRUPO_ETARIO_VICTIMA", "GRUPO_ETARIO_VICTIMA_num", "ESTADO_CIVIL_VICTIMA", "MEDIO_TRANSPORTE_VICTIMA", "MEDIO_TRANSPORTE_VICTIMARIO", "TIPO_ARMA"],
                                     "FORMATO": ["dd/mm/aaaa", "Entero", "Entero", "Texto", "Entero", "Entero", "Texto", "Entero", "Decimal", "Decimal", "Texto", "Texto", "Entero", "Texto", "Texto", "Texto", "Texto", "Texto", "Texto", "Entero", "Texto", "Entero", "Texto", "Texto", "Texto", "Texto"],
                                     "VALOR FALTANTE": ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "En blanco", "En blanco", "NO REPORTA", "NO REPORTA", "0", "NO REPORTA", "NO REPORTA", "NO REPORTA", "NO REPORTA", "NO REPORTA", "NO REPORTA", "-1", "NO REPORTA", "0", "NO REPORTA", "NO REPORTA", "NO REPORTA", "NO REPORTA"]})

notice_label = "Pandora usa por defecto una versión ajustada y enriquecida de la base de datos de delitos registrados en Bucaramanga " \
"entre Enero de 2010 y Febrero de 2021 del repositorio de Datos Abiertos del Gobierno de Colombia. El enriquecimiento de los datos " \
"consiste en la union espacial de la base de datos con los polígonos de barrios, comunas y corregimientos y y el cálculo de la distancia " \
"de cada delito a la estación de policía más cercana. Si el usuario desea considerar una base de datos diferente para el análisis, debe " \
"preparar un archivo en formato csv con los campos y formatos que se muestran a continuación. Los campos relacionados con la fecha de " \
"cada delito no puede tener datos faltantes."

drag_drop_notice_label = "Arrastre y sulte el archivo en el recuadro de abajo o haga click para seleccionar el archivo que desea considerar " \
"para el análisis. Tenga en cuenta que el procesamiento y enriquecimiento de los datos puede tardar varios minutos. Una vez procesados, " \
"Pandora mostrará el nombre del archivo subido y la fecha de la última vez que fue modificado."
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
                                html.H3("Herramientas", className="card-title",
                                    style={"font-family": "revert", "color": "#5f5f5f", "margin-left": "5px"}
                                ),
                                html.Hr(),
                        ])
                    ], width=12,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Tabs(
                            [
                                dbc.Tab(
                                    label="Actualizar archivo CSV",
                                    tab_id="update-csv-tab",
                                    labelClassName="tabs-font",
                                    activeLabelClassName="tabs-font-selected")
                            ],
                            id="tabs",
                            active_tab="update-csv-tab",
                        ),
                        html.Div(id="tools-tab-content"),
                    ], width=12,
                ),
            ]
        ),
    ],
    fluid=True
)

update_csv_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Actualización de base de datos de casos", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.H6(notice_label
                                                            , className="tools-notice"),
                                                    html.Br(),
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
                                                         style_header={
                                                             'fontWeight': 'bold'
                                                         }
                                                     ),
                                                    html.Br(),
                                            ])
                                        ], width=12,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.H6(drag_drop_notice_label, className="tools-notice"),
                                                    html.Br(),
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
                                                        html.A('Seleccionar Archivo', style={'color': '#1074f1'})
                                                    ]),
                                                    className="drag-n-drop-panel",
                                                    multiple=False
                                                )
                                            ])
                                        ], width=12,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Br(),
                                            dbc.Spinner(dbc.Alert(
                                                [
                                                    html.Div([
                                                        html.H4(id="alert-title", className="alert-heading"),
                                                        html.Hr(),
                                                        html.P(id="filename-uploaded"),
                                                        html.P(id="date-uploaded"),
                                                    ], id='output-data-upload')
                                                ],
                                                id="uploaded-alert",
                                                dismissable=True,
                                                fade=False,
                                                is_open=False,
                                            ), color="info", type="grow", fullscreen=True),
                                        ], width=12,
                                    )
                                ], style={"padding": "0 16px 0 16px"})
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="12"
                )
            ]
        )
    ],
    id="update-csv-container",
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)

@app.callback(
    Output("tools-tab-content", "children"),
    Input("tabs", "active_tab"),
)
def render_tab_content(active_tab):
    if active_tab is not None:
        if active_tab == "update-csv-tab":
            return update_csv_container
    return update_csv_container

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

            # Release memory from unnecessary objects
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
        return 'Hubo un error procesando el archivo. Asegúrese de que este siga los requerimientos anteriormente descritos.', ''

    return filename, datetime.datetime.fromtimestamp(date)

# ################################################################################
# Declare callbacks
# ################################################################################
@app.callback(
    [
        Output('filename-uploaded', 'children'),
        Output('date-uploaded', 'children'),
        Output('alert-title', 'children'),
        Output('uploaded-alert', 'is_open'),
        Output('uploaded-alert', 'color'),
    ],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    State('uploaded-alert', 'is_open'),
)
def update_output(list_of_contents, list_of_names, list_of_dates, is_open):
    file_name = None
    file_date = None
    box_color = 'success'
    is_open = False
    alert_title = 'Actualización exitosa.'
    if list_of_contents is not None:
        file_name, file_date = parse_contents(list_of_contents, list_of_names, list_of_dates)
        print(file_name, file_date)
    if file_date is None:
        is_open = False
    elif file_date == '':
        is_open = True
        box_color = 'danger'
        alert_title = 'Error en la actualización.'
    else:
        is_open = True

    return file_name, file_date, alert_title, is_open, box_color

