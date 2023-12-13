#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 100

int check_string(char* str, size_t len) {
    int consecutive = 0;
    int pairs = 0;
    int pair_skip = 0;
    for (size_t i = 1; i < len; i++) {
        if (i > 1) {
            consecutive = consecutive || 
            ((str[i - 2] == str[i - 1] - 1) &&
             (str[i - 2] == str[i] - 2));
        }
        if (!pair_skip) {
            int is_pair = str[i] == str[i - 1];
            if (is_pair) {
                pairs++; 
                pair_skip = 1;
            }
        } else {
            pair_skip = 0;
        }
    }
    if ((pairs >= 2) && consecutive) {
        return 1;
    }
    return 0;
}

void increment(char* str, size_t len) {
    size_t i = len - 1;
    while (i >= 0) {
        if (str[i] == 'z') {
            str[i] = 'a';
            i--;
        } else {
            str[i]++;
            if (str[i] == 'i' || str[i] == 'o' || str[i] == 'l') {
                str[i]++;
            }
            break;
        }
    }
}

void rm_illegal_chars(char* str) {
    while (*str) {
        if (*str == 'i' || *str == 'o' || *str == 'l') {
            (*str)++;
            str++;
            break;
        }
        str++;
    }
    while (*str) {
        *str = 'a';
        str++;
    }
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input11.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    fgets(line, MAX_CHAR, f);
    fclose(f);
    size_t len = strlen(line);
    rm_illegal_chars(line);
    int found = 0;
    while (1) {
        if (check_string(line, len)) {
            if (found) {
                printf("Part 2: %s\n", line);
                return 0;
            } else {
                printf("Part 1: %s\n", line);
                found = 1;
            }
        }
        increment(line, len);
    }
    return 0;
}
