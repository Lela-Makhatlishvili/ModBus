//
#include <mysql.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
//
#include "database.h"
//
MYSQL *mysql = 0;
//
unsigned char
database_init(const char* p_user,const char* p_pass){
	if(mysql){
		mysql_close(mysql);
		mysql = NULL;
	}
	mysql = mysql_init(NULL);
	if(!mysql){
		fprintf(stderr, "%s\n", mysql_error(mysql));
		return 1;
	}
	//
	if(!mysql_real_connect(mysql, "localhost", "root", "123456789", "db_ModBus", 3306, NULL, 0)){
		fprintf(stderr, "Error: %s (errno: %d)\n", mysql_error(mysql), mysql_errno(mysql));
		mysql_close(mysql);
		return 2;
	}
	return 0;
}
//
void
database_uninit(){
	mysql_close(mysql);
	mysql = 0;
}
//
unsigned char
database_call_proc(unsigned char proc,unsigned char dev_id, short meaning, unsigned char *p_result){
	// initialize and prepare CALL statement with parameter placeholders.
	MYSQL_STMT *stmt = mysql_stmt_init(mysql);
	if (!stmt){
		fprintf(stderr, "Could not initialize statement\n");
		return 3;
	}
	//
	char buff[30];
	switch(proc){
	case 1:
		sprintf(buff,"call add_temp(?, ?, ?)");
		break;
	case 2:
		sprintf(buff,"call add_pressure(?, ?, ?)");
		break;
	case 3:
		sprintf(buff,"call add_gas_co(?, ?, ?)");
		break;
	default:
		mysql_stmt_close(stmt);
		return 3;
	}
	int status = mysql_stmt_prepare(stmt, buff, strlen(buff));
	if (status){
		fprintf(stderr, "Error: %s (errno: %d)\n", mysql_stmt_error(stmt), mysql_stmt_errno(stmt));
		mysql_stmt_close(stmt);
		return 4;
	}
	// initialize parameters: p_in, p_out, p_inout (all INT).
	bool	is_null[3];
	MYSQL_BIND ps_params[3];
	memset(ps_params, 0, sizeof (ps_params));
	
	unsigned char local_dev_id = dev_id;
	ps_params[0].buffer_type = MYSQL_TYPE_TINY;
	ps_params[0].buffer = (char *) &local_dev_id;
	ps_params[0].length = 0;
	ps_params[0].is_null = 0;
	
	short local_meaning = meaning;
	ps_params[1].buffer_type = MYSQL_TYPE_SHORT;
	ps_params[1].buffer = (char *) &local_meaning;
	ps_params[1].length = 0;
	ps_params[1].is_null = 0;
	
	unsigned char local_result = 0;
	ps_params[2].buffer_type = MYSQL_TYPE_TINY;
	ps_params[2].buffer = (char *) &local_result;
	ps_params[2].length = 0;
	ps_params[2].is_null = 0;

	// bind parameters
	status = mysql_stmt_bind_param(stmt, ps_params);
	if (status){
		fprintf(stderr, "Error: %s (errno: %d)\n", mysql_stmt_error(stmt), mysql_stmt_errno(stmt));
		mysql_stmt_close(stmt);
		return 5;
	}	
	// assign values to parameters and execute statement
	local_dev_id = dev_id;
	local_meaning = meaning;
	local_result = 0;
	
	status = mysql_stmt_execute(stmt);
	if (status){
		fprintf(stderr, "Error: %s (errno: %d)\n", mysql_stmt_error(stmt), mysql_stmt_errno(stmt));
		mysql_stmt_close(stmt);
		return 6;
	}
	// process results until there are no more
	int num_fields = mysql_stmt_field_count(stmt);
	if(num_fields != 1){
		fprintf(stderr, "Error: number fields");
		mysql_stmt_close(stmt);
		return 7;
	}
	MYSQL_RES *rs_metadata = mysql_stmt_result_metadata(stmt);
	if (!rs_metadata){
		fprintf(stderr, "Error: %s (errno: %d)\n", mysql_stmt_error(stmt), mysql_stmt_errno(stmt));
		mysql_stmt_close(stmt);
		return 8;
	}
	MYSQL_FIELD *fields = mysql_fetch_fields(rs_metadata);
	MYSQL_BIND *rs_bind = (MYSQL_BIND *) malloc(sizeof (MYSQL_BIND) * num_fields);
	if (!rs_bind) {
		fprintf(stderr, "Cannot allocate output buffers\n");
		mysql_free_result(rs_metadata);
		mysql_stmt_close(stmt);
		return 9;
	}
	memset(rs_bind, 0, sizeof (MYSQL_BIND) * num_fields);
	// set up and bind result set output buffers
	rs_bind[0].buffer_type = fields[0].type;
	rs_bind[0].is_null = &is_null[0];
	switch (fields[0].type) {
	case MYSQL_TYPE_TINY:
		rs_bind[0].buffer = (char *) &(dev_id);
		rs_bind[0].buffer_length = sizeof(dev_id);
		break;
	default:
		fprintf(stderr, "ERROR: unexpected type: %d.\n", fields[0].type);
		mysql_free_result(rs_metadata);
		free(rs_bind);
		mysql_stmt_close(stmt);
		return 10;
	}
	status = mysql_stmt_bind_result(stmt, rs_bind);
	if (status){
		fprintf(stderr, "Error: %s (errno: %d)\n", mysql_stmt_error(stmt), mysql_stmt_errno(stmt));
		mysql_free_result(rs_metadata);
		free(rs_bind);
		mysql_stmt_close(stmt);
		return 11;
	}
	// fetch and display result set rows
	while (1) {
		status = mysql_stmt_fetch(stmt);
		if (status == 1 || status == MYSQL_NO_DATA){
			break;
		}
		switch (rs_bind[0].buffer_type) {
			case MYSQL_TYPE_TINY:
				if (!*rs_bind[0].is_null){
					mysql_free_result(rs_metadata);
					free(rs_bind);
					mysql_stmt_close(stmt);
					return 12;
				}
				else{
					//printf("val[%d] = %u;\n", 0, *((unsigned char *) rs_bind[0].buffer));
					*p_result = *((unsigned char *) rs_bind[0].buffer);
				}
				break;
			default:
				printf("unexpected type (%d)\n", rs_bind[0].buffer_type);
				mysql_free_result(rs_metadata);
				free(rs_bind);
				mysql_stmt_close(stmt);
				return 12;
		}
	}
	mysql_free_result(rs_metadata);
	free(rs_bind);
	// more results? -1 = no, >0 = error, 0 = yes (keep looking)
	status = mysql_stmt_next_result(stmt);
	if (status > 0){
		fprintf(stderr, "Error: %s (errno: %d)\n", mysql_stmt_error(stmt), mysql_stmt_errno(stmt));
		mysql_stmt_close(stmt);
		return 12;
	}
	//
	mysql_stmt_close(stmt);
	return 0;
}
//

