#include <string.h>
#include <stdlib.h>

#include "pw_generator.h"

void randomPasswordGenerator(int N, char* total_pw, char* final_password){
    int i;
    char password[N + 1];
    int total_pw_length = strlen(total_pw); 

    for (i=0; i <N; i++){
        password[i] = total_pw[rand() % total_pw_length];
    };
    password[N] = '\0';
    strcpy(final_password, password);
    pw_strenth(final_password);
}