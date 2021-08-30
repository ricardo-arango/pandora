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
import pandas.io.sql as psql
import psycopg2

# ################################################################################
# Declare and define global variables
# ################################################################################
global crime_df             # crime database
global police_df            # police station database
global barrio_geojson       # spatial units (polygons) in geojson format
global spunit_db            # crime_df field that contains name of spatial units
global spunit_js            # barrio_geojson field that contains name of spatial units

spunit_db = "UNIDAD_ESPACIAL"
spunit_js = "NOMBRE"

# ################################################################################
# Load spatial data
# ################################################################################
barrio_geojson = geopandas.read_file("data/Barrio_Comuna_Corregimiento.geojson")
police_geojson = geopandas.read_file("data/Estaciones_policia.geojson")

# ################################################################################
# Load and adjust default crime database (Jan 2010 - Feb 2021)
# ################################################################################
crime_df_columns = ['CRIMEN_ID', 'FECHA', 'AÑO', 'MES', 'MES_num', 'DIA', 'DIA_SEMANA', 'DIA_SEMANA_num', 'LATITUD', 'LONGITUD', 'ZONA', 'COMUNA', 'COMUNA_num', 'BARRIO', 'UNIDAD_ESPACIAL', 'TIPO_DELITO_ARTICULO', 'TIPO_DELITO', 'TIPO_CONDUCTA', 'TIPO_LESION', 'GENERO_VICTIMA', 'EDAD_VICTIMA', 'GRUPO_ETARIO_VICTIMA', 'GRUPO_ETARIO_VICTIMA_num', 'ESTADO_CIVIL_VICTIMA', 'MEDIO_TRANSPORTE_VICTIMA', 'MEDIO_TRANSPORTE_VICTIMARIO', 'TIPO_ARMA', 'DISTANCIA_ESTACION_POLICIA_CERCANA', 'ESTACION_POLICIA_CERCANA']
police_df_columns = ['NOMBRE', 'LATITUD', 'LONGITUD']
months = [{"label": "Enero", "value": 1}, {"label": "Febrero", "value": 2}, {"label": "Marzo", "value": 3}, {"label": "Abril", "value": 4}, {"label": "Mayo", "value": 5}, {"label": "Junio", "value": 6}, {"label": "Julio", "value": 7}, {"label": "Agosto", "value": 8}, {"label": "Septiembre", "value": 9}, {"label": "Octubre", "value": 10}, {"label": "Noviembre", "value": 11}, {"label": "Diciembre", "value": 12}]

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
              "UNIDAD_ESPACIAL": "category",
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
              "TIPO_ARMA": "category",
              "DISTANCIA_ESTACION_POLICIA_CERCANA": "float64",
              "ESTACION_POLICIA_CERCANA": "category"}

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
    print("Connection successful******************")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error retrieving data from server: reading data from backup files.")
    print(error)
    crime_df = pd.read_csv("data/2010-2021.csv", delimiter=",", encoding="utf-8", dtype=dtypes, parse_dates=["FECHA"])
    police_df = pd.read_csv("data/Estaciones_policia.csv", delimiter=",", encoding="utf-8")
finally:
    if connection is not None:
        cursor.close()
        connection.close()

# Adjust value order of several categorical fields
column_dtype = pd.api.types.CategoricalDtype(categories=['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE'], ordered=True)
crime_df["MES"] = crime_df["MES"].astype(column_dtype)
column_dtype = pd.api.types.CategoricalDtype(categories=['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO'], ordered=True)
crime_df["DIA_SEMANA"] = crime_df["DIA_SEMANA"].astype(column_dtype)
column_dtype = pd.api.types.CategoricalDtype(categories=['PRIMERA INFANCIA', 'INFANCIA', 'ADOLESCENCIA', 'JOVENES', 'ADULTEZ', 'PERSONA MAYOR', 'NO REPORTA'], ordered=True)
crime_df["GRUPO_ETARIO_VICTIMA"] = crime_df["GRUPO_ETARIO_VICTIMA"].astype(column_dtype)
print("Finishing adjusting categorical fields******************")