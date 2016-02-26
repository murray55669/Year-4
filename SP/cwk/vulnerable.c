#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>

int main(int argc, char** argv) {
    char correct_hash[16] = {
        0xd0, 0xf9, 0x19, 0x94, 0x4a, 0xf3, 0x10, 0x92,
        0x32, 0x98, 0x11, 0x8c, 0x33, 0x27, 0x91, 0xeb
    };
    char password[16] = {
        0x69, 0x69, 0x69, 0x69, 0x69, 0x69, 0x69, 0x69,
        0x69, 0x69, 0x69, 0x69, 0x69, 0x69, 0x69, 0x69
    };

    printf("Insert your password: ");
    scanf("%29s", password);

    printf("\nLength: %d\n", strlen(password));
    MD5(password, strlen(password), password);

    if(memcmp(password, correct_hash, 16) == 0) {
        printf("Correct Password!\n");
    } else {
        printf("Wrong Password, sorry!\n");
    }
    return 0;
}
