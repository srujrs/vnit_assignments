/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "chat.h"
#include <string.h>
#include <stdlib.h>

void
chat_prog_1(char *host, char* client_mssg)
{
	CLIENT *clnt;
	char * *result_1;
	char * chat_1_arg;

#ifndef	DEBUG
	clnt = clnt_create (host, CHAT_PROG, CHAT_VERS, "udp");
	if (clnt == NULL) {
		clnt_pcreateerror (host);
		exit (1);
	}
#endif	/* DEBUG */

	chat_1_arg = client_mssg;

	result_1 = chat_1(&chat_1_arg, clnt);
	if (result_1 == (char **) NULL) {
		clnt_perror (clnt, "call failed");
	}
	
	printf("Server said: %s\n",*result_1);
	
#ifndef	DEBUG
	clnt_destroy (clnt);
#endif	 /* DEBUG */
}


int
main (int argc, char *argv[])
{
	char *host;

	if (argc < 2) {
		printf ("usage: %s server_host\n", argv[0]);
		exit (1);
	}
	host = argv[1];
	char* mssg;

	printf("-----------------------------------------\n");
	printf("\tWelcome to the Chat!\n");
	printf("-----------------------------------------\n");

	while(1) {
		printf("Your mssg: ");

		size_t len = 0;
		ssize_t linesize = 0;

		linesize = getline(&mssg, &len, stdin);

		if(linesize <= 1) {
			printf("\tExiting chat!\n");
			break;
		} 
		else {
			mssg[linesize - 1] = '\0';
			chat_prog_1 (host, mssg);
		}
	}
	
exit (0);
}
