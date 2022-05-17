#include <stdio.h>
#include <string.h>         // strcmp(), strcpy()
#include <stdlib.h>			// exit()
#include <unistd.h>			// fork(), getpid(), exec()
#include <sys/wait.h>		// wait()
#include <signal.h>			// signal()
#include <fcntl.h>			// close(), open()

void handle_sigint(int signo)
{
    // this function is for handling signals in child process
	exit(0);
}

char** parseInput(char* string,int* choice,int* numOfArgs)
{
	// This function will parse the input string into multiple commands or a single command with arguments depending on the delimiter (&&, ##, >, or spaces).
    int size = 1;
    for(int i = 1;i < strlen(string);++i)
        if(*(string + i) == 32) size += 1;
    
    char** parsedArgs = (char**)malloc(size*sizeof(char*));
    char *delimiter = " ";
    char *word;
    int length = 0;

    // Splits inputString.
    word = strtok(string, delimiter);
    while (word != NULL)
    {
        parsedArgs[length] = word;  // Storing separated words in parsedArgs array.
        word = strtok(NULL, delimiter);
        length += 1;
    }
            
    parsedArgs[size - 1][strlen(parsedArgs[size - 1]) - 1] = '\0'; // removing new line character read at the end

    char* exit = "exit"; 
    char* found0 = "&&";       // different types special commands or delimiters
    char* found1 = "##";
    char* found2 = ">";

    // detecting the type of command, choice pointer stores the type of command

    if(strcmp(parsedArgs[0],exit) == 0 && size == 1) // exit command
        *choice =  -1;

    for(int i = 0;i < size;++i) {
        if(strcmp(parsedArgs[i],found0) == 0) { // parallel execution
            *choice =  0;
            break;
        }
        else if(strcmp(parsedArgs[i],found1) == 0) { // sequential execution
            *choice =  1;
            break;
        }  
        else if(strcmp(parsedArgs[i],found2) == 0) { // output redirection
            *choice =  2;
            break;
        }
    }
    *numOfArgs = size;
    return parsedArgs; // sending back split arguments
}

void executeCommand(char** execCommand,int size)
{   
    // check and execute for cd command
    if(strcmp(execCommand[0],"cd") == 0){
        if(size == 2) {
            if(chdir(execCommand[1]) != 0) // checking for successful run of command
                printf("cd: %s: No such file or directory\n",execCommand[1]);
        }
    }
    else {
        // This function will fork a new process to execute a command

        execCommand = (char**)realloc(execCommand,size + 1); // adding NULL at the end for the execvp command
        execCommand[size] = NULL;

        int rc = fork();
        
        if (rc < 0){			// fork failed; exit
            exit(0);
        }
        else if (rc == 0) {		// child (new) process
            signal(SIGINT, handle_sigint);

            // -------- EXEC system call ---------

            int retval = execvp(execCommand[0], execCommand);
            if(retval < 0) {
                printf("Shell: Incorrect command\n");
                exit(0);
            }
            
            // -----------------------------------
        } 
        else {              // parent process (rc holds child PID)
            int rc_wait = wait(NULL); // parent waits till child finishes
        }
    }
}

void executeParallelCommands(char** execCommands,int size)
{
	// This function will run multiple commands in parallel

    char** tempCommands = malloc(10*sizeof(char*)); // array to hold individual commands
    for(int i =0;i < 10;++i)
        tempCommands[i] = malloc(10*sizeof(char));

    // getting individual commands between the delimiter
    int i = 0,start = 0,j;
    while(i < size) {
        j = 0;
        for(i = start;i < size;++i) {
            if(strcmp(execCommands[i],"&&") == 0) {
                tempCommands[j] = NULL;
                start = i + 1;
                break;
            } else {
                strcpy(tempCommands[j],execCommands[i]);
                j += 1;
            }
        }
        tempCommands[j] = NULL;
        // executing the commands that we separated individually
        if(strcmp(tempCommands[0],"cd") == 0){
            if(chdir(tempCommands[1]) != 0)
                printf("cd: %s: No such file or directory\n",tempCommands[1]);
        } else {
            int rc = fork();
        
            if (rc < 0){			// fork failed; exit
                exit(0);
            }
            else if (rc == 0) {		// child (new) process
                signal(SIGINT, handle_sigint);

                // -------- EXEC system call ---------

                int retval = execvp(tempCommands[0], tempCommands);
                if(retval < 0) {
                    printf("Shell: Incorrect command\n");
                    exit(0);
                }
                
                // -----------------------------------
            }
        }
    }
}

