#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048
#define LITRES 150
#define max(a, b) ((a) > (b) ? (a) : (b))

struct containers {
    int capacity;
    struct containers* next;
};

void append(struct containers** list, int capacity) {
    struct containers* ls = *list;
    if (ls == NULL) {
        *list = malloc(sizeof(struct containers));
        ls = *list;
    } else {
        while (ls->next) {
            ls = ls->next;
        }
        ls->next = malloc(sizeof(struct containers));
        ls = ls->next;
    }
    ls->capacity = capacity;
    ls->next = NULL;
}

int count_bottles(int combination) {
    int summation = 0;
    while (combination) {
        summation += (combination & 1);
        combination >>= 1;
    }
    return summation;
}

int combination_sum(struct containers* list, int combination) {
    int summation = 0;
    while ((combination != 0) && list) {
        summation += (combination & 1) * list->capacity;
        combination >>= 1;
        list = list->next;
    }
    return summation;
}

int is_sum_to(struct containers* list, int combination, int value) {
    return (combination_sum(list, combination) == value);
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input17.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];

    int n_bottles = 0;
    struct containers* list = NULL;
    while (fgets(line, MAX_CHAR, f)) {
        append(&list, atoi(line));
        n_bottles++;
    }
    fclose(f);

    int total_combinations = 0;
    int min_bottles = n_bottles;
    int min_bottle_combinations = 0;
    for (int i = 0; i < (1 << n_bottles); i++) {
        int is_equal = is_sum_to(list, i, LITRES);
        if (is_equal) {
            total_combinations += 1;
            int bottles = count_bottles(i);
            if (bottles < min_bottles) {
                min_bottles = bottles;
                min_bottle_combinations = 1;
            } else if (bottles == min_bottles) {
                min_bottle_combinations++;
            }
        }
    }
    printf("Part 1: %d\n", total_combinations);
    printf("Part 2: %d\n", min_bottle_combinations);
    return 0;
}
