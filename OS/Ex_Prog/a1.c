#include <stdio.h>
#include <unistd.h>			// fork(), getpid(), exec
#include <sys/wait.h>		// wait()
#include <stdlib.h>			// exit()
#include <signal.h> 		// signal()

int main(){
	int rc = fork();
	
	if (rc < 0){			// fork failed; exit
		exit(0);
	}
	else if (rc == 0) {		// child (new) process
		printf("%d is child PID\n", getpid());
	} 
	else {              // parent process (rc holds child PID)
		int rc_wait = wait(NULL);
		printf("%d is parent PID, %d is child pid\n", getpid(), rc);
	}
}

