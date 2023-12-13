#include <stdio.h>
#include <stdlib.h>
#define MAX_CHAR 100

typedef struct node {
    int x;
    int y;
    int count;
} node;

typedef struct positions {
    node* arr;
    int length;
    int arr_len;
} pos;

void deliver(pos* p, int x, int y) {
    for (int i = 0; i < p->length; i++) {
        node n = p->arr[i];
        if (n.x == x && n.y == y) {
            n.count++;
            return;
        }
    }
    if (p->length == p->arr_len) {
        p->arr = realloc(p->arr, 2 * p->arr_len * sizeof(node));
        p->arr_len *= 2;
    }
    p->arr[p->length].x = x;
    p->arr[p->length].y = y;
    p->arr[p->length].count = 1;
    p->length++;
}

pos* init_positions(int arr_length) {
    pos* p = malloc(sizeof(pos));
    p->arr_len = arr_length;
    p->length = 0;
    p->arr = malloc(p->arr_len * sizeof(node));
    return p;
}

void destroy_pos(pos* p) {
    free(p->arr);
    free(p);
}

void move(char d, int* x, int* y) {
    if (d == '<') {
        *x -= 1;
    } else if (d == '>') {
        *x += 1;
    } else if (d == 'v') {
        *y -= 1;
    } else if (d == '^') {
        *y += 1;
    }
}

void part1(FILE* f) {
    char line[MAX_CHAR];
    pos *p = init_positions(100);
    int x = 0;
    int y = 0;
    deliver(p, 0, 0);
    while (fgets(line, MAX_CHAR, f)) {
        for (int i = 0; i < MAX_CHAR; i++) {
            if (line[i] == 0) {
                break;
            }
            move(line[i], &x, &y);
            deliver(p, x, y);
        }
    }
    printf("Part 1: %d\n", p->length);
    destroy_pos(p);
}

void part2(FILE* f) {
    char line[MAX_CHAR];
    pos *p = init_positions(100);
    int x1 = 0;
    int y1 = 0;
    int x2 = 0;
    int y2 = 0;
    int turn = 0;
    deliver(p, 0, 0);
    while (fgets(line, MAX_CHAR, f)) {
        for (int i = 0; i < MAX_CHAR; i++) {
            if (line[i] == 0) {
                break;
            }
            if (turn % 2 == 0) {
                move(line[i], &x1, &y1);
                deliver(p, x1, y1);
            } else {
                move(line[i], &x2, &y2);
                deliver(p, x2, y2);
            }
            turn++;

        }
    }
    printf("Part 2: %d\n", p->length);
    destroy_pos(p);
}

FILE* get_file(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input3.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
    }
    return f;
}



int main(int argc, char** argv) {
    
    FILE* f = get_file(argc, argv);
    if (f) {
        part1(f);
    }
    fclose(f);
    f = get_file(argc, argv);
    if (f) {
        part2(f);
    }
    fclose(f);
    return 0;
}