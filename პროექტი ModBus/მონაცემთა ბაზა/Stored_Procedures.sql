use db_ModBus;



delimiter //
create procedure add_device(
	in	param_dev_id	tinyint unsigned,
	in	param_dev_name	varchar(50),
	out	param_result	tinyint unsigned
)
begin
	declare local_count tinyint unsigned;
	set local_count = (select count(*) from t_device where dev_id = param_dev_id);
	if local_count = 0 then
		insert into t_device(dev_id,dev_name) values(param_dev_id, param_dev_name);
		set param_result = 0;
	else
		set param_result = 1;
	end if;
end //

create procedure add_temp(
	in	param_dev_id	tinyint unsigned,
	in	param_meaning	smallint,
	out	param_result	tinyint unsigned
)
begin
	declare local_count tinyint unsigned;
	set local_count = (select count(*) from t_device where dev_id = param_dev_id);
	if local_count = 0 then
		set param_result = 1;
	else
		insert into t_temp(dev_id, meaning, date_time)values(param_dev_id, param_meaning, now());
		set param_result = 0;
	end if;
end //

create procedure add_humidity(
	in	param_dev_id	tinyint unsigned,
	in	param_meaning	smallint,
	out	param_result	tinyint unsigned
)
begin
	declare local_count tinyint unsigned;
	set local_count = (select count(*) from t_device where dev_id = param_dev_id);
	if local_count = 0 then
		set param_result = 1;
	else
		insert into t_humidity(dev_id, meaning, date_time)values(param_dev_id, param_meaning, now());
		set param_result = 0;
	end if;
end //

create procedure add_gas_co(
	in	param_dev_id	tinyint unsigned,
	in	param_meaning	smallint,
	out	param_result	tinyint unsigned
)
begin
	declare local_count tinyint unsigned;
	set local_count = (select count(*) from t_device where dev_id = param_dev_id);
	if local_count = 0 then
		set param_result = 1;
	else
		insert into t_gas_co(dev_id, meaning, date_time)values(param_dev_id, param_meaning, now());
		set param_result = 0;
	end if;
end //

delimiter ;



CREATE PROCEDURE `search_gas_co_data`(
    IN param_sensor_id TINYINT UNSIGNED,
    IN param_date_time DATETIME
)
BEGIN
    DECLARE local_gas_co_data SMALLINT;
    
    IF param_sensor_id IS NULL THEN
        SELECT 'Invalid sensor ID.' AS gas_co_result;
    ELSE
        SELECT meaning INTO local_gas_co_data FROM t_gas_co
        WHERE dev_id = param_sensor_id AND date_time = param_date_time;
        
        IF local_gas_co_data IS NULL THEN
            SELECT 'მონაცემი არ მოიძებნა' AS gas_co_result;
        ELSE
            SELECT local_gas_co_data AS gas_co_result;
        END IF;
    END IF;
END //



CREATE  PROCEDURE `search_pressure_data`(
    IN param_sensor_id TINYINT UNSIGNED,
    IN param_date_time DATETIME
)
BEGIN
    DECLARE local_pressure_data SMALLINT;
    
    IF param_sensor_id IS NULL THEN
        SELECT 'Invalid sensor ID.' AS  pressure_result;
    ELSE
        SELECT meaning INTO local_pressure_data FROM  t_pressure
        WHERE dev_id = param_sensor_id AND date_time = param_date_time;
        
        IF local_pressure_data IS NULL THEN
            SELECT 'მონაცემი არ მოიძებნა' AS  pressure_result;
        ELSE
            SELECT local_pressure_data AS  pressure_result;
        END IF;
    END IF;
END //


CREATE PROCEDURE `search_temp_data`(
    IN param_sensor_id TINYINT UNSIGNED,
    IN param_date_time DATETIME
)
BEGIN
    DECLARE local_temp_data SMALLINT;
    
    IF param_sensor_id IS NULL THEN
        SELECT 'Invalid sensor ID.' AS  temp_result;
    ELSE
        SELECT meaning INTO local_temp_data FROM  t_temp
        WHERE dev_id = param_sensor_id AND date_time = param_date_time;
        
        IF local_temp_data IS NULL THEN
            SELECT 'მონაცემი არ მოიძებნა' AS  temp_result;
        ELSE
            SELECT local_temp_data AS  temp_result;
        END IF;
    END IF;
END //

