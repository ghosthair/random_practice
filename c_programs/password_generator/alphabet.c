#include "alphabet.h"

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h> 

#define MAX_PW_LENGTH 2048
#define MAX_USR_INPUT 1024

char* alphabet(const char *luds, const char *usr_input) {
    const char numbers[] = "0123456789";
    const char lower_letters[] = "abcdefghijklmnopqrstuvwxyz";
    const char upper_letters[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const char symbols[] = "`~!@#$%^&*()-_=+[]{}\\|;:'\",<.>/?";
    
    char total_pw[MAX_PW_LENGTH] = "";
    size_t total_pw_length = 0;
    int found = 0;
    
    char usr_alphabet[MAX_USR_INPUT] = "";
    if (usr_input && strlen(usr_input) > 0) {
        strncpy(usr_alphabet, usr_input, MAX_USR_INPUT - 1);
    } else {
        strcpy(usr_alphabet, "a");
    }

    if (luds && strlen(luds) > 0) {
        for (size_t j = 0; j < strlen(luds); j++) {
            if (luds[j] == 'l') {
                strcat(total_pw, lower_letters);
                total_pw_length += strlen(lower_letters);
            } else if (luds[j] == 'u') {
                strcat(total_pw, upper_letters);
                total_pw_length += strlen(upper_letters);
            } else if (luds[j] == 'd') {
                strcat(total_pw, numbers);
                total_pw_length += strlen(numbers);
            } else if (luds[j] == 's') {
                strcat(total_pw, symbols);
                total_pw_length += strlen(symbols);
            }
        }
    } else {
        // Default behavior if no luds provided
        strcpy(total_pw, lower_letters);
        strcat(total_pw, upper_letters);
        strcat(total_pw, numbers);
        strcat(total_pw, symbols);
        total_pw_length = strlen(total_pw);
    }

    for (size_t i = 0; i < strlen(usr_alphabet); i++) {
        found = 0;
        for (size_t k = 0; k < total_pw_length; k++) {
            if (usr_alphabet[i] == total_pw[k]) {
                found = 1;
                break;
            }
        }
        if (!found) {
            if (islower(usr_alphabet[i]) && !strchr(total_pw, usr_alphabet[i])) {
                strcat(total_pw, lower_letters);
                total_pw_length += strlen(lower_letters);
            } else if (isupper(usr_alphabet[i]) && !strchr(total_pw, usr_alphabet[i])) {
                strcat(total_pw, upper_letters);
                total_pw_length += strlen(upper_letters);
            } else if (isdigit(usr_alphabet[i]) && !strchr(total_pw, usr_alphabet[i])) {
                strcat(total_pw, numbers);
                total_pw_length += strlen(numbers);
            } else if (ispunct(usr_alphabet[i]) && !strchr(total_pw, usr_alphabet[i])) {
                strcat(total_pw, symbols);
                total_pw_length += strlen(symbols);
            }
        }
    }

    char* result = (char*)malloc(total_pw_length + 1);
    if (result == NULL) {
        return NULL; 
    }
    strcpy(result, total_pw);
    return result;
}

void free_alphabet(char* alphabet) {
    free(alphabet);
}