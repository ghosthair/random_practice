#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <ctype.h>

#include "alphabet.h"
#include "information_content.h"
#include "pw_generator.h"

int main(int argc, char *argv[]) {
    srand(time(NULL));
    if (argc < 3) {
        printf("Error: Missing length or number of passwords arguments\n");
        return 1;
    }
    
    int N = atoi(argv[1]);
    int num_of_pw = atoi(argv[2]);
    char luds[10] = "";
    char usr_input[1024] = "";
    char final_password[N + 1];

    if (argc >= 4 && argv[3] != NULL) {
        if (strlen(argv[3]) > 10) {
            printf("Too many options in luds\n");
            return 1;
        } else {
            strcat(luds, argv[3]);
        }
    }

    if (argc >= 5 && argv[4] != NULL) {
        if (isgraph(*argv[4])) {
            strcat(usr_input, argv[4]);
            if (strlen(usr_input) == 1) {
                strcat(usr_input, "abc");
            }
        } else {
            printf("Not the proper symbols!\n");
            return 1;
        }
    }

    printf("Generating %d password(s) of length %d\n", num_of_pw, N);
    char* total_pw = alphabet(luds, usr_input);
    if (total_pw == NULL) {
        printf("Memory allocation failed.\n");
        return 1;
    }

    for (int i = 0; i < num_of_pw; i++) {
        randomPasswordGenerator(N, total_pw, final_password);
        printf("Password: %s\n", final_password);
    }
    
    free(total_pw);
    return 0;
}