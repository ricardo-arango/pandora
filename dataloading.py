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
import numpy as np
import pandas as pd
import pandas.io.sql as psql
from geopy import distance
from geopandas.tools import sjoin
from sklearn.neighbors import BallTree
import psycopg2

# ################################################################################
# Declare and define global variables
# ################################################################################
global crime_df             # crime database
global police_stations_df   # police stationsdatabase
global barrio_geojson       # spatial units (polygons) in geojson format
global spunit_db            # crime_df field that contains name of spatial units
global spunit_js            # barrio_geojson field that contains name of spatial units

spunit_db = "UNIDAD_ESPACIAL"
spunit_js = "NOMBRE"

# ################################################################################
# Load and adjust default crime database (Jan 2010 - Feb 2021)
# ################################################################################
column_names = ['CRIMEN_ID', 'FECHA', 'AÑO', 'MES', 'MES_num', 'DIA', 'DIA_SEMANA','DIA_SEMANA_num', 'LATITUD', 'LONGITUD', 'ZONA', 'COMUNA', 'COMUNA_num','BARRIO', 'UNIDAD_ESPACIAL', 'TIPO_DELITO_ARTICULO', 'TIPO_DELITO','TIPO_CONDUCTA', 'TIPO_LESION', 'GENERO_VICTIMA', 'EDAD_VICTIMA','GRUPO_ETARIO_VICTIMA', 'GRUPO_ETARIO_VICTIMA_num','ESTADO_CIVIL_VICTIMA', 'MEDIO_TRANSPORTE_VICTIMA','MEDIO_TRANSPORTE_VICTIMARIO', 'TIPO_ARMA','DISTANCIA_ESTACION_POLICIA_CERCANA', 'ESTACION_POLICIA_CERCANA']
police_est_column_names = ['NOMBRE', 'LATITUD', 'LONGITUD']
dtypes = {"MES": "category",
          "DIA_SEMANA": "category",
          "ZONA": "category",
          "COMUNA": "category",
          "BARRIO": "category",
          spunit_db: "category",
          "TIPO_DELITO_ARTICULO": "category",
          "TIPO_DELITO": "category",
          "TIPO_CONDUCTA": "category",
          "TIPO_LESION": "category",
          "GENERO_VICTIMA": "category",
          "GRUPO_ETARIO_VICTIMA": "category",
          "GRUPO_ETARIO_VICTIMA_num": "int64",
          "ESTADO_CIVIL_VICTIMA": "category",
          "MEDIO_TRANSPORTE_VICTIMA": "category",
          "MEDIO_TRANSPORTE_VICTIMARIO": "category",
          "TIPO_ARMA": "category",
          "ESTACION_POLICIA_CERCANA": "category"}

# ################################################################################
# Load and adjust default crime database
# ################################################################################
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
    cases = cursor.fetchall()
    crime_df = pd.DataFrame(cases, columns=column_names)
    crime_df = crime_df.astype(dtypes)
    cursor.execute('select * from estacion_policia')
    police_est = cursor.fetchall()
    police_stations_df = pd.DataFrame(police_est, columns=police_est_column_names)
except (Exception, psycopg2.DatabaseError) as error:
    print("ERROR. Reading the data from the file then.")
    print(error)
    crime_df = pd.read_csv("data/2010-2021.csv", delimiter=",", encoding="utf-8", dtype=dtypes, parse_dates=["FECHA"])
    police_stations_df = pd.read_csv("data/estaciones-policia.csv", delimiter=",", encoding="utf-8")
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

# ################################################################################
# Load spatial data
# ################################################################################
barrio_geojson = geopandas.read_file("data/Barrio_Comuna_Corregimiento.geojson")
police_geojson = geopandas.read_file("data/Estaciones_policia.geojson")


