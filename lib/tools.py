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
import dataloading
import pandas as pd
import numpy as np

from geopandas.tools import sjoin
from lib import applicationconstants


from app import app


# ################################################################################
# Declare and define variables/objects
# ################################################################################
db_requirements = pd.DataFrame(
    data={
        "COLUMNA": range(1, 27),
         "NOMBRE": [
             applicationconstants.CRIMEN_ID,
             applicationconstants.FECHA,
             applicationconstants.AÑO,
             applicationconstants.MES,
             applicationconstants.MES_num,
             applicationconstants.DIA,
             applicationconstants.DIA_SEMANA,
             applicationconstants.DIA_SEMANA_num,
             applicationconstants.LATITUD,
             applicationconstants.LONGITUD,
             applicationconstants.ZONA,
             applicationconstants.COMUNA,
             applicationconstants.COMUNA_num,
             applicationconstants.BARRIO,
             applicationconstants.TIPO_DELITO_ARTICULO,
             applicationconstants.TIPO_DELITO,
             applicationconstants.TIPO_CONDUCTA,
             applicationconstants.TIPO_LESION,
             applicationconstants.GENERO_VICTIMA,
             applicationconstants.EDAD_VICTIMA,
             applicationconstants.GRUPO_ETARIO_VICTIMA,
             applicationconstants.GRUPO_ETARIO_VICTIMA_num,
             applicationconstants.ESTADO_CIVIL_VICTIMA,
             applicationconstants.MEDIO_TRANSPORTE_VICTIMA,
             applicationconstants.MEDIO_TRANSPORTE_VICTIMARIO,
             applicationconstants.TIPO_ARMA
         ],
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
        if filename.endswith(".csv"):
            # Load and adjust user crime database
            dtypes = {applicationconstants.CRIMEN_ID: "int64",
                      applicationconstants.AÑO: "int64",
                      applicationconstants.MES: "category",
                      applicationconstants.MES_num: "int64",
                      applicationconstants.DIA: "int64",
                      applicationconstants.DIA_SEMANA: "category",
                      applicationconstants.DIA_SEMANA_num: "int64",
                      applicationconstants.LATITUD: "float64",
                      applicationconstants.LONGITUD: "float64",
                      applicationconstants.ZONA: "category",
                      applicationconstants.COMUNA: "category",
                      applicationconstants.COMUNA_num: "int64",
                      applicationconstants.BARRIO: "category",
                      applicationconstants.TIPO_DELITO_ARTICULO: "category",
                      applicationconstants.TIPO_DELITO: "category",
                      applicationconstants.TIPO_CONDUCTA: "category",
                      applicationconstants.TIPO_LESION: "category",
                      applicationconstants.GENERO_VICTIMA: "category",
                      applicationconstants.EDAD_VICTIMA: "int64",
                      applicationconstants.GRUPO_ETARIO_VICTIMA: "category",
                      applicationconstants.GRUPO_ETARIO_VICTIMA_num: "int64",
                      applicationconstants.ESTADO_CIVIL_VICTIMA: "category",
                      applicationconstants.MEDIO_TRANSPORTE_VICTIMA: "category",
                      applicationconstants.MEDIO_TRANSPORTE_VICTIMARIO: "category",
                      applicationconstants.TIPO_ARMA: "category"}
            file_to_save = pd.read_csv(io.StringIO(decoded.decode('utf-8'))).astype(dtypes)

            # Adjust value order of several categorical fields
            column_dtype = pd.api.types.CategoricalDtype(categories=dataloading.months_caps, ordered=True)
            file_to_save[applicationconstants.MES] = file_to_save[applicationconstants.MES].astype(column_dtype)
            column_dtype = pd.api.types.CategoricalDtype(categories=dataloading.week_days_caps, ordered=True)
            file_to_save[applicationconstants.DIA_SEMANA] = file_to_save[applicationconstants.DIA_SEMANA].astype(column_dtype)
            column_dtype = pd.api.types.CategoricalDtype(categories=dataloading.age_group_caps, ordered=True)
            file_to_save[applicationconstants.GRUPO_ETARIO_VICTIMA] = file_to_save[applicationconstants.GRUPO_ETARIO_VICTIMA].astype(column_dtype)

            # Join spatial units with crime database
            crime_coordinates = geopandas.GeoDataFrame(file_to_save[[applicationconstants.CRIMEN_ID, applicationconstants.BARRIO, applicationconstants.COMUNA]], crs='epsg:4326', geometry=geopandas.points_from_xy(file_to_save.LONGITUD, file_to_save.LATITUD))
            crime_spunits = sjoin(crime_coordinates, dataloading.barrio_geojson, how="left")
            file_to_save.loc[:, applicationconstants.UNIDAD_ESPACIAL] = np.nan
            file_to_save.loc[np.array(crime_spunits[applicationconstants.CRIMEN_ID] - 1), applicationconstants.UNIDAD_ESPACIAL] = np.array(crime_spunits[applicationconstants.NOMBRE])
            file_to_save[applicationconstants.UNIDAD_ESPACIAL] = file_to_save[applicationconstants.UNIDAD_ESPACIAL].fillna("NO REPORTA")

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
            file_to_save[applicationconstants.DISTANCIA_ESTACION_POLICIA_CERCANA] = mindist
            file_to_save[applicationconstants.ESTACION_POLICIA_CERCANA] = dataloading.police_geojson.loc[nearps.values, "NOMBRE"].values

            # Release memory from unnecessary objects
            del mindist, nearps, dist2police, x1, y1, projected_police_station, projected_crime_coordinates, crime_coordinates, crime_spunits

            # Reorder dataframe columns
            file_to_save = file_to_save[[
                applicationconstants.CRIMEN_ID,
                applicationconstants.FECHA,
                applicationconstants.AÑO,
                applicationconstants.MES,
                applicationconstants.MES_num,
                applicationconstants.DIA,
                applicationconstants.DIA_SEMANA,
                applicationconstants.DIA_SEMANA_num,
                applicationconstants.LATITUD,
                applicationconstants.LONGITUD,
                applicationconstants.ZONA,
                applicationconstants.COMUNA,
                applicationconstants.COMUNA_num,
                applicationconstants.BARRIO,
                applicationconstants.UNIDAD_ESPACIAL,
                applicationconstants.TIPO_DELITO_ARTICULO,
                applicationconstants.TIPO_DELITO,
                applicationconstants.TIPO_CONDUCTA,
                applicationconstants.TIPO_LESION,
                applicationconstants.GENERO_VICTIMA,
                applicationconstants.EDAD_VICTIMA,
                applicationconstants.GRUPO_ETARIO_VICTIMA,
                applicationconstants.GRUPO_ETARIO_VICTIMA_num,
                applicationconstants.ESTADO_CIVIL_VICTIMA,
                applicationconstants.MEDIO_TRANSPORTE_VICTIMA,
                applicationconstants.MEDIO_TRANSPORTE_VICTIMARIO,
                applicationconstants.TIPO_ARMA,
                applicationconstants.DISTANCIA_ESTACION_POLICIA_CERCANA,
                applicationconstants.ESTACION_POLICIA_CERCANA]]
            dataloading.crime_df = pd.DataFrame(file_to_save)
        else:
            return 'El archivo debe tener la extensión .csv', ''

    except Exception as e:
        print(e)
        return 'Hubo un error procesando el archivo. Asegúrese de que este siga los requerimientos anteriormente descritos.', ''

    return 'Nombre de archivo: ' + filename, 'Última fecha de actualización de archivo: ' + datetime.datetime.fromtimestamp(date).strftime('%d/%m/%Y')

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

