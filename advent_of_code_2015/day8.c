#include <stdio.h>
#define MAX_CHAR 100

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input8.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    int chr_lit = 0;
    int chr_mem = 0;
    int chr_esc = 0;
    while (fgets(line, MAX_CHAR, f)) {
        char* p = line;
        while (*p) {
            char c = *p;
            if (c == '\r' || c == '\n') {
                break;
            }
            if (c == '\\') {
                if (p[1] == 'x') {
                    chr_mem++;
                    chr_esc += 5;
                    chr_lit += 4;
                    p += 4;
                } else {
                    chr_mem++;
                    chr_lit += 2;
                    chr_esc += 4;
                    p += 2;
                }
            } else if (c == '"') {
                chr_lit++;
                chr_esc += 2;
                p++;
            } else {
                chr_lit++;
                chr_mem++;
                chr_esc++;
                p++;
            }
        }
        chr_esc += 2;
    }
    printf("Part 1: %d\n", chr_lit - chr_mem);
    printf("Part 2: %d\n", chr_esc - chr_lit);
    return 0;
}