#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048

char red_string[] = ":\"red\"";

struct summation {
    long total_sum;
    long non_red_sum;
};

struct summation summation(FILE* f) {
    struct summation sum;
    long total_sum = 0;
    long curr_n = 0;
    int sign = 1;
    char ch;

    int red_i = 0;
    int has_red = 0;
    int non_red_sum = 0;
    while ((ch = fgetc(f)) != EOF) {

        if (ch == '-') {
            sign = -1;
        } else if ('0' <= ch && ch <= '9') {
            curr_n = (curr_n * 10) + (ch - '0');
        } else {
            total_sum += sign * curr_n;
            non_red_sum += sign * curr_n;
            curr_n = 0;
            sign = 1;
        }

        char red_c = red_string[red_i];
        if (red_c && !has_red) {
            if (red_c == ch) {
                red_i++;
            } else {
                red_i = 0;
            }
        } else {
            has_red = 1;
        }

        if (ch == '}') {
            sum.total_sum = total_sum;
            if (!has_red) {
                sum.non_red_sum = non_red_sum;
            } else {
                sum.non_red_sum = 0;
            }
            return sum;
        } else if (ch == '{') {
            struct summation results = summation(f);
            total_sum += results.total_sum;
            non_red_sum += results.non_red_sum;
        }
    }

    sum.total_sum = total_sum;
    sum.non_red_sum = non_red_sum;
    return sum;
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input12.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    struct summation sum = summation(f);
    fclose(f);
    printf("Part 1: %ld\n", sum.total_sum);
    printf("Part 2: %ld\n", sum.non_red_sum);
    return 0;
}
