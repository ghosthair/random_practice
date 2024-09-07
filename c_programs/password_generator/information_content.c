#include <math.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

#include "information_content.h"

void pw_strenth(char* password){
    size_t i;
    int lowerx = 0;
    int upperx = 0;
    int digitx = 0;
    int symbolx = 0;
    float alphabet_size = 0.0;
    size_t password_length = strlen(password);
    double information_content;

    for (i = 0; i < password_length; i++) {
        if (islower(password[i])){
            lowerx++;
        }else if (isupper(password[i])){
            upperx++;
        }else if (isdigit(password[i])){
            digitx++;
        }else {
            symbolx++;
        }
    }
    if (lowerx > 0){
        alphabet_size += 26.0;
    }
    if (upperx > 0)
    {
        alphabet_size += 26.0;
    }
    if (digitx > 0)
    {
        alphabet_size += 10.0;
    }
    if (symbolx > 0) {
        alphabet_size += 32.0;
    }
    printf("Approximate alphabet: %f\n",alphabet_size);
    information_content = password_length * (log2(alphabet_size));
    printf("Information Content: %f\n", information_content);
}