void executeSequentialCommands(char** execCommands,int size)
{	
	// This function will run multiple commands in sequence

    // loop till all individual commands are not executed one by one
    int i = 0,start = 0,j;
    while(i < size) {
        j = 0;
        char** tempCommands = malloc(10*sizeof(char*)); // array to hold individual commands
        for(int i =0;i < 10;++i)
            tempCommands[i] = malloc(10*sizeof(char));

        // getting individual commands between the delimiter
        for(i = start;i < size;++i) {
            if(strcmp(execCommands[i],"##") == 0) {
                start = i + 1;
                break;
            } else {
                strcpy(tempCommands[j],execCommands[i]);
                j += 1;
            }
        }
        executeCommand(tempCommands,j);
	}
}

void executeCommandRedirection(char** execCommands,int size)
{
	// This function will run a single command with output redirected to an output file specificed by user

    char** tempCommands = malloc(10*sizeof(char*)); // array to hold individual commands
    for(int i =0;i < 10;++i)
        tempCommands[i] = malloc(10*sizeof(char));

    int i = 0,j = 0;
    for(i = 0;i < size;++i) {
        if(strcmp(execCommands[i],">") == 0) {
            tempCommands[j] = NULL;
            break;
        } else {
            strcpy(tempCommands[j],execCommands[i]);
            j += 1;
        }
    }
    int rc = fork();
	
	if (rc < 0){			// fork failed; exit
		exit(0);
	}
	else if (rc == 0) {		// child (new) process
         // ------- Redirecting STDOUT --------
		
        int file_desc = open(execCommands[size - 1], O_CREAT | O_WRONLY | O_APPEND,S_IRWXU); // opening user specified file
        if(file_desc < 0) 
            printf("Error opening the file\n");
        dup2(file_desc,1); // temporarily replace STDOUT with the given file

        // ------------------------------------
        
        execvp(tempCommands[0], tempCommands);
	} 
	else {              // parent process (rc holds child PID)
		int rc_wait = wait(NULL);
	}
}

int main()
{
	// Initial declarations
    signal(SIGINT, SIG_IGN); // ignores Ctrl + C
    signal(SIGTSTP, SIG_IGN); // ignores Ctrl + Z
	
	while(1)	// This loop will keep your shell running until user exits.
	{
		// Print the prompt in format - currentWorkingDirectory$
        char cwd[1024];
        if(getcwd(cwd,sizeof(cwd)) != NULL) 
            printf("%s$",cwd);
		
		// accept input with 'getline()'
        size_t size = 10,bytes_read;
        char* string;
        string = (char*)malloc(size);
        bytes_read = getline(&string,&size,stdin);

        if(bytes_read != -1 && strlen(string) != 1) {

            // Parse input with 'strsep()' for different symbols (&&, ##, >) and for spaces.
            int choice = 3,numOfArgs = 0;
            char** command = parseInput(string,&choice,&numOfArgs); 
    
            if(choice == -1)	// When user uses exit command.
            {
            	printf("Exiting shell...\n");
            	break;
            }
            
            if(choice == 0)
            	executeParallelCommands(command,numOfArgs);		// This function is invoked when user wants to run multiple commands in parallel (commands separated by &&)
            else if(choice == 1)
            	executeSequentialCommands(command,numOfArgs);	// This function is invoked when user wants to run multiple commands sequentially (commands separated by ##)
            else if(choice == 2)
            	executeCommandRedirection(command,numOfArgs);	// This function is invoked when user wants redirect output of a single command to and output file specificed by user
            else
            	executeCommand(command,numOfArgs);		// This function is invoked when user wants to run a single commands
        }
	}
	
	return 0;
}
