#include <stdio.h>		// ------- SIGNALS --------
#include <unistd.h>			// fork(), getpid(), exec()
#include <sys/wait.h>		// wait()
#include <stdlib.h>			// exit()
#include <signal.h> 		// signal()
#include <fcntl.h>			// close(), open()

void handle_sigint(int signo)
{
	printf("Caught SIGINT signal...\n");
}

int main(){
	int rc;
	
	signal(SIGINT, SIG_IGN);	// Ignore SIGINT signal
	
	while(1)
	{
		rc = fork();
	
		if (rc < 0){			// fork failed; exit
			exit(0);
		}
		else if (rc == 0) {		// child (new) process
		
			signal(SIGINT, SIG_DFL);			// Restore the default behavior for SIGINT signal
			// signal(SIGINT, handle_sigint);	// This can be used to invoke a function instead of default behavior
			while(1)
			{
				printf("%d is child PID\n", getpid());
				sleep(5);
			}
		} 
		else {              // parent process (rc holds child PID)
			int rc_wait = wait(NULL);
			printf("Parent PID:%d, Child pid:%d\n\n", getpid(), rc);
		}
		
		sleep(5);
		
	}
}

