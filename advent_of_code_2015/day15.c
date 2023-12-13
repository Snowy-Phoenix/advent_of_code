#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048
#define max(a, b) ((a) > (b) ? (a) : (b))

struct ingredients {
    int capacity;
    int durability;
    int flavour;
    int texture;
    int calories;
    struct ingredients* next;
};

struct ingredients* parse_ingredient(struct ingredients* ingredients_list, char* line) {
    char* line_ptr = line;
    while (*line_ptr != ' ') {
        line_ptr++;
    }
    int capacity;
    int durability;
    int flavour;
    int texture;
    int calories;
    sscanf(line_ptr, " capacity %d, durability %d, flavor %d, texture %d, calories %d", 
        &capacity, &durability, &flavour, &texture, &calories);
    struct ingredients* ls;
    if (ingredients_list == NULL) {
        ls = malloc(sizeof(struct ingredients));
        ingredients_list = ls;
    } else {
        ls = ingredients_list;
        while (ls->next) {
            ls = ls->next;
        }
        ls->next = malloc(sizeof(struct ingredients));
        ls = ls->next;
    }
    ls->calories = calories;
    ls->capacity = capacity;
    ls->durability = durability;
    ls->flavour = flavour;
    ls->texture = texture;
    ls->next = NULL;

    return ingredients_list;
}

void print_ingredients(struct ingredients* ingredient_list) {
    while (ingredient_list) {
        printf("Capacity %d, durability %d, flavor %d, texture %d, calories %d\n", 
        ingredient_list->capacity, ingredient_list->durability, ingredient_list->flavour, ingredient_list->texture, ingredient_list->calories);
        ingredient_list = ingredient_list->next;
    }
}

int compute_score(struct ingredients* ingredient_list, int* amounts, int len) {
    int capacity = 0;
    int durability = 0;
    int flavour = 0;
    int texture = 0;
    for (int i = 0; i < len; i++) {
        capacity += amounts[i] * ingredient_list->capacity;
        durability += amounts[i] * ingredient_list->durability;
        flavour += amounts[i] * ingredient_list->flavour;
        texture += amounts[i] * ingredient_list->texture;
        ingredient_list = ingredient_list->next;
    }
    if (capacity < 0 || durability < 0 || flavour < 0 || texture < 0) {
        return 0;
    }
    return (capacity * durability * flavour * texture);
}

int compute_calories(struct ingredients* ingredient_list, int* amounts, int len) {
    int calories = 0;
    for (int i = 0; i < len; i++) {
        calories += amounts[i] * ingredient_list->calories;
        ingredient_list = ingredient_list->next;
    }
    if (calories < 0) {
        return 0;
    }
    return calories;
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input15.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    struct ingredients* ingredient_list = NULL;
    int n_ingredients = 0;
    while (fgets(line, MAX_CHAR, f)) {
        ingredient_list = parse_ingredient(ingredient_list, line);
        n_ingredients++;
    }
    fclose(f);
    int max_tsp = 100;
    // The last ingredient amount is not independent.
    int* ratios = calloc(n_ingredients ,sizeof(int));
    int used_tsp = 0;
    int maximum = 0;
    int maximum_500 = 0;
    int i = 0;
    while (ratios[n_ingredients - 2] != max_tsp) {
        ratios[n_ingredients - 1] = max_tsp - used_tsp;
        int score = compute_score(ingredient_list, ratios, n_ingredients);
        if (compute_calories(ingredient_list, ratios, n_ingredients) == 500) {
            maximum_500 = max(maximum_500, score);
        }
        maximum = max(maximum, score);
        if (used_tsp == max_tsp) {
            used_tsp -= ratios[i];
            ratios[i] = 0;
            i++;
        } else {
            ratios[i]++;
            used_tsp++;
            i = 0;
        }
    }
    // Check if the final permutation is the maximum.
    int score = compute_score(ingredient_list, ratios, n_ingredients);
    if (compute_calories(ingredient_list, ratios, n_ingredients) == 500) {
        maximum_500 = max(maximum_500, score);
    }
    printf("Part 1: %d\n", maximum);
    printf("Part 2: %d\n", maximum_500);
    return 0;
}
