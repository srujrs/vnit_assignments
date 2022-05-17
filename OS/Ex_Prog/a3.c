#include <stdio.h>
#include <unistd.h>			// fork(), getpid(), exec()
#include <sys/wait.h>		// wait()
#include <stdlib.h>			// exit()
#include <signal.h> 		// signal()
#include <fcntl.h>			// close(), open()

int main(){
	int rc = fork();
	
	if (rc < 0){			// fork failed; exit
		exit(0);
	}
	else if (rc == 0) {		// child (new) process
		printf("%d is child PID\n", getpid());

		// ------- Redirecting STDOUT --------
		
		close(STDOUT_FILENO);
		open("output.txt", O_CREAT | O_WRONLY | O_APPEND);

		// -----------------------------------
		
		char *execCommand[] = {"ls", NULL};
		execvp(execCommand[0], execCommand);

	} 
	else {              // parent process (rc holds child PID)
		int rc_wait = wait(NULL);
		printf("%d is parent PID, %d is child pid\n", getpid(), rc);
	}
}
