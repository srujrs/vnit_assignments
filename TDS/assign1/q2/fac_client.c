/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "fac.h"


void
fac_prog_1(char *host, int n)
{
	CLIENT *clnt;
	int  *result_1;
	int  fac_1_arg;

#ifndef	DEBUG
	clnt = clnt_create (host, FAC_PROG, FAC_VERS, "udp");
	if (clnt == NULL) {
		clnt_pcreateerror (host);
		exit (1);
	}
#endif	/* DEBUG */
	fac_1_arg = n;
	result_1 = fac_1(&fac_1_arg, clnt);
	if (result_1 == (int *) NULL) {
		clnt_perror (clnt, "call failed");
	}
	else {
		printf("Result:%d\n", *result_1);
	}
#ifndef	DEBUG
	clnt_destroy (clnt);
#endif	 /* DEBUG */
}


int
main (int argc, char *argv[])
{
	char *host;

	if (argc < 3) {
		printf ("usage: %s server_host NUMBER\n", argv[0]);
		exit (1);
	}
	host = argv[1];
	fac_prog_1 (host, atoi(argv[2]));
exit (0);
}