# Code reserved for data loading and processing using user database
'''
# ################################################################################
# Load and adjust user crime database
# ################################################################################
dtypes = {"MES": "category",
          "DIA_SEMANA": "category",
          "ZONA": "category",
          "COMUNA": "category",
          "BARRIO": "category",
          "TIPO_DELITO_ARTICULO": "category",
          "TIPO_DELITO": "category",
          "TIPO_CONDUCTA": "category",
          "TIPO_LESION": "category",
          "GENERO_VICTIMA": "category",
          "GRUPO_ETARIO_VICTIMA": "category",
          "GRUPO_ETARIO_VICTIMA_num": "int64",
          "ESTADO_CIVIL_VICTIMA": "category",
          "MEDIO_TRANSPORTE_VICTIMA": "category",
          "MEDIO_TRANSPORTE_VICTIMARIO": "category",
          "TIPO_ARMA": "category"}
crime_df = pd.read_csv("data/2010-2021.csv", delimiter=",", encoding="utf-8", dtype=dtypes, parse_dates=["FECHA"])

# Adjust value order of several categorical fields
column_dtype = pd.api.types.CategoricalDtype(categories=['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE'], ordered=True)
crime_df["MES"] = crime_df["MES"].astype(column_dtype)
column_dtype = pd.api.types.CategoricalDtype(categories=['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES', 'SÁBADO', 'DOMINGO'], ordered=True)
crime_df["DIA_SEMANA"] = crime_df["DIA_SEMANA"].astype(column_dtype)
column_dtype = pd.api.types.CategoricalDtype(categories=['PRIMERA INFANCIA', 'INFANCIA', 'ADOLESCENCIA', 'JOVENES', 'ADULTEZ', 'PERSONA MAYOR', 'NO REPORTA'], ordered=True)
crime_df["GRUPO_ETARIO_VICTIMA"] = crime_df["GRUPO_ETARIO_VICTIMA"].astype(column_dtype)

# ################################################################################
# Join spatial units with crime database
# ################################################################################
barrio_geojson = geopandas.read_file("data/Barrio_Comuna_Corregimiento.geojson")

# Create spatial object (GeoDataFrame) using crime coordinates
crime_coordinates = geopandas.GeoDataFrame(crime_df[["CRIMEN_ID", "BARRIO", "COMUNA"]], crs='epsg:4326', geometry=geopandas.points_from_xy(crime_df.LONGITUD, crime_df.LATITUD))
crime_spunits = sjoin(crime_coordinates, barrio_geojson, how="left")
crime_df.loc[:, spunit_db] = np.nan
crime_df.loc[crime_spunits.sort_values(by="CRIMEN_ID")["CRIMEN_ID"]-1, spunit_db] = np.array(crime_spunits.sort_values(by="CRIMEN_ID").loc[:, spunit_js])

# ################################################################################
# Identify nearest police station to each crime in database
# ################################################################################
police_geojson = geopandas.read_file("data/Estaciones_policia.geojson")
tree = BallTree(police_geojson[['LATITUD', 'LONGITUD']].values, metric=lambda u, v: distance.distance(u, v).km)
distances, indices = tree.query(crime_df[['LATITUD', 'LONGITUD']].fillna(0).values, k = 1)
crime_df['DISTANCIA_ESTACION_POLICIA_CERCANA'] = distances
crime_df['ESTACION_POLICIA_CERCANA'] = np.array(police_geojson["NOMBRE"][np.concatenate(indices, axis=0)])

# Reorder dataframe columns
crime_df = crime_df[['CRIMEN_ID', 'FECHA', 'AÑO', 'MES', 'MES_num', 'DIA', 'DIA_SEMANA', 'DIA_SEMANA_num',
                     'LATITUD', 'LONGITUD', 'ZONA', 'COMUNA', 'COMUNA_num', 'BARRIO', spunit_db,
                     'TIPO_DELITO_ARTICULO', 'TIPO_DELITO', 'TIPO_CONDUCTA', 'TIPO_LESION',
                     'GENERO_VICTIMA', 'EDAD_VICTIMA', 'GRUPO_ETARIO_VICTIMA', 'GRUPO_ETARIO_VICTIMA_num',
                     'ESTADO_CIVIL_VICTIMA', 'MEDIO_TRANSPORTE_VICTIMA', 'MEDIO_TRANSPORTE_VICTIMARIO', 'TIPO_ARMA',
                     'DISTANCIA_ESTACION_POLICIA_CERCANA', 'ESTACION_POLICIA_CERCANA']]
'''