#include <stdio.h>
#define MAX_CHAR 100

int is_nice1(char* line) {
    int vowels = 0;
    int double_letters = 0;
    int bad = 0;
    char last_char = 0;
    while (*line) {
        char c = *line;
        if ((last_char == 'a' && c == 'b') ||
            (last_char == 'c' && c == 'd') ||
            (last_char == 'p' && c == 'q') ||
            (last_char == 'x' && c == 'y')) {
            bad = 1;
            break;
        }
        if (c == 'a' || 
            c == 'e' || 
            c == 'i' || 
            c == 'o' ||
            c == 'u') {
            vowels++;
        }
        double_letters += last_char == c;
        last_char = c;
        line++;
    }
    return (vowels > 2 && double_letters && !bad);
}

int is_nice2(char* line) {
    int hash_len = 26*26;
    int hashmap[hash_len];
    for (int i = 0; i < hash_len; i++) {
        hashmap[i] = 0;
    }
    char last1_char = 0;
    char last2_char = 0;
    int overlap = 0;
    int pair_match = 0;
    int gap_match = 0;
    while (*line) {
        char c = *line;
        if (c == '\n' || c == '\r') {
            break;
        }
        if (last2_char == c) {
            gap_match++;
        }
        int pair = -1;
        if (last1_char) {
            if (c != last1_char) {
                overlap = 0;
            }
            pair = (last1_char - 'a') * 26 + (c - 'a');
            if (hashmap[pair] && !overlap) {
                pair_match++;
            }
            hashmap[pair]++;
            if (c == last1_char) {
                overlap = !overlap;
            }
        }
        if (gap_match && pair_match) {
            return 1;
        }
        last2_char = last1_char;
        last1_char = c;
        line++;
    }
    return 0;
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input5.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    int nice1 = 0;
    int nice2 = 0;
    while (fgets(line, MAX_CHAR, f)) {
        if (is_nice1(line)) {
            nice1++;
        }
        if (is_nice2(line)) {
            nice2++;
        }
    }
    printf("Part 1: %d\n", nice1);
    printf("Part 2: %d\n", nice2);
    return 0;
}