create table equipo(
id numeric(8) primary key,
nombre varchar(30),
nro_trofeos int,
fecha_creacion date);
insert into equipo values(1234,'sktelecom',3,'2000-01-01'),
(123434,'fanatic',5,'2010-01-01'),
(172334,'sktelecom',2,'2011-01-01');
create table jugador(
ci numeric(8) primary key,
nombre varchar(30),
telefono int,
fecha_nacimiento date,
id_equipo numeric(8),
CONSTRAINT fk_jugador FOREIGN KEY (id_equipo)
REFERENCES equipo (id));
insert into equipo values(142434,'david',72423545,'2001-01-01'),
(12343744,'sergio',61928876,'2002-01-01'),
(17724334,'paola',73456735,'2003-01-01');
