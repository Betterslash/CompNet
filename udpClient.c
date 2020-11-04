#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>

#define SOCKET int
#define PORT 2020
#define HOST "192.168.1.2"

void error(char *);
int main(){
    SOCKET s;
    struct sockaddr_in server;
    uint32_t srv_len = sizeof(server);
    s = socket(AF_INET, SOCK_DGRAM, 0);
    printf("Socket created...\n");
    
    memset(&server, 0, sizeof(server));
    server.sin_port = htons(PORT);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr(HOST);

    uint16_t len;
    uint16_t arr[100];
    printf("Give here the length of the array >> ");
    scanf("%hu", &len);
    for(int i = 0; i < len; i++){
        printf("vector[%d] = ", i);
        scanf("%hu", &arr[i]);
    }

    uint16_t s_len = htons(len);
    sendto(s, (char*)&s_len, sizeof(uint16_t), 0, (struct sockaddr*)&server, sizeof(server));
    uint16_t elem;
    for(int i = 0; i < len; i++){
        elem = htons(arr[i]);
        sendto(s, (char*)&elem, sizeof(uint16_t), 0, (struct sockaddr*)&server, sizeof(server));
    }

    uint16_t r_len;
    uint16_t r_arr[100];
    recvfrom(s, (char*)&r_len, sizeof(uint16_t), 0, (struct sockaddr*)&server, &srv_len);
    r_len = ntohs(r_len);
    uint16_t r_elem;
    for(int i = 0; i < r_len; i++){
        recvfrom(s, (char*)&r_elem, sizeof(uint16_t), 0, (struct sockaddr*)&server, &srv_len);  
        r_arr[i] = ntohs(r_elem);
    }

    for(int i = 0; i < r_len; i++){
        printf("vector_r[%d] = %hu\n", i, r_arr[i]);
    }

    close(s);
    return 0;
}