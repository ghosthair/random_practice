#include <stdio.h>
#include <string.h>  
#include <ctype.h> 
#include <math.h>

int main() {
    char str[101];
    printf("Enter the password string: %s\n", str);
    scanf("%100s",str);
    int i;
    int lowerx = 0;
    int upperx = 0;
    int digitx = 0;
    int symbolx = 0;
    double alphabet_size;
    int size_t = strlen(str);
    double information_content;

    for (i = 0; i < strlen(str); i++) {
        if (islower(str[i])){
            lowerx++;
        }else if (isupper(str[i])){
            upperx++;
        }else if (isdigit(str[i])){
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

    information_content = size_t * (log2(alphabet_size));
    printf("Length: %i\n", size_t);
    printf("Information Content: %f\n", information_content);


    return 0;
}