#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>

void print_array(char arr[16]);

int main(int argc, char** argv) {

    char rand_str[16] = {0x4e, 0x55, 0x56, 0x45, 0x57, 0x5a, 0x50, 0x42, 0x45, 0x59, 0x4c, 0x54, 0x43, 0x43, 0x59, 0x56};
    char hashed[16];

    printf("Length: %d\n", strlen(rand_str));
    
    MD5(rand_str, strlen(rand_str), hashed);
    print_array(hashed);
    
    return 0;
}

void print_array(char arr[16]) {
    int index;
    
    for (index = 0; index < 16; index++) {
        printf("\\x%02x", (unsigned char)arr[index]);
    }
    printf("\n");
}