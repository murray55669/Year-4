#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>
#include <time.h>

void print_array(char arr[16]);
void print_array_c(char arr[16]);

int main(int argc, char** argv) {
    int count = 0;
    int index;
    char rand_str[16];
    rand_str[15] = 0x00;
    
    int str_len = 15;

    char end0 = 0x00;
    char end1 = 0x91;
    char end2 = 0xeb;
    
    time_t t;
    srand((unsigned) time(&t));

    char hashed[16];

    while(1) {
        count++;

        for (index = 0; index < 15; index++) {
            rand_str[index] = 'A' + (rand() % 26);
        }

        MD5(rand_str, str_len, hashed);

        if ((hashed[13] == end0) && (hashed[14] == end1) && (hashed[15] == end2)) {
            printf("String: ");
            print_array(rand_str);
            printf("Digest: ");
            print_array(hashed);
            printf("Target length: %d\nAttempts: %d\n", str_len, count);
            print_array_c(rand_str);
            print_array_c(hashed);
            
            break;
        }
    }

    return 0;
}

void print_array(char arr[16]) {
    int index;
    
    for (index = 0; index < 16; index++) {
        printf("\\x%02x", (unsigned char)arr[index]);
    }
    printf("\n");

}

void print_array_c(char arr[16]) {
    int index;
    
    for (index = 0; index < 16; index++) {
        printf("0x%02x, ", (unsigned char)arr[index]);
    }
    printf("\n");
}