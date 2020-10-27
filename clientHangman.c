#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <string.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdint.h>

#define HOST "192.168.1.19"
#define PORT 2020
#define SOCKET int

int main(){
    SOCKET s;
    struct sockaddr_in server;
    
    s = socket(AF_INET,SOCK_STREAM,0);
    printf("Socket created...\n");

    memset(&server, 0, sizeof(server));
    server.sin_addr.s_addr = inet_addr(HOST);
    server.sin_port = htons(PORT);
    server.sin_family = AF_INET;

    connect(s, (struct sockaddr*)&server, sizeof(server));
    printf("Connetion succeded...\n");
    uint16_t len;
    char comp[8] = "HANGMAN'\0'";
    recv(s, (char*)&len, sizeof(uint16_t), 0);
    len = ntohs(len);
    printf("The length of the word is %hu !\n", len);
    len += 1;
    char cuv[len];
    while(1){
        char lit;
        printf("litera = ");
        scanf(" %c", &lit);
        printf("\n");
        send(s, (char*)&lit, sizeof(char), 0);
        char hangman[8];
        recv(s, hangman, sizeof(char) * 8, 0);
        hangman[7] = '\0';
        printf("I am %s !\n",hangman);
        if(strcmp(hangman,comp) == 0){
            printf("I lost !");
            return;
        }
        recv(s, cuv, sizeof(char) * len, 0);
        cuv[len - 1] = '\0';
        printf("The current word is %s !\n", cuv);
    }
    close(s);   
    return 0;
}
