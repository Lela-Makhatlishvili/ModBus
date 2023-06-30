//
#pragma once
//
unsigned char
database_init(const char* p_user,const char* p_pass);
//
void
database_uninit();
//
unsigned char
database_call_proc(unsigned char proc,unsigned char dev_id, short meaning, unsigned char *p_result);
//
