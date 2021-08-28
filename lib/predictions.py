import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import dataloading
from dataloading import months
from app import app
from dataloading import crime_df, police_df, barrio_geojson, spunit_db, spunit_js
from datetime import date
from dash.dependencies import Input, Output, State

from lib import applicationconstants
from dataloading import crime_df

from tensorflow import keras
model = keras.models.load_model('data/Neural_net_Mintic.h5')
raw_data = dataloading.crime_df.copy()
raw_data['COMUNA'] = raw_data['COMUNA'].str.strip()
raw_data['UNIDAD_ESPACIAL'] = raw_data['UNIDAD_ESPACIAL'].str.strip()
raw_data['TIPO_DELITO'] = raw_data['TIPO_DELITO'].str.strip()
raw_data['UNIDAD_ESPACIAL'].replace({'NO REPORTA': np.nan}, inplace=True)
raw_data['TIPO_DELITO'].replace({'NO REPORTA': np.nan}, inplace=True)
raw_data.dropna(inplace=True)

nn_data = raw_data[['MES_num', 'DIA', 'DIA_SEMANA_num', 'UNIDAD_ESPACIAL', 'COMUNA', 'TIPO_DELITO', 'AÑO', 'DIA_SEMANA']]
data_group = nn_data.groupby(by=['AÑO','MES_num', 'DIA', 'DIA_SEMANA', 'COMUNA', 'UNIDAD_ESPACIAL','TIPO_DELITO']).count().reset_index().sort_values(by=['TIPO_DELITO'])


data_delitos = pd.read_csv('data/NeuralNetworksData.csv', index_col=0)
model_data = data_delitos[data_delitos['AÑO'] >= 2019].copy()
model_data.drop(['AÑO'], axis=1, inplace=True)
model_data.rename(columns={'ACCESO CARNAL O ACTO SEXUAL ABUSIVO CON INCAPAZ DE RESISTIR': 'ACCESO CARNAL O ACTO SEXUAL ABUSIVO CON PERSONA EN INCAPACIDAD DE RESISTIR'}, inplace=True)


# Diccionario con todos las columnas de input = 0
tipo_delito = data_group['TIPO_DELITO'].unique()
area_espacial =data_group['UNIDAD_ESPACIAL'].unique()

model_input = model_data.drop(tipo_delito, axis=1).columns
model_output = model_data[tipo_delito].columns





predictions_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("Predicciones", className="card-title",
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
                                    label="Tipo de delito",
                                    tab_id="deadly-injuries-tab",
                                    labelClassName="tabs-font",
                                    activeLabelClassName="tabs-font-selected"),
                                dbc.Tab(
                                    label="Top delitos por comuna",
                                    tab_id="sexual-violence-tab",
                                    labelClassName="tabs-font",
                                    activeLabelClassName="tabs-font-selected"),
                            ],
                            id="tabs",
                            active_tab="deadly-injuries-tab",
                        ),
                        html.Div(id="tab-content"),
                    ], width=12,
                ),
            ]
        ),
    ],
    fluid=True
)

deadly_injuries_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Predicción de lesiones fatales", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label(applicationconstants.month_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-month",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=months
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.comuna_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-comuna",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in crime_df["COMUNA"].str.title().unique()
                                            ]
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.barrio_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-barrio",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in crime_df["BARRIO"].str.title().unique()
                                            ]
                                        ),
                                    ], width="2"),
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="predict-graph1", style={"height": "74%"}),
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="12"
                )
            ]
        )
    ],
    id="deadly-injuries-container",
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)

sexual_violence_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Predicción de violencia sexual", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label(applicationconstants.month_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-violence-month",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=months
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.crime_type_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-violence-delito",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in crime_df["TIPO_DELITO"].str.capitalize().unique()
                                            ]
                                        ),
                                    ], width="3"),
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="predict-graph1", style={"height": "74%"}),
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="12"
                )
            ]
        ),
    ],
    id="sexual-violence-container",
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    if active_tab is not None:
        if active_tab == "deadly-injuries-tab":
            return deadly_injuries_container
        elif active_tab == "sexual-violence-tab":
            return sexual_violence_container
    return deadly_injuries_container


