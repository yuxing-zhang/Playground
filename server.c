#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>

#define PORT 5050
#define QUELEN 1

int main(void) {
    int sockfd;
    if ((sockfd = socket(PF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Failed in creating socket!");
        exit(1);
    }

    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof servaddr);

    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    servaddr.sin_port = htons(PORT);
    
    if (bind(sockfd, (struct sockaddr *) &servaddr, sizeof servaddr)) {
        perror("Failed in binding socket!");
        exit(2);
    }

    if (listen(sockfd, QUELEN)) {
        perror("Failed in listening!");
        exit(3);
    }

    int connfd;
    struct sockaddr_in cliaddr;
    socklen_t addrlen = sizeof cliaddr;

    while (1) {
        memset(&cliaddr, 0, sizeof cliaddr);
        if ((connfd = accept(sockfd, (struct sockaddr *)&cliaddr, 
                             &addrlen)) < 0) {
            perror("Failed in accepting connection!");
            exit(4);
        }

        int pid = fork();

        if (pid) {
            close(connfd);
        }
        else {
            close(sockfd);

            char buff[128];
            int n;

            while ((n = recv(connfd, buff, 128, 0)) > 0) {
                fputs(buff, stdout);
                fgets(buff, 128, stdin);
                send(connfd, buff, strlen(buff) + 1, 0);
            }

            if (n < 0) {
                perror("Failed in reading message!");
                exit(5);
            }

            close(connfd);
            exit(0);
        }
    }
}

