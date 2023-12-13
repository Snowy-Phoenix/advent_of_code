#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048
#define LITRES 150
#define max(a, b) ((a) > (b) ? (a) : (b))
#define min(a, b) ((a) < (b) ? (a) : (b))

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input25.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    char* line_ptr = line;
    int row;
    int col;
    fgets(line, MAX_CHAR, f);
    sscanf(line_ptr, "To continue, please consult the code grid in the manual.  Enter the code at row %d, column %d.", &row, &col);
    fclose(f);

    unsigned long long seed = 20151125;
    unsigned long long mult = 252533;
    unsigned long long mod = 33554393;
    unsigned long long next_row = 3;
    unsigned long long curr_row = 2;
    unsigned long long curr_col = 1;
    unsigned long long curr_val = 20151125;
    while (1) {
        curr_val *= mult;
        curr_val %= mod;
        if (curr_col == col && curr_row == row) {
            break;
        }
        curr_col++;
        curr_row--;
        if (curr_row == 0) {
            curr_row = next_row;
            next_row++;
            curr_col = 1;
        }
    }
    printf("Part 1: %d\n", curr_val);
    return 0;
}
