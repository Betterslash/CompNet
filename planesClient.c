#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <string.h>
#include <stdint.h>

#define PORT 2020
#define HOST "192.168.1.2"
#define SOCKET int

int main(){
    SOCKET s;
    struct sockaddr_in server;
    
    s = socket(AF_INET, SOCK_STREAM, 0);
    printf("Socket created...\n");

    memset(&server, 0, sizeof(server));
    server.sin_addr.s_addr = inet_addr(HOST);
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);

    connect(s, (struct sockaddr*)&server, sizeof(server));
    printf("Connected to server...\n");

    
    while(1){
        char* lives = (char*)malloc(sizeof(char));
        uint16_t l, c;
        printf("line = ");
        scanf("%hu",&l);
        l = htons(l);
        send(s, (char*)&l, sizeof(uint16_t), 0);
        printf("column = ");
        scanf("%hu",&c);
        c = htons(c);
        send(s, (char*)&c, sizeof(uint16_t), 0);
        uint16_t lgt;
        recv(s, (char*)&lgt, sizeof(uint16_t), 0);
        lgt = ntohs(lgt);
        printf("%hu\n", lgt);
        char* res = (char*)malloc(sizeof(char) * lgt);
        recv(s, res, sizeof(char) * lgt, 0);
        res[lgt + 1] = '\0';
        printf("%s",res); 
        recv(s, lives, sizeof(char), 0);
        if(lives[0] == 'W'){
            printf("I won!\n");
            return;
        }
        if(lives[0] == 'L'){
            printf("I lost!\n");
            return;
        }
    }
    close(s);
    return 0;
}
