//
#include <stdio.h>
//
#include "slave.h"
//
int main(){
	//
	int result = slave_init("username","password");
	if(result){
		return result;
	}
	//
	result = getchar();
	//
	slave_uninit();
	//
	return 0;
}

