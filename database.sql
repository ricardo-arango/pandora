create table casos (
	CRIMEN_ID int not null,
	FECHA timestamp,
	AÑO int,
	MES varchar,
	MES_num int,
	DIA int,
	DIA_SEMANA varchar,
	DIA_SEMANA_num int,
	LATITUD varchar,
	LONGITUD varchar,
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
	EDAD_VICTIMA decimal,
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
	LATITUD varchar,
	LONGITUD varchar,
	PRIMARY KEY (NOMBRE)
);

insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1164896', '-73.1120825', 'CAI SOTOMAYOR');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1286976', '-73.1247962', 'OFICINA ATENCIÓN AL CIUDADANO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.0990524', '-73.1255706', 'POLICIA NACIONAL REAL DE MINAS CAI');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1178298', '-73.1370937', 'CAI SANTANDER');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1186108', '-73.1091518', 'CAI SAN PIO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1224836', '-73.1339547', 'CAI GIRARDOT');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.12664',   '-73.1100091', 'CAI LAS AMERICAS');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1018035', '-73.1289482', 'ESTACIÓN POLICÍA SUR');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1013338', '-73.1407281', 'CAI CAMPO HERMOSO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1309077', '-73.1247316', 'CAI SAN FRANCISCO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1158761', '-73.1287078', 'COMANDO METROPOLITANO DE POLICIA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1221507', '-73.1251189', 'CAI CENTENARIO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.114938',  '-73.129539',    'EFECTY CALLE 42 COMANDO DE POLICIA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1231838', '-73.1250203', 'ESTACIÓN DE POLICÍA CENTRO');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1412614', '-73.1331857', 'CAI POLICE VIRGIN');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1036937', '-73.1264464', 'ESTACIÓN DE POLICIA SUR BUCARAMANGA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.0976464', '-73.113579',  'INSPECCIÓN DE POLICÍA BUCARAMANGA');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1461981', '-73.126462',  'CAI ESPERANZA I CUADRANTE 006');
insert into estacion_policia(LATITUD, LONGITUD, NOMBRE) values('7.1227501', '-73.1192885', 'SIJIN CRIMINAL INVESTIGATION BRANCH SANTANDER');