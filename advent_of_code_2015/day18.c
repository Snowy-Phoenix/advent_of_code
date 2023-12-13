#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048
#define GRID_SIZE 100
#define max(a, b) ((a) > (b) ? (a) : (b))

FILE* get_fp(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input18.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return NULL;
    }
    return f;
}

void update_neighbour_data(char grid[GRID_SIZE][GRID_SIZE], char neighbours[GRID_SIZE][GRID_SIZE]) {
    // Clear all the data in the neighbours grid
    for (int row = 0; row < GRID_SIZE; row++) {
        for (int col = 0; col < GRID_SIZE; col++) {
            neighbours[row][col] = 0;
        }
    }

    // Update the neighbours grid with the new data.
    for (int row = 0; row < GRID_SIZE; row++) {
        for (int col = 0; col < GRID_SIZE; col++) {
            if (grid[row][col] == 0) {
                continue;
            }
            for (int r = -1; r < 2; r++) {
                for (int c = -1; c < 2; c++) {
                    int cell_r = row + r;
                    int cell_c = col + c;
                    if (0 <= cell_r && cell_r < GRID_SIZE) {
                        if (0 <= cell_c && cell_c < GRID_SIZE) {
                            neighbours[cell_r][cell_c]++;
                        }
                    }
                }
            }
        }
    }
}

void update_part1(char grid[GRID_SIZE][GRID_SIZE], char neighbours[GRID_SIZE][GRID_SIZE]) {
    update_neighbour_data(grid, neighbours);
    // Update the original grid with the new cells.
    for (int row = 0; row < GRID_SIZE; row++) {
        for (int col = 0; col < GRID_SIZE; col++) {
            int cell = neighbours[row][col];
            if (grid[row][col] == 0) {
                grid[row][col] = (cell == 3);
            } else {
                grid[row][col] = (3 <= cell && cell <= 4);
            }
        }
    }
}

void update_part2(char grid[GRID_SIZE][GRID_SIZE], char neighbours[GRID_SIZE][GRID_SIZE]) {
    grid[0][0] = 1;
    grid[0][GRID_SIZE - 1] = 1;
    grid[GRID_SIZE - 1][0] = 1;
    grid[GRID_SIZE - 1][GRID_SIZE - 1] = 1;

    update_neighbour_data(grid, neighbours);
    // Update the original grid with the new cells.
    for (int row = 0; row < GRID_SIZE; row++) {
        for (int col = 0; col < GRID_SIZE; col++) {
            int cell = neighbours[row][col];
            if (grid[row][col] == 0) {
                grid[row][col] = (cell == 3);
            } else {
                grid[row][col] = (3 <= cell && cell <= 4);
            }
        }
    }
    grid[0][0] = 1;
    grid[0][GRID_SIZE - 1] = 1;
    grid[GRID_SIZE - 1][0] = 1;
    grid[GRID_SIZE - 1][GRID_SIZE - 1] = 1;
}

int simulate(FILE* f, void (*update)(char[GRID_SIZE][GRID_SIZE], char[GRID_SIZE][GRID_SIZE])) {
    char line[MAX_CHAR];
    char grid[GRID_SIZE][GRID_SIZE];
    char neighbours[GRID_SIZE][GRID_SIZE];
    int row = 0;
    int col = 0;
    while (fgets(line, MAX_CHAR, f)) {
        char* ptr = line;
        while (*ptr) {
            grid[row][col] = ((*ptr) == '#');
            if (col >= GRID_SIZE) {
                break;
            }
            col++;
            ptr++;
        }
        row++;
        col = 0;
        if (row >= GRID_SIZE) {
            break;
        }
    }

    const int steps = 100;
    for (int step = 0; step < steps; step++) {
        update(grid, neighbours);
        
    }
    int sum = 0;
    for (int row = 0; row < GRID_SIZE; row++) {
        for (int col = 0; col < GRID_SIZE; col++) {
            sum += grid[row][col];
        }
    }
    return sum;
}

int main(int argc, char** argv) {
    FILE* f = get_fp(argc, argv);
    if (f == NULL) {
        return -1;
    }
    printf("Part 1: %d\n", simulate(f, update_part1));
    fclose(f);

    f = get_fp(argc, argv);
    if (f == NULL) {
        return -1;
    }
    printf("Part 2: %d\n", simulate(f, update_part2));
    fclose(f);
    return 0;
}
