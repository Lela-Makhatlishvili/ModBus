use sys;
drop database if exists db_ModBus;
create database db_ModBus;
use db_ModBus;
CREATE TABLE t_device (
	id		int unsigned primary key auto_increment,
	dev_id		tinyint unsigned,
	dev_name	varchar(50)
);
CREATE TABLE t_temp (
	id		int unsigned primary key auto_increment,
	dev_id		tinyint unsigned,
	meaning		smallint,
	date_time	datetime
);
CREATE TABLE t_pressure (
	id		int unsigned primary key auto_increment,
	dev_id		tinyint unsigned,
	meaning		smallint,
	date_time	datetime
);
CREATE TABLE t_gas_co (
	id		int unsigned primary key auto_increment,
	dev_id		tinyint unsigned,
	meaning		smallint,
	date_time	datetime
);

CREATE TABLE `users` (
  id                    int NOT NULL AUTO_INCREMENT,
  username              varchar(255) NOT NULL,
  password              varchar(255) NOT NULL,
  )

