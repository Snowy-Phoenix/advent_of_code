#include <stdio.h>
#include <stdlib.h>
#define MAX_CHAR 100

typedef struct Sequence {
    char* str;
    int len;
    int max_len;
} Sequence;

void append(Sequence* seq, char c, int times) {
    for (int i = 0; i < times; i++) {
        if (seq->max_len == seq->len) {
            seq->max_len *= 2;
            seq->str = realloc(seq->str, seq->max_len * sizeof(char));
        }
        seq->str[seq->len] = c;
        seq->len++;
    }
}

void set_null(Sequence* seq) {
    if (seq->str[seq->len - 1] != 0) {
        append(seq, 0, 1);
    }
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input10.txt", "r");
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
    Sequence* seq1 = malloc(sizeof(Sequence));
    Sequence* seq2 = malloc(sizeof(Sequence));
    seq1->str = malloc(MAX_CHAR * sizeof(char));
    seq1->len = 0;
    seq1->max_len = MAX_CHAR;
    seq2->str = malloc(MAX_CHAR * sizeof(char));
    seq2->len = 0;
    seq2->max_len = MAX_CHAR;
    int i = 0;
    while (line[i]) {
        append(seq1, line[i], 1);
        i++;
    }
    set_null(seq1);
    int iterations = 50;
    for (int i = 1; i <= iterations; i++) {
        char curr_n = seq1->str[0];
        int consecutives = 1;
        for (int j = 1; j < seq1->len; j++) {
            if (seq1->str[j] - '0' < 0 || seq1->str[j] - '0' > 9) {
                append(seq2, consecutives + '0', 1);
                append(seq2, curr_n, 1);
                set_null(seq2);
                break;
            } else if (seq1->str[j] != curr_n) {
                append(seq2, consecutives + '0', 1);
                append(seq2, curr_n, 1);
                curr_n = seq1->str[j];
                consecutives = 1;
            } else {
                consecutives++;
            }
        }
        Sequence* tmp = seq1;
        seq1 = seq2;
        seq2 = tmp;
        seq2->len = 0;
        if (i == 40) {
            printf("Part 1: %d\n", seq1->len - 1);
        }
    }
    printf("Part 2: %d\n", seq1->len - 1);
    free(seq1->str);
    free(seq1);
    free(seq2->str);
    free(seq2);
    return 0;
}
