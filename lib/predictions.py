import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import joblib
import plotly.express as px

from dataloading import months
from app import app
from datetime import date
from dash.dependencies import Input, Output
from lib import applicationconstants
from tensorflow.keras import models


raw_data = pd.read_csv('data/2010-2021.csv')

#Neural Network
model = models.load_model('data/Neural_net_Mintic.h5')
model_data = pd.read_csv('data/NeuralNetworksData.csv', index_col=0)
raw_data[applicationconstants.TIPO_DELITO].replace({'NO REPORTA': np.nan}, inplace=True)
raw_data.dropna(inplace=True)
tipo_delito = raw_data[applicationconstants.TIPO_DELITO].str.strip().unique()
model_input = model_data.drop(tipo_delito, axis=1).columns

# Tree
forest_train = pd.read_csv('data/forestTrain.csv', index_col=0)
rf = joblib.load('data/DelitosRandomForestModel')

# Variables used in functions.
genero = pd.get_dummies(forest_train[applicationconstants.GENERO_VICTIMA])
edad = pd.get_dummies(forest_train[applicationconstants.EDAD_VICTIMA])
comuna = pd.get_dummies(forest_train[applicationconstants.COMUNA])
espacial = pd.get_dummies(forest_train[applicationconstants.UNIDAD_ESPACIAL])
forest_data = pd.concat([forest_train, genero, edad, comuna, espacial], axis=1)
forest_data.drop([applicationconstants.GENERO_VICTIMA, applicationconstants.EDAD_VICTIMA, applicationconstants.COMUNA, applicationconstants.UNIDAD_ESPACIAL, 'VICTIMA_POINT'], axis=1, inplace=True)



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
                                    label="Predicción de delito",
                                    tab_id="injury-type-tab",
                                    labelClassName="tabs-font",
                                    activeLabelClassName="tabs-font-selected"),
                                dbc.Tab(
                                    label="Ocurrencia de delito",
                                    tab_id="crime-type-prob-tab",
                                    labelClassName="tabs-font",
                                    activeLabelClassName="tabs-font-selected"),
                            ],
                            id="tabs",
                            active_tab="injury-type-tab",
                        ),
                        html.Div(id="tab-content"),
                    ], width=12,
                ),
            ]
        ),
    ],
    fluid=True
)

injury_type_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Predicción de tipos de delito", className="tile-title"),
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
                                        ),
                                    ], width="4"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.barrio_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="predict-barrio",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                        ),
                                    ], width="4"),
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="predictions-graph", style={"height": "74%"}),
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="12"
                )
            ]
        )
    ],
    id="predictions_container",
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)

crime_probability_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Probabilidad de ocurrencia de delito", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col([
                                        dbc.Label(applicationconstants.gender_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="prob-gender",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in raw_data[applicationconstants.GENERO_VICTIMA].astype('str').str.capitalize().unique()
                                            ]
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.age_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="prob-age",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in range(1, 111)
                                            ]
                                        ),
                                    ], width="2"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.comuna_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="prob-comuna",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in raw_data[applicationconstants.COMUNA].astype('str').str.capitalize().unique()
                                            ]
                                        ),
                                    ], width="4"),
                                    dbc.Col([
                                        dbc.Label(applicationconstants.barrio_label, className="labels-font labels-margin"),
                                        dcc.Dropdown(
                                            id="prob-barrio",
                                            placeholder=applicationconstants.dropdown_placeholder,
                                            options=[
                                                {"label": col, "value": col} for col in raw_data[applicationconstants.UNIDAD_ESPACIAL].astype('str').str.capitalize().unique()
                                            ]
                                        ),
                                    ], width="4"),
                                ], style={"padding": "0 16px 0 16px"}),
                                dcc.Graph(id="prob-graph", style={"height": "74%"}),
                            ], className="panel-st-3"),
                    ],
                    width="12"
                )
            ],
        )
    ],
    id="crime-probability-container",
    fluid=True,
    style={
        "width": "100%",
        "background": "#f8f9fa"
    }
)


@app.callback(
    Output("predict-comuna", "options"),
    Input("predict-barrio", "value"),
)
def filter_comunas_by_barrio_predictions(barrio):
    if barrio is not None:
        barrio_by_comuna = raw_data[raw_data[applicationconstants.UNIDAD_ESPACIAL] == barrio.upper()][applicationconstants.COMUNA]
        return [
            {"label": col, "value": col} for col in barrio_by_comuna.astype('str').str.capitalize().unique()
        ]
    return [
        {"label": col, "value": col} for col in raw_data[applicationconstants.COMUNA].astype('str').str.capitalize().unique()
    ]


@app.callback(
    Output("predict-barrio", "options"),
    Input("predict-comuna", "value"),
)
def filter_barrioss_by_comuna_predictions(comuna):
    if comuna is not None:
        barrio_by_comuna = raw_data[raw_data[applicationconstants.COMUNA] == comuna.upper()][applicationconstants.UNIDAD_ESPACIAL]
        return [
            {"label": col, "value": col} for col in barrio_by_comuna.astype('str').str.capitalize().unique()
        ]
    return [
        {"label": col, "value": col} for col in raw_data[applicationconstants.UNIDAD_ESPACIAL].astype('str').str.capitalize().unique()
    ]


@app.callback(
    Output("prob-comuna", "options"),
    Input("prob-barrio", "value"),
)
def filter_comunas_by_barrio_probability(barrio):
    if barrio is not None:
        barrio_by_comuna = raw_data[raw_data[applicationconstants.UNIDAD_ESPACIAL] == barrio.upper()][applicationconstants.COMUNA]
        return [
            {"label": col, "value": col} for col in barrio_by_comuna.astype('str').str.capitalize().unique()
        ]
    return [
        {"label": col, "value": col} for col in raw_data[applicationconstants.COMUNA].astype('str').str.capitalize().unique()
    ]


@app.callback(
    Output("prob-barrio", "options"),
    Input("prob-comuna", "value"),
)
def filter_barrioss_by_comuna_probability(comuna):
    if comuna is not None:
        barrio_by_comuna = raw_data[raw_data[applicationconstants.COMUNA] == comuna.upper()][applicationconstants.UNIDAD_ESPACIAL]
        return [
            {"label": col, "value": col} for col in barrio_by_comuna.astype('str').str.capitalize().unique()
        ]
    return [
        {"label": col, "value": col} for col in raw_data[applicationconstants.UNIDAD_ESPACIAL].astype('str').str.capitalize().unique()
    ]



@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    if active_tab is not None:
        if active_tab == "injury-type-tab":
            return injury_type_container
        elif active_tab == "crime-type-prob-tab":
            return crime_probability_container
    return injury_type_container


# Predecir casos para un mes y locacion en particular.
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
        applicationconstants.COMUNA: comuna_df,
        applicationconstants.UNIDAD_ESPACIAL: espacial_df,
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
    Output("predictions-graph", "figure"),
    [
     Input("predict-month", "value"),
     Input("predict-comuna", "value"),
     Input("predict-barrio", "value")
    ]
)
def plot_predictions(month, comuna, barrio):
    fig = go.Figure()
    if month is not None and comuna is not None and barrio is not None:
        date_month = date(2021, month, 1).strftime("%B")
        month_pred = monthPrediction(month, comuna.upper(), barrio.upper())
        to_plot = {}
        for i in range(len(tipo_delito)):
            for e in range(len(month_pred)):
                if month_pred[tipo_delito[i]][e] > 0.1:
                    to_plot[tipo_delito[i]] = [1]
                    break
            else:
                to_plot[tipo_delito[i]] = [0]

        plot_df = pd.DataFrame(to_plot)
        for i in range(len(plot_df.columns)):
            if plot_df[plot_df.columns[i]][0] == 1:
                fig.add_trace(go.Scatter(x=month_pred['DIA'], y=month_pred[plot_df.columns[i]],
                                         mode='lines',
                                         name=plot_df.columns[i].capitalize()))

        # Edit the layout
        fig.update_layout(
            xaxis_title='Día del mes',
            yaxis_title='Casos',
            font_family="revert",
            font_color="#5f5f5f",
            paper_bgcolor="white"
        )
    return fig


