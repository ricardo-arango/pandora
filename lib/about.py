import dash_html_components as html
import dash_bootstrap_components as dbc


context_label_p1 = "En Colombia, el feminicidio y los delitos sexuales y de género han aumentado a tasas alarmantes durante la última década.  Según el Observatorio Colombiano de las Mujeres, en 2019 se reportaron 226 feminicidios, lo que representa un aumento de casi  el 296% en comparación con los casos reportados en 2016. De igual manera, los delitos sexuales han aumentado un 39% durante  el período 2007-2019, siendo las mujeres menores de edad las más afectadas. Este fenómeno ha llamado la atención de las  autoridades nacionales y locales, que realizan un esfuerzo constante para abordar los delitos en sus territorios mediante  el desarrollo de estrategias de mitigación."
context_label_p2 = "La Alcaldía de Bucaramanga ha notado patrones de delincuencia similares en la ciudad. Por ello, se interesa en identificar  a la población en mayor riesgo de ser víctima de feminicidio y delitos sexuales y de género y los factores socioeconómicos  que impulsan este tipo de delitos para diseñar potenciales estrategias de mitigación y determinar dónde sería más efectiva su  implementación."
problem_label = "Actualmente hay un número significativo de crímenes, incluyendo feminicidios y violencia de género en Bucaramanga. Las autoridades locales no cuentan con herramientas de análisis de datos que puedan identificar y predecir zonas espaciales y factores que hacen que ciertos grupos poblacionales sean vulnerables a estos crímenes. Debido a esto, diseñar e implementar planes de mitigación sigue ciendo una tarea compleja y desafiante."
importance_label = "Es crucial reducir las tasas de crimen para salvaguardar las vidas de los habitantes en las zonas rurales y urbanas de la ciudad, independientemente de la raza, género, orientación sexual o creencias religiosas al igual que mejorar la calidad de vida de las personas y la seguridad en Bucaramanga."
pandora_label_p1 = "Pandora es una herramienta de análisis de datos que representa de una manera visual, los datos obtenidos del repositorio de Datos Abiertos del Gobierno de Colombia, mostrando en diferentes tipos de gráficas el comportamiento de los crímenes en la ciudad desde Enero de 2010 hasta la última fecha de actualización de dichos datos."
pandora_label_p2 = "El panel de control inicial muestra de manera global datos de crímenes desde Enero de 2010, top de barrios con mayor cantidad de delitos cometidos, ubicación geográfica de dichos barrios, mapas de calor de densidad de crímenes y ubicación de estaciones de policía."
pandora_label_p3 = "La opción de violencia sexual se enfoca en mostrar los tipos de delitos relacionados con violencia y abuso sexual, desplegando mapas de calor que hacen fácil la identificación de puntos en donde están ocurriendo la mayor cantidad de estos crímenes y un mapa de la ciudad y sus zonas rurales cercanas en donde dichos delitos están ocurriendo."
pandora_label_p4 = "La opción de predicciones hace posible entender qué tipos de delitos van a ocurrir para un mes, comuna y barrios determinados. Esto es muy útil para que las autoridades diseñen y ejecuten planes de acción en dichos lugares."
pandora_label_p5 = "Herramientas es una opción en donde el usuario puede actualizar la base de datos del repositorio de Datos Abiertos del Gobierno de Colombia."





about_container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H3("Acerca de Pandora", className="card-title panel-title"),
                                html.Hr()
                        ])
                    ], width=12,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Contexto", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.P(context_label_p1, className="tools-notice"),
                                                    html.P(context_label_p2, className="tools-notice")
                                            ])
                                        ], width=12,
                                    ),
                                ], style={"padding": "0 16px 0 16px"})
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="12"
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Problema", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.H6(problem_label, className="tools-notice"),
                                            ])
                                        ], width=12,
                                    ),
                                ], style={"padding": "0 16px 0 16px"})
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="6"
                ),
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Importancia", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.P(importance_label, className="tools-notice"),
                                            ])
                                        ], width=12,
                                    ),
                                ], style={"padding": "0 16px 0 16px"})
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="6"
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.Div(
                            [
                                html.H5("Pandora", className="tile-title"),
                                html.Hr(),
                                dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    html.P(pandora_label_p1, className="tools-notice"),
                                                    html.Ul(
                                                        [
                                                            html.Li(pandora_label_p2, className="tools-notice"),
                                                            html.Li(pandora_label_p3, className="tools-notice"),
                                                            html.Li(pandora_label_p4, className="tools-notice"),
                                                            html.Li(pandora_label_p5, className="tools-notice"),
                                                        ]
                                                    )
                                            ])
                                        ], width=12,
                                    ),
                                ], style={"padding": "0 16px 0 16px"})
                            ],
                            className="panel-st-3"
                        )
                    ],
                    width="12"
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

