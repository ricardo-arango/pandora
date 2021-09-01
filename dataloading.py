# ################################################################################
# Module      : dataloading.py
# Description : Load crime database and spatial data
#               Spatially join crime database with spatial units
#               Compute distances and identify nearest police station to crimes
# ################################################################################

# ################################################################################
# Load/invoke required libraries/modules
# ################################################################################
import geopandas
import pandas as pd
import psycopg2

from lib import applicationconstants
# ################################################################################
# Declare and define global variables
# ################################################################################
global crime_df             # crime database
global police_df            # police station database
global barrio_geojson       # spatial units (polygons) in geojson format

# ################################################################################
# Load spatial data
# ################################################################################
barrio_geojson = geopandas.read_file("data/Barrio_Comuna_Corregimiento.geojson")
police_geojson = geopandas.read_file("data/Estaciones_policia.geojson")

# ################################################################################
# Load and adjust default crime database (Jan 2010 - Feb 2021)
# ################################################################################
crime_df_columns = [
    applicationconstants.CRIMEN_ID, applicationconstants.FECHA, applicationconstants.AÑO, applicationconstants.MES, applicationconstants.MES_num,
    applicationconstants.DIA, applicationconstants.DIA_SEMANA, applicationconstants.DIA_SEMANA_num, applicationconstants.LATITUD, applicationconstants.LONGITUD,
    applicationconstants.ZONA, applicationconstants.COMUNA, applicationconstants.COMUNA_num, applicationconstants.BARRIO,
    applicationconstants.UNIDAD_ESPACIAL, applicationconstants.TIPO_DELITO_ARTICULO, applicationconstants.TIPO_DELITO,
    applicationconstants.TIPO_CONDUCTA, applicationconstants.TIPO_LESION, applicationconstants.GENERO_VICTIMA, applicationconstants.EDAD_VICTIMA,
    applicationconstants.GRUPO_ETARIO_VICTIMA, applicationconstants.GRUPO_ETARIO_VICTIMA_num, applicationconstants.ESTADO_CIVIL_VICTIMA,
    applicationconstants.MEDIO_TRANSPORTE_VICTIMA, applicationconstants.MEDIO_TRANSPORTE_VICTIMARIO, applicationconstants.TIPO_ARMA,
    applicationconstants.DISTANCIA_ESTACION_POLICIA_CERCANA, applicationconstants.ESTACION_POLICIA_CERCANA
]
police_df_columns = [applicationconstants.NOMBRE, applicationconstants.LATITUD, applicationconstants.LONGITUD]
months = [{"label": "Enero", "value": 1}, {"label": "Febrero", "value": 2}, {"label": "Marzo", "value": 3}, {"label": "Abril", "value": 4}, {"label": "Mayo", "value": 5}, {"label": "Junio", "value": 6}, {"label": "Julio", "value": 7}, {"label": "Agosto", "value": 8}, {"label": "Septiembre", "value": 9}, {"label": "Octubre", "value": 10}, {"label": "Noviembre", "value": 11}, {"label": "Diciembre", "value": 12}]

dtypes = {
    applicationconstants.CRIMEN_ID: "int64",
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
    applicationconstants.UNIDAD_ESPACIAL: "category",
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
    applicationconstants.TIPO_ARMA: "category",
    applicationconstants.DISTANCIA_ESTACION_POLICIA_CERCANA: "float64",
    applicationconstants.ESTACION_POLICIA_CERCANA: "category"
}

months_caps = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']
week_days_caps = ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO']
age_group_caps = ['PRIMERA INFANCIA', 'INFANCIA', 'ADOLESCENCIA', 'JOVENES', 'ADULTEZ', 'PERSONA MAYOR', 'NO REPORTA']

conn = None
try:
    # connect to the PostgreSQL server
    connection = psycopg2.connect(
        host="bucaramangadb.cx4nqzuqwvdx.us-east-1.rds.amazonaws.com",
        database="crimenes",
        user="dbadmin",
        password="rootadmin"
    )
    cursor = connection.cursor()
    cursor.execute('select * from casos')
    crime_df = pd.DataFrame(cursor.fetchall(), columns=crime_df_columns)
    crime_df = crime_df.astype(dtypes)
    cursor.execute('select * from estacion_policia')
    police_df = pd.DataFrame(cursor.fetchall(), columns=police_df_columns)
    print("Connection successful.")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error retrieving data from server: reading data from backup files.")
    print(error)
    crime_df = pd.read_csv("data/2010-2021.csv", delimiter=",", encoding="utf-8", dtype=dtypes, parse_dates=[applicationconstants.FECHA])
    police_df = pd.read_csv("data/Estaciones_policia.csv", delimiter=",", encoding="utf-8")
finally:
    if connection is not None:
        cursor.close()
        connection.close()

# Adjust value order of several categorical fields
column_dtype = pd.api.types.CategoricalDtype(categories=months_caps, ordered=True)
crime_df[applicationconstants.MES] = crime_df[applicationconstants.MES].astype(column_dtype)
column_dtype = pd.api.types.CategoricalDtype(categories=week_days_caps, ordered=True)
crime_df[applicationconstants.DIA_SEMANA] = crime_df[applicationconstants.DIA_SEMANA].astype(column_dtype)
column_dtype = pd.api.types.CategoricalDtype(categories=age_group_caps, ordered=True)
crime_df[applicationconstants.GRUPO_ETARIO_VICTIMA] = crime_df[applicationconstants.GRUPO_ETARIO_VICTIMA].astype(column_dtype)
print("Finishing adjusting categorical fields.")