def random_forest_probability(genero, edad, comuna, espacial):
    tipo_delito = ['HURTO A ENTIDADES COMERCIALES', 'HURTO A PERSONAS',
                   'LESIONES CULPOSAS (EN ACCIDENTE DE TRANSITO)', 'HURTO A RESIDENCIAS',
                   'LESIONES PERSONALES', 'HURTO A MOTOCICLETAS',
                   'HOMICIDIO CULPOSO (EN ACCIDENTE DE TRÁNSITO)', 'EXTORSIÓN',
                   'VIOLENCIA INTRAFAMILIAR', 'HOMICIDIO', 'HURTO A AUTOMOTORES',
                   'LESIONES CULPOSAS', 'ACTO SEXUAL VIOLENTO', 'ACCESO CARNAL VIOLENTO',
                   'ACCESO CARNAL O ACTO SEXUAL EN PERSONA PUESTA EN INCAPACIDAD DE RESISTIR',
                   'FEMINICIDIO', 'HURTO A ABIGEATO',
                   'ACTOS SEXUALES CON MENOR DE 14 AÑOS',
                   'ACCESO CARNAL O ACTO SEXUAL ABUSIVO CON PERSONA EN INCAPACIDAD DE RESISTIR',
                   'LESIONES PERSONALES (CIRCUNSTANCIAS DE AGRAVACIÓN)',
                   'ACCESO CARNAL ABUSIVO CON MENOR DE 14 AÑOS', 'ACOSO SEXUAL',
                   'UTILIZACIÓN O FACILITACIÓN DE MEDIOS DE COMUNICACIÓN PARA OFRECER SERVICIOS SEXUALES DE MENORES',
                   'PORNOGRAFÍA CON MENORES']

    data = forest_data.drop(tipo_delito, axis=1)
    data_dt = data.loc[0].copy()
    data_dt.iloc[:] = np.zeros(369)
    data_dt[genero] = 1
    data_dt[edad] = 1
    data_dt[comuna] = 1
    data_dt[espacial] = 1

    prediction = rf.predict(np.array(data_dt).reshape(1, -1))
    predictions = {applicationconstants.TIPO_DELITO: tipo_delito, 'PROBABILIDAD': prediction[0]}
    predictions_df = pd.DataFrame(predictions)
    predictions_df['PROBABILIDAD'].replace({0: np.nan}, inplace=True)
    predictions_df.dropna(inplace=True)
    return predictions_df


@app.callback(
    Output("prob-graph", "figure"),
    [
        Input("prob-gender", "value"),
        Input("prob-age", "value"),
        Input("prob-comuna", "value"),
        Input("prob-barrio", "value")
    ]
)
def plot_prob_bar(gender, age, comuna, barrio):
    fig = go.Figure()
    if gender is not None and age is not None and comuna is not None and barrio is not None:
        df = random_forest_probability(gender.upper(), age, comuna.upper(), barrio.upper())
        df.loc[:, applicationconstants.TIPO_DELITO] = df[applicationconstants.TIPO_DELITO].str.capitalize()
        fig = px.bar(
            df.sort_values(by="PROBABILIDAD", ascending=False),
            x=applicationconstants.TIPO_DELITO,
            y='PROBABILIDAD',
            color='PROBABILIDAD',
            color_continuous_scale=px.colors.sequential.Blues,
            labels={'PROBABILIDAD': '% Probabilidad', applicationconstants.TIPO_DELITO: 'Tipo de delito'}
        )
        fig.update_traces(
            marker_line_color='rgb(8,48,107)',
            marker_line_width=0.2,
            opacity=0.8)
        fig.update_layout(
            font_family="revert",
            font_color="#5f5f5f",
            paper_bgcolor="white",
            xaxis_tickangle=45
        )
    return fig