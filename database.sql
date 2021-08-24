create table casos (
	CRIMEN_ID int not null,
	FECHA timestamp,
	AÑO int,
	MES varchar,
	MES_num int,
	DIA int,
	DIA_SEMANA varchar,
	DIA_SEMANA_num int,
	LATITUD decimal(10,7),
	LONGITUD decimal(10,7),
	ZONA varchar,
	COMUNA varchar,
	COMUNA_num decimal,
	BARRIO varchar,
	UNIDAD_ESPACIAL varchar,
	TIPO_DELITO_ARTICULO varchar,
	TIPO_DELITO varchar,
	TIPO_CONDUCTA varchar,
	TIPO_LESION varchar,
	GENERO_VICTIMA varchar,
	EDAD_VICTIMA int,
	GRUPO_ETARIO_VICTIMA varchar,
	GRUPO_ETARIO_VICTIMA_num int,
	ESTADO_CIVIL_VICTIMA varchar,
	MEDIO_TRANSPORTE_VICTIMA varchar,
	MEDIO_TRANSPORTE_VICTIMARIO varchar,
	TIPO_ARMA varchar,
	DISTANCIA_ESTACION_POLICIA_CERCANA decimal(15, 6),
	ESTACION_POLICIA_CERCANA varchar,
	PRIMARY KEY (CRIMEN_ID)
);

create table estacion_policia (
	NOMBRE varchar not null,
	LATITUD decimal(10,7),
	LONGITUD decimal(10,7),
	PRIMARY KEY (NOMBRE)
);

insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1522035, -73.1336676, 'CAI KENNEDY');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1134950, -73.1184010, 'CAI LA CONCORDIA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1461981, -73.1264620, 'CAI LA ESPERANZA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1108695, -73.1397951, 'CAI LA JOYA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.0978148, -73.1190803, 'CAI LA VICTORIA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1412614, -73.1331857, 'CAI LA VIRGEN');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1266400, -73.1100091, 'CAI LAS AMERICAS');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1259993, -73.1184014, 'CAI LOS NIÑOS');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1344503, -73.1044030, 'CAI MORRORICO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1002056, -73.1317421, 'CAI MUTIS');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.0990189, -73.1255525, 'CAI REAL DE MINAS');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1307333, -73.1136908, 'CAI SAN ALONSO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1309077, -73.1247316, 'CAI SAN FRANCISCO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1186108, -73.1091518, 'CAI SAN PIO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1178298, -73.1370937, 'CAI SANTANDER');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1164896, -73.1120825, 'CAI SOTOMAYOR');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.0884678, -73.1227788, 'CAI SUR');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.0882117, -73.1296600, 'CAI TERMINAL DE TRANSPORTE');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1127381, -73.1061993, 'CAI TERRAZAS');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.0965682, -73.1105181, 'CAI VIADUCTO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1286976, -73.1247962, 'COMANDO DE POLICIA SANTANDER');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1158761, -73.1287078, 'COMANDO METROPOLITANO DE POLICIA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1149380, -73.1295390, 'EFECTY CALLE 42 COMANDO DE POLICIA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1171147, -73.1250310, 'ESTACIÓN DE POLICÍA CENTRO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1043412, -73.1249094, 'ESTACIÓN DE POLICÍA SUR');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1405154, -73.1328911, 'ESTACIÓN POLICÍA NORTE');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values(7.1227501, -73.1192885, 'POLICIA SANTANDER SIC-SIP');