def monthPrediction(mes, comuna, espacial):
  short_months = [2]
  medium_months = [4, 6, 9, 11]
  long_months = [1, 3, 5, 7, 8, 9, 10, 12]
  week_days = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']

  if mes in short_months:
    month_days = 28
  elif mes in medium_months:
    month_days = 30
  elif mes in long_months:
    month_days = 31
  else:
    return 'Invalid month input'


# Predecir casos para un mes y locacion en particular.
def monthPrediction(mes, comuna, espacial):
    model_input = model_data.drop(tipo_delito, axis=1).columns
    short_months = [2]
    medium_months = [4, 6, 9, 11]
    long_months = [1, 3, 5, 7, 8, 9, 10, 12]
    week_days = ['LUNES', 'MARTES', 'MIERCOLES', 'JUEVES', 'VIERNES', 'SABADO', 'DOMINGO']

    if mes in short_months:
        month_days = 28
    elif mes in medium_months:
        month_days = 30
    elif mes in long_months:
        month_days = 31
    else:
        return 'Invalid month input'

    # Arrays that will contain the predictions for the entire month.
    mes_df = []
    dia_df = []
    dia_semana_df = []
    comuna_df = []
    espacial_df = []

    sexual_abusivo = []
    sexual_incapacidad = []
    accesso_carnal = []
    carnal_violento = []
    acoso = []
    sexual_violento = []
    sexual_14 = []
    extorsion = []
    feminicidio = []
    homicidio = []
    homicidio_culposo = []
    hurto_abigeato = []
    hurto_automotores = []
    hurto_comerciales = []
    hurto_financieras = []
    hurto_motocicletas = []
    hurto = []
    hurto_pirateria = []
    hurto_residencias = []
    incapacidad = []
    lesiones_feto = []
    lesiones_culposas = []
    lesion_transito = []
    lesion_personales = []
    agravacion_personales = []
    pornografia = []
    secuestro_extorsivo = []
    secuestro = []
    communicacion_prostitucion = []
    violencia_familiar = []

    for i in range(month_days):
        # Obtaining dayweek.
        day_num = date(2021, mes, i + 1).weekday()
        day_week = week_days[day_num]

        # Base dictionary to create Dataframe for predictions.
        base = {}
        for e in range(len(model_input)):
            key = model_input[e]
            value = [0]
            base[key] = value

        # Adding input into dictionary for predictions.
        base['MES'] = [mes]
        base['DIA'] = [i]
        base[day_week] = [1]
        base[comuna] = [1]
        base[espacial] = [1]

        # Dataframe containing prediction of single day.
        data = pd.DataFrame(base)
        labels = np.array(data).reshape(1, -1)
        predictions = model.predict(labels)

        # Adding prediction to the predictions dictionary
        mes_df.append(mes)
        dia_df.append(i + 1)
        dia_semana_df.append(day_week)
        comuna_df.append(comuna)
        espacial_df.append(espacial)

        sexual_abusivo.append(predictions[0][0])
        sexual_incapacidad.append(predictions[0][1])
        accesso_carnal.append(predictions[0][2])
        carnal_violento.append(predictions[0][3])
        acoso.append(predictions[0][4])
        sexual_violento.append(predictions[0][5])
        sexual_14.append(predictions[0][6])
        extorsion.append(predictions[0][7])
        feminicidio.append(predictions[0][8])
        homicidio.append(predictions[0][9])
        homicidio_culposo.append(predictions[0][10])
        hurto_abigeato.append(predictions[0][11])
        hurto_automotores.append(predictions[0][12])
        hurto_comerciales.append(predictions[0][13])
        hurto_financieras.append(predictions[0][14])
        hurto_motocicletas.append(predictions[0][15])
        hurto.append(predictions[0][16])
        hurto_pirateria.append(predictions[0][17])
        hurto_residencias.append(predictions[0][18])
        incapacidad.append(predictions[0][19])
        lesiones_feto.append(predictions[0][20])
        lesiones_culposas.append(predictions[0][21])
        lesion_transito.append(predictions[0][22])
        lesion_personales.append(predictions[0][23])
        agravacion_personales.append(predictions[0][24])
        pornografia.append(predictions[0][25])
        secuestro_extorsivo.append(predictions[0][26])
        secuestro.append(predictions[0][27])
        communicacion_prostitucion.append(predictions[0][28])
        violencia_familiar.append(predictions[0][29])

    result = pd.DataFrame({
        'MES': mes_df,
        'DIA': dia_df,
        'DIA_SEMANA': dia_semana_df,
        'COMUNA': comuna_df,
        'UNIDAD_ESPACIAL': espacial_df,
        'ACCESO CARNAL ABUSIVO CON MENOR DE 14 AÑOS': sexual_abusivo,
        'ACCESO CARNAL O ACTO SEXUAL ABUSIVO CON PERSONA EN INCAPACIDAD DE RESISTIR': sexual_incapacidad,
        'ACCESO CARNAL O ACTO SEXUAL EN PERSONA PUESTA EN INCAPACIDAD DE RESISTIR': accesso_carnal,
        'ACCESO CARNAL VIOLENTO': carnal_violento,
        'ACOSO SEXUAL': acoso,
        'ACTO SEXUAL VIOLENTO': sexual_violento,
        'ACTOS SEXUALES CON MENOR DE 14 AÑOS': sexual_14,
        'EXTORSIÓN': extorsion,
        'FEMINICIDIO': feminicidio,
        'HOMICIDIO': homicidio,
        'HOMICIDIO CULPOSO (EN ACCIDENTE DE TRÁNSITO)': homicidio_culposo,
        'HURTO A ABIGEATO': hurto_abigeato,
        'HURTO A AUTOMOTORES': hurto_automotores,
        'HURTO A ENTIDADES COMERCIALES': hurto_comerciales,
        'HURTO A ENTIDADES FINANCIERAS': hurto_financieras,
        'HURTO A MOTOCICLETAS': hurto_motocicletas,
        'HURTO A PERSONAS': hurto,
        'HURTO A PIRATERÍA TERRESTRE': hurto_pirateria,
        'HURTO A RESIDENCIAS': hurto_residencias,
        'INCAPACIDAD PARA TRABAJAR O ENFERMEDAD': incapacidad,
        'LESIONES AL FETO': lesiones_feto,
        'LESIONES CULPOSAS': lesiones_culposas,
        'LESIONES CULPOSAS (EN ACCIDENTE DE TRANSITO)': lesion_transito,
        'LESIONES PERSONALES': lesion_personales,
        'LESIONES PERSONALES (CIRCUNSTANCIAS DE AGRAVACIÓN)': agravacion_personales,
        'PORNOGRAFÍA CON MENORES': pornografia,
        'SECUESTRO EXTORSIVO': secuestro_extorsivo,
        'SECUESTRO SIMPLE': secuestro,
        'UTILIZACIÓN O FACILITACIÓN DE MEDIOS DE COMUNICACIÓN PARA OFRECER SERVICIOS SEXUALES DE MENORES': communicacion_prostitucion,
        'VIOLENCIA INTRAFAMILIAR': violencia_familiar
    })
    return result


@app.callback(
    Output("sexviolence-graph", "figure"),
    [
     Input("predict-month", "value"),
     Input("predict-comuna", "value"),
     Input("predict-barrio", "value")
    ]
)
def plot_predictions(month, comuna, barrio):
    fig = go.Figure()
    if month is not None and comuna is not None and barrio is not None:
        month_pred = monthPrediction(month, comuna, barrio)
        tipo_delito_columns = month_pred.copy()
        tipo_delito_columns.drop(['DIA', 'MES', 'DIA_SEMANA', 'COMUNA', 'UNIDAD_ESPACIAL'], axis=1, inplace=True)
        tipo_delito = tipo_delito_columns.columns
        to_plot = {}
        for i in range(len(tipo_delito)):
            for e in range(len(month_pred)):
                if month_pred[tipo_delito[i]][e] > 0:
                    to_plot[tipo_delito[i]] = [1]
                    break
            else:
                to_plot[tipo_delito[i]] = [0]
        plot_df = pd.DataFrame(to_plot)
        for i in range(len(plot_df.columns)):
            if plot_df[plot_df.columns[i]][0] == 1:
                fig.add_trace(
                    go.Scatter(
                        x=month_pred['DIA'],
                        y=month_pred[plot_df.columns[i]],
                        mode='lines',
                        name=plot_df.columns[i].capitalize()
                    )
                )
    return fig