/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "fac.h"

int *
fac_1_svc(int *argp, struct svc_req *rqstp)
{
	static int  result;

	printf("factorial(%d) was called\n", *argp);
	int num = *argp;
	int temp_num, temp, sum_val;
	temp_num = num;
	sum_val = 0;
	result = 0;

	while(temp_num > 0) {
		temp = temp_num%10;
		sum_val += temp*temp*temp;
		temp_num = (int)temp_num/10;
	}

	if(sum_val == num) {
		result = 1;
	}

	// for(int i = n-1;i > 1;--i) result *= i;

	return &result;
}