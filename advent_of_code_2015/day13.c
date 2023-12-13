#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048
#define max(a, b) ((a) > (b) ? (a) : (b))

struct names {
    char name[32];
    struct names* next;
};

struct happiness {
    int happiness;
    struct happiness* col_next;
    struct happiness* row_next;
};

void print_table(struct happiness* table) {
    while (table) {
        struct happiness* col = table;
        while (col) {
            printf("%d\t", col->happiness);
            col = col->col_next;
        }
        printf("\n");
        table = table->row_next;
    }
}

int get_i_name(struct names* names_list, char* name) {
    int i = 0;
    while (1) {
        if (!strlen(names_list->name)) {
            strncpy(names_list->name, name, 32);
            names_list->name[31] = 0;
            return i;
        }
        if (strcmp(names_list->name, name) == 0) {
            return i;
        } else {
            i++;
            if (names_list->next == NULL) {
                names_list->next = calloc(1, sizeof(struct names));
            }
            names_list = names_list->next;
        }
    }
}

void add_happiness(struct happiness* table, int row, int col, int happiness) {
    for (int r = 0; r < row; r++) {
        if (table->row_next == NULL) {
            table->row_next = calloc(1, sizeof(struct happiness));
        }
        table = table->row_next;
    }
    for (int c = 0; c < col; c++) {

        if (table->col_next == NULL) {
            table->col_next = calloc(1, sizeof(struct happiness));
        }
        table = table->col_next;
    }
    table->happiness = happiness;
}

int get_happiness(struct happiness* table, int row, int col) {
    for (int r = 0; r < row; r++) {
        table = table->row_next;
    }
    for (int c = 0; c < col; c++) {
        table = table->col_next;
    }
    return table->happiness;
}

int get_max_happiness(struct happiness* table, int* seating, int* people_map, int len, int free_spots) {
    int max_happiness = 0;
    if (free_spots) {
        int i = 0;
        for (; i < len; i++) {
            if (seating[i] == -1) {
                break;
            }
        }
        for (int j = 0; j < len; j++) {
            if (people_map[j] == -1) {
                seating[i] = j;
                people_map[j] = i;
                int happiness = get_max_happiness(table, seating, people_map, len, free_spots - 1);
                max_happiness = max(max_happiness, happiness);
                seating[i] = -1;
                people_map[j] = -1;
            }
        }
        if (free_spots == 1) {

        }
    } else {
        for (int i = 0; i < len; i++) {
            max_happiness += get_happiness(table, seating[i], seating[(i + 1) % len]);
            max_happiness += get_happiness(table, seating[(i + 1) % len], seating[i]);
        }
    }
    return max_happiness;
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input13.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    struct names names_list = {0};
    struct happiness happiness_table = {0};
    int happiness = 1;
    int rows = 0;
    int cols = 0;
    while (fgets(line, MAX_CHAR, f)) {
        char* words = strtok(line, " .\n"); // name
        int row = get_i_name(&names_list, words);
        strtok(NULL, " .\n");               // would
        words = strtok(NULL, " .\n");       // gain/lose
        if (strcmp(words, "lose") == 0) {
            happiness = -1;
        }

        words = strtok(NULL, " .\n");       // number
        happiness *= atoi(words);
        strtok(NULL, " .\n");               // happiness
        strtok(NULL, " .\n");               // units
        strtok(NULL, " .\n");               // by
        strtok(NULL, " .\n");               // sitting
        strtok(NULL, " .\n");               // next
        strtok(NULL, " .\n");               // to

        words = strtok(NULL, " .\n");       // name
        int col = get_i_name(&names_list, words);
        add_happiness(&happiness_table, row, col, happiness);
        happiness = 1;
        rows = max(rows, row);
        cols = max(cols, col);
    }
    rows += 1; // Rows and cols were computed using array indices.
    cols += 1;
    fclose(f);
    if (rows != cols) {
        printf("Invalid table\n");
        return 1;
    }
    int* seating = malloc(sizeof(int) * rows);
    int* people = malloc(sizeof(int) * rows);
    for (int i = 0; i < rows; i++) {
        seating[i] = -1;
        people[i] = -1;
    }
    int max_happiness = get_max_happiness(&happiness_table, seating, people, rows, rows);
    printf("Part 1: %d\n", max_happiness);

    for (int i = 0; i < rows; i++) {
        add_happiness(&happiness_table, rows, i, 0);
        add_happiness(&happiness_table, i, cols, 0);
    }
    
    seating = realloc(seating, sizeof(int) * (rows + 1));
    people = realloc(people, sizeof(int) * (rows + 1));
    for (int i = 0; i < rows + 1; i++) {
        seating[i] = -1;
        people[i] = -1;
    }
    max_happiness = get_max_happiness(&happiness_table, seating, people, rows + 1, rows + 1);
    printf("Part 2: %d\n", max_happiness);
    
    return 0;
}
