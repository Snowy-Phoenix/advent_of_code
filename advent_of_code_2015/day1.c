#include <stdio.h>

int main(void) {
    FILE* f = fopen("input1.txt", "r");
    char line[1000];
    int floor = 0;
    int basement = 0;
    int position = 1;
    while (fgets(line, 1000, f)) {
        for (int i = 0; i < 1000; i++) {
            if (line[i] == 0) {
                break;
            }
            if (line[i] == '(') {
                floor++;
            } else {
                floor--;
            }
            if (floor == -1 && basement == 0) {
                basement = position;
            }
            position += 1;
        }
    }
    printf("Part 1: %d\n", floor);
    printf("Part 2: %d\n", basement);
    return 0;
}