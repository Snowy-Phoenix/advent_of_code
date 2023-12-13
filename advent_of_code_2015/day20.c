#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_CHAR 512
#define max(a, b) ((a) > (b) ? (a) : (b))

void part1(int n) {
    int house = 1;
    while (house < __INT_MAX__) {
        int presents = 0;
        int i;
        int upper_bound = (int)sqrtf((float)house);
        for (i = 1; i <= upper_bound; i++) {
            if (house % i == 0) {
                presents += i * 10;
                presents += (house / i) * 10;
            }
        }
        if (house % upper_bound == 0) {
            presents -= upper_bound * 10;
        }
        if (presents >= n) {
            printf("Part 1: %d\n", house);
            return;
        }
        house++;
    }
}

void part2(int n) {
    int* houses = calloc(n, sizeof(int));
    for (int i = 1; i < n / 10; i++) {
        for (int j = 1; j <= 50; j++) {
            if (i * j >= n) {
                break;
            }
            houses[i * j] += 11 * i;
        }
    }
    for (int i = 1; i < n; i++) {
        if (houses[i] >= n) {
            printf("Part 2: %d\n", i);
            free(houses);
            return;
        }
    }
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input20.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        puts("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    int n;
    if (!fscanf(f, "%d", &n)) {
        puts("Unable to parse input.");
        return 1;
    }
    fclose(f);
    part1(n);
    part2(n);

    return 0;
}
