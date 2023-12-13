#include <stdio.h>
#include <stdlib.h>
#define MAX_CHAR 100

enum type {TOGGLE, ON, OFF};

typedef struct instruction {
    enum type t;
    int x1;
    int x2;
    int y1;
    int y2;
} instruction;

void parse_coords(char* coords, int* x, int* y) {
    *x = 0;
    *y = 0;
    while (*coords) {
        char d = *coords - '0';
        if (0 <= d && d <= 9) {
            *x = (*x * 10) + d;
        } else {
            break;
        }
        coords++;
    }
    coords++;
    while (*coords) {
        char d = *coords - '0';
        if (0 <= d && d <= 9) {
            *y = (*y * 10) + d;
        } else {
            return;
        }
        coords++;
    }
}

void parse_ins(char* line, instruction* ins) {
    int coord1 = -1;
    int coord2 = -1;
    int parsing_coords = 0;
    int i = 0;
    while (line[i]) {
        char c = line[i];
        if (0 <= c - '0' && c - '0' <= 9 && !parsing_coords) {
            if (coord1 == -1) {
                coord1 = i;
            } else {
                coord2 = i;
                break;
            }
            parsing_coords = 1;
        } else if (c == ' ') {
            parsing_coords = 0;
        }
        i++;
    }
    if (coord1 == 7) {
        ins->t = TOGGLE;
    } else if (coord1 == 8) {
        ins->t = ON;
    } else {
        ins->t = OFF;
    }
    parse_coords(line + coord1, &ins->x1, &ins->y1);
    parse_coords(line + coord2, &ins->x2, &ins->y2);
}

char toggle(char light) {
    return !light;
}
char on(char light) {
    return 1;
}
char off(char light) {
    return 0;
}

void turn_lights(char* grid, instruction* ins, char (*function)(char)) {
    for (int y = ins->y1; y <= ins->y2; y++) {
        for (int x = ins->x1; x <= ins->x2; x++) {
            grid[y * 1000 + x] = function(grid[y * 1000 + x]);
        }
    }
}

void turn_lights1(char* grid, instruction* ins) {
    char (*function)(char);
    switch (ins->t) {
        case (TOGGLE):
            function = &toggle;
            break;
        case (ON):
            function = &on;
            break;
        case (OFF):
            function = &off;
            break;
    }
    turn_lights(grid, ins, function);
}

char on_increase(char brightness) {
    return brightness + 1;
}
char off_decrease(char brightness) {
    brightness -= 1;
    if (brightness < 0) {
        return 0;
    } return brightness;
}
char toggle_increase(char brightness) {
    return brightness + 2;
}

void turn_lights2(char* grid, instruction* ins) {
    char (*function)(char);
    switch (ins->t) {
        case (TOGGLE):
            function = &toggle_increase;
            break;
        case (ON):
            function = &on_increase;
            break;
        case (OFF):
            function = &off_decrease;
            break;
    }
    turn_lights(grid, ins, function);
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input6.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    char grid1[1000*1000] = {0};
    char grid2[1000*1000] = {0};
    while (fgets(line, MAX_CHAR, f)) {
        instruction ins;
        parse_ins(line, &ins);
        turn_lights1(grid1, &ins);
        turn_lights2(grid2, &ins);
    }
    int on = 0;
    int total_brightness = 0;
    for (int i = 0; i < 1000*1000; i++) {
        on += grid1[i];
        total_brightness += grid2[i];
    }
    printf("Part 1: %d\n", on);
    printf("Part 2: %d\n", total_brightness);
    return 0;
}