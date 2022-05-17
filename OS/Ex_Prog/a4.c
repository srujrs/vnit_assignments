#include <stdio.h>		// ---- Serial and parallel ----
#include <unistd.h>			// fork(), getpid(), exec
#include <sys/wait.h>		// wait()
#include <stdlib.h>			// exit()
#include <signal.h> 		// signal()

int main(){
	int rc1 = fork();
	
	if (rc1 < 0){			// fork failed; exit
		exit(0);
	}
	else if (rc1 == 0) {		// child (new) process 1
		char *execCommand[] = {"ls", NULL};
		execvp(execCommand[0], execCommand);
	} 
	else {              // parent process (rc holds child PID)
		int rc_wait1 = wait(NULL); 		// COMMENTING THIS WAIT WILL CHANGE THE EXECUTION FROM SERIAL TO PARALLEL
		printf("Parent PID:%d, Child1 pid:%d\n\n", getpid(), rc1);
		
		int rc2 = fork();
		
		if (rc2 < 0){			// fork failed; exit
			exit(0);
		}
		else if (rc2 == 0) {		// child (new) process 2
			char *execCommand[] = {"pwd", NULL};
			execvp(execCommand[0], execCommand);
		}
		else {              // parent process (rc holds child PID)
			int rc_wait2 = wait(NULL);
			
			printf("Parent PID:%d, Child2 pid:%d\n", getpid(), rc2);
		}
	}	
}

