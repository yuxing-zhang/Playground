#include <stdlib.h>
#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>

#define PORT 5050

int main(int argc, char **argv) {
    int sockfd;
    if ((sockfd = socket(PF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Failed to create socket!");
        exit(1);
    }

    struct sockaddr_in servaddr;
    memset(&servaddr, 0, sizeof servaddr);

    servaddr.sin_family = AF_INET;
    inet_aton(argv[1], &servaddr.sin_addr);
    servaddr.sin_port = htons(PORT);

    if (connect(sockfd, (struct sockaddr *) &servaddr, sizeof servaddr)) {
        perror("Falied to connect to server!");
        exit(2);
    }

    char buff[128];
    int n;
    while (1) {
        fgets(buff, 128, stdin);
        if ((n = strlen(buff)) == 1) {
            break;
        }
        send(sockfd, buff, n + 1, 0);
        recv(sockfd, buff, 128, 0);
        fputs(buff, stdout);
    }
    
    close(sockfd);
}
