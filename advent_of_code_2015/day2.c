#include <stdio.h>

int min(int i1, int i2, int i3) {
    int m = i1;
    if (i2 < m) {
        m = i2;
    }
    if (i3 < m) {
        m = i3;
    }
    return m;
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input2.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[100];
    int total_paper = 0;
    int total_ribbon = 0;
    while (fgets(line, 100, f)) {
        int i1, i2, i3;
        sscanf(line, "%dx%dx%d", &i1, &i2, &i3);
        total_paper += 2*i1*i2 + 2*i1*i3 + 2*i2*i3;
        total_paper += min(i1*i2, i1*i3, i2*i3);
        total_ribbon += min(2*i1+2*i2, 2*i1+2*i3, 2*i2+2*i3);
        total_ribbon += i1*i2*i3;
        
    }
    printf("Part 1: %d\n", total_paper);
    printf("Part 2: %d\n", total_ribbon);
    return 0;
}