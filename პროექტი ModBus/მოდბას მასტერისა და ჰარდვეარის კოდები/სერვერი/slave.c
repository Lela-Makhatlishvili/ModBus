#include <stdio.h>
#include <netdb.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
//
#include "database.h"
//
static int i_socket = -1;
//
#define	ANALOG_OUT_COUNT	3
//
short AO[ANALOG_OUT_COUNT];
//
void* client_proc(void* param){
	//
	int i_client = (long)param;
	//
	while(1){
		char p_buff[1500];
		//
		ssize_t size = recv(i_client,p_buff,1500,0);
		if(size == -1){
			printf("recv failed...\n");
			break;
		}
		if(size == 0){
			
			printf("disconnect client\n");
			break;
		}
		//
		unsigned short t_id = ((unsigned short)p_buff[0] << 8) + p_buff[1];
		unsigned short m_len = ((unsigned short)p_buff[4] << 8) + p_buff[5];
		unsigned char dev_id = p_buff[6];
		unsigned char f_code = p_buff[7];
		unsigned short index = ((unsigned short)p_buff[8] << 8) + p_buff[9];
		unsigned short meaning = ((unsigned short)p_buff[10] << 8) + p_buff[11];
		//
		if(f_code == 0x06){
			if(index < ANALOG_OUT_COUNT){
				unsigned char res;
				AO[index] = meaning;
				database_call_proc(index+1,dev_id,meaning, &res);
			}
			else{
				p_buff[4] = 0;
				p_buff[5] = 3;
				p_buff[7] = p_buff[7] | 0x80;
				p_buff[8] = 0x02;
				size = 9;
			}
		}
		else{
			p_buff[4] = 0;
			p_buff[5] = 3;
			p_buff[7] = p_buff[7] | 0x80;
			p_buff[8] = 0x01;
			size = 9;
		}
		//
		if(send(i_client,p_buff,size,0) == -1){
			printf("send failed...\n");
			break;
		}
	}
	close(i_client);
	return 0;
}
//
void* connect_proc(void* param){
	//
	int i_socket = (long)param;
	//
	struct sockaddr_in cli;
	bzero(&cli, sizeof(cli));
	unsigned int len = sizeof(cli);
	//
	while(1){
		int i_client = accept(i_socket, (struct sockaddr*)&cli, &len);
		if (i_client == -1) {
			printf("accept failed...\n");
			break;
		}
		printf("server accept the client...\n");
		//
		pthread_t thread;
		if(pthread_create(&thread,0,client_proc,(void*)((long)i_client))){
			printf("run clent...\n");
			break;
		}
	}
	//
	close(i_socket);
	i_socket = -1;
	return 0;
}
//
int
slave_init(const char* p_user, const char* p_pass){
	//
	if(i_socket != -1){
		printf("bind failed\n");
		close(i_socket);
	}
	//
	i_socket = socket(AF_INET,SOCK_STREAM,0);
	if(i_socket == -1){
		fprintf(stderr,"socket creation failed\n");
		return 1;
	}
	printf("Socket successfully created..\n");
	//
	struct sockaddr_in servaddr;
	bzero(&servaddr, sizeof(servaddr));
	//
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = INADDR_ANY;
	servaddr.sin_port = htons(502);
	//
	if(bind(i_socket,(struct sockaddr*)&servaddr,sizeof(servaddr)) == -1){
		fprintf(stderr,"bind failed\n");
		close(i_socket);
		i_socket = -1;
		return 2;
	}
	printf("Socket successfully binded..\n");
	//
	if(listen(i_socket, 5) == -1) {
		fprintf(stderr,"Listen failed...\n");
		close(i_socket);
		i_socket = -1;
		return 3;
	}
	printf("Server listening..\n");
	//
	if(database_init(p_user, p_pass)){
		fprintf(stderr,"Listen failed...\n");
		close(i_socket);
		i_socket = -1;
		return 3;
	}
	//	
	pthread_t thread;
	if(pthread_create(&thread,0,connect_proc,(void*)((long)i_socket))){
		fprintf(stderr,"Listen failed...\n");
		close(i_socket);
		i_socket = -1;
		return 4;
	}
	//
	return 0;
}
//
void
slave_uninit(){
	if(i_socket != -1){
		close(i_socket);
		i_socket = -1;
	}
	database_uninit();
}
//

