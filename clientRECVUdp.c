#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdint.h>

#define PORT_C 2030
#define HOST_C "127.0.0.1"
#define PORT 2020
#define HOST "192.168.1.2"
#define SOCKET int

int main(){
    int c_len;
    c_len = sizeof(struct sockaddr_in);
    SOCKET s_socket, c_socket;
    struct sockaddr_in server, client;

    c_socket = socket(AF_INET, SOCK_DGRAM, 0);
    s_socket = socket(AF_INET, SOCK_STREAM, 0);
    printf("Socket created...\n");

    memset(&client, 0, sizeof(client));
    client.sin_addr.s_addr = inet_addr(HOST_C);
    client.sin_port = htons(PORT_C);
    client.sin_family = AF_INET;

    memset(&server, 0, sizeof(server));
    server.sin_addr.s_addr = inet_addr(HOST);
    server.sin_port = htons(PORT);
    server.sin_family = AF_INET;

    if(connect(s_socket, (struct sockaddr*)&server, sizeof(server)) < 0){
        printf("Failed to connect to the server...\n");
        return 0;
    }
    char* username = (char*)malloc(sizeof(char)*100);
    printf("Connection succeded...\n");
    printf("Give here your username:");
    scanf("%s", username);
    uint16_t lgt = strlen(username);
    username[lgt] = '\0';
    lgt = htons(lgt);
    if(send(s_socket, (char*)&lgt, sizeof(uint16_t), 0) < 0){
        printf("Failed to register...\n");
        return 0;
    }
    if(send(s_socket, username, sizeof(char)*ntohs(lgt), 0) < 0){
        printf("Failed to register...\n");
        return 0;
    }
    printf("Registered succesfully...\n");
    bind(c_socket, (struct sockaddr*)&client, sizeof(client));
    while(1){
        uint16_t r_len;
        recvfrom(c_socket, (char*)&r_len, sizeof(uint16_t), 0, (struct sockaddr*)&client, &c_len);
        r_len = ntohs(r_len);
        char* r_word = (char*)malloc(sizeof(char) * r_len);
        recvfrom(c_socket, r_word, sizeof(char) * r_len, 0, (struct sockaddr*)&client, &c_len);
        r_word[r_len] = '\0';
         if(strcmp(r_word, "exit") == 0){
            printf("I will exit now thanks!...\n");
            return;
        }
        printf("<< %s \n", r_word);
        char* word = (char*)malloc(sizeof(char) * 100);
        printf(">> ");
        fgets(word, 35, stdin);
        uint16_t len = strlen(word);
        word[len - 1] = '\0';
        len = htons(len);
        sendto(c_socket, (char*)&len, sizeof(uint16_t), 0, (struct sockaddr*)&client, sizeof(client));
        sendto(c_socket, word, sizeof(char)*ntohs(len), 0, (struct sockaddr*)&client, sizeof(client));
        if(strcmp(word, "exit") == 0){
            return;
        }
    }
    printf("Exited succesfully...");
    close(s_socket);
    close(c_socket);
    return 0;
}
