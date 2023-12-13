#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048
#define max(a, b) ((a) > (b) ? (a) : (b))

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input16.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }

    const int exp_values[] = {3, 7, 2, 3, 0, 0, 5, 3, 2, 1};
    const char* attributes[] = {"children", "cats", "samoyeds",
        "pomeranians", "akitas", "vizslas", "goldfish",
        "trees", "cars", "perfumes"};

    char delineators[] = ":, \n";
    char line[MAX_CHAR];
    while (fgets(line, MAX_CHAR, f)) {
        char* word;
        int sue_n;
        int part1_match = 1;
        int part2_match = 1;

        strtok(line, delineators); // Sue
        sue_n = atoi(strtok(NULL, delineators)); // Sue number
        word = strtok(NULL, delineators);   // Attribute
        while (word) {
            for (int i = 0; i < sizeof(attributes) / sizeof(char*); i++) {
                if (strcmp(word, attributes[i]) == 0) {
                    int value = atoi(strtok(NULL, delineators));    // attribute value
                    int exp_value = exp_values[i];
                    if ((i == 1) || (i == 7))  {  
                        // cats and trees
                        part2_match = part2_match && (value > exp_value);
                    } else if ((i == 3) || (i == 6)) {
                        // pomeranians and goldfish
                        part2_match = part2_match && (value < exp_value);
                    } else {
                        part2_match = part2_match && (value == exp_value);
                    }
                    part1_match = part1_match && (value == exp_value);
                }
            }
            word = strtok(NULL, delineators);
        }
        if (part1_match) {
            printf("Part 1: %d\n", sue_n);
        }
        if (part2_match) {
            printf("Part 2: %d\n", sue_n);
        }
        
    }
    fclose(f);

    return 0;
}
