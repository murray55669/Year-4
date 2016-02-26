/*
   (C) 2013 Riccardo Focardi (r1x) <focardi at dsi.unive.it>
   This is vulnerable code developed for the Computer Security course
   at Ca' Foscari University for educational puroposes.
  
   Modified for the Secure Programming course at Edinburgh University
   by Joseph Hallett <J.Hallett@sms.ed.ac.uk>.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License <http://www.gnu.org/licenses/> for more
   details.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>

int main(int argc, char** argv) {
    char correct_hash[16] = {
        0xd0, 0xf9, 0x19, 0x94, 0x4a, 0xf3, 0x10, 0x92,
        0x32, 0x98, 0x11, 0x8c, 0x33, 0x27, 0x91, 0xeb
    };
    char password[16];

    // Show the relative position of the buffers, should be 16
    //printf("%li \n",correct_hash-password);

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
