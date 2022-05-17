#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<string.h>

int main() {
    size_t size = 10,bytes_read;
    char* string,*found;
    string = (char*)malloc(size);
    bytes_read = getline(&string,&size,stdin);
    if(bytes_read == -1) printf("ERROR\n");
    
    else puts(string);
    for(int i = 0;i < strlen(string);++i)
        printf("%d ",string[i]);

    // char* exit = "exit";
    // while((found = strsep(&string," ")) != NULL) {
    //     found[strlen(found) - 1] = 0;
    //     for(int i = 0;i < strlen(found);++i)
    //         printf("%d ",found[i]);
    // }


    // char cwd[100];
    // if(getcwd(cwd,sizeof(cwd)) != NULL) 
    //     puts(cwd);

}