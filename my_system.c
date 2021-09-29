#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>

/* Execute command using sh */
int my_system(const char *command) {
    pid_t p = fork();
    if (p == 0) {
        execlp("sh", "sh", "-c", command, NULL);
        perror("Execution failed");
        _exit(EXIT_FAILURE);
        
    }

    if (p == -1) {
        perror("Forking failed");
        exit(EXIT_FAILURE);
    }

    int status;
    waitpid(p, &status, 0);
    return status;
}

