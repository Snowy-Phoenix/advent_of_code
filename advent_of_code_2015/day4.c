#include <stdio.h>
#include <openssl/md5.h>
#include <strings.h>
#include <stdlib.h>
#define MAX_CHAR 100

void incinput(char* input, int* len) {
    int i = (*len) - 1;
    char c = input[i];
    while ('0' <= c && c <= '9') {
        if (c == '9') {
            input[i] = '0';
            i--;
            c = input[i];
        } else {
            input[i]++;
            return;
        }
    }
    input[i + 1] = '1';
    input[*len] = '0';
    input[*len + 1] = 0;
    (*len)++;
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input4.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    char input[MAX_CHAR];
    fgets(line, MAX_CHAR, f);

    int strlen = 0;
    while (line[strlen]) {
        input[strlen] = line[strlen];
        strlen++;
    }
    input[strlen] = '0';
    strlen++;
    input[strlen] = 0;

    unsigned char* hash;
    int i = 0;
    int part1 = 0;
    while (i < __INT32_MAX__) {
        hash = MD5(input, strlen, NULL);
        if (!part1 && hash[0] == 0 && hash[1] == 0 && (hash[2] & 0xf0) == 0) {
            printf("Part 1: %d\n", i);
            part1 = 1;
        }
        if (hash[0] == 0 && hash[1] == 0 && hash[2] == 0) {
            printf("Part 2: %d\n", i);
            break;
        }
        incinput(input, &strlen);
        i++;
    }

    return 0;
}