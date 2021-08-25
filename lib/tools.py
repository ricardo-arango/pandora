import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from app import app

import io
import base64
import pandas as pd
import datetime
import dash_table
from dataloading import crime_df, dtypes

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
                                        "repositorio de Datos Abiertos del Gobierno de Colombia. Si el usuario desea considerar "
                                        "una base de datos diferente para el análisis, debe arastrar y soltar o seleccionar el "
                                        "archivo en formato csv en el recuadro de abajo."
                                        , className="card-title panel-title"),
                                #html.Hr()
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
                                    html.A('Seleccionar Archivo')
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
                                # Allow multiple files to be uploaded
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


def parse_contents(contents, filename, date):
    global crime_df
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if '.csv' in filename:
            # Assume that the user uploaded a CSV file
            crime_df = pd.read_csv(io.StringIO(decoded.decode('utf-8'))).astype(dtypes)
            #df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), delimiter=",", encoding="utf-8", dtype=types,
            #                       parse_dates=["FECHA"])
            #return df
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=crime_df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in crime_df.columns]
        ),

        #html.Hr(),  # horizontal line

        # # For debugging, display the raw contents provided by the web browser
        # html.Div('Raw Content'),
        # html.Pre(contents[0:200] + '...', style={
        #     'whiteSpace': 'pre-wrap',
        #     'wordBreak': 'break-all'
        # })
    ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    # if list_of_contents is not None:
    #     children = [
    #         parse_contents(c, n, d) for c, n, d in
    #         zip(list_of_contents, list_of_names, list_of_dates)]
    #     return children
    if list_of_contents is not None:
        children = [parse_contents(list_of_contents, list_of_names, list_of_dates)]
        return children

