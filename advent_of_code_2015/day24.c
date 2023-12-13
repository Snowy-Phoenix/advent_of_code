#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048
#define LITRES 150
#define max(a, b) ((a) > (b) ? (a) : (b))
#define min(a, b) ((a) < (b) ? (a) : (b))

typedef struct ArrayList {
    int* list;
    int __array_len;
    int len;
} List;

List* list_init() {
    List* ls = malloc(sizeof(List));
    ls->len = 0;
    ls->__array_len = 64;
    ls->list = malloc(sizeof(int) * 64);
    return ls;
}
void list_append(List* ls, int val) {
    if (ls->len == ls->__array_len) {
        ls->__array_len *= 2;
        ls->list = realloc(ls->list, sizeof(int) * ls->__array_len);
    }
    ls->list[ls->len] = val;
    ls->len++;
}
int list_get(List* ls, int i) {
    if (0 <= i && i < ls->len) {
        return ls->list[i];
    }
    printf("Array index %d out of bounds\n", i);
    return 0;
}

int check_subset(List* ls, char* hashmap, int desired_sum, 
                 int current_sum, int last_i, int num_containers) {
    for (int i = last_i; i >= 0; i--) {
        if (hashmap[i]) {
            // Already selected.
            continue;
        }
        int new_sum = current_sum + list_get(ls, i);
        if (new_sum == desired_sum) {
            // We found a subset equalling to the desired sum. Check the remaining
            // containers.
            if (num_containers <= 2) {
                return 1;
            } else {
                hashmap[i] = 1;
                int ret_val = check_subset(ls, hashmap, desired_sum, 0, ls->len - 1, num_containers - 1);
                hashmap[i] = 0;
                if (ret_val) {
                    return ret_val;
                }
            }
        } else if (new_sum > desired_sum) {
            // The new sum is too big.
            continue;
        } else {
            hashmap[i] = 1;
            int ret_val = check_subset(ls, hashmap, desired_sum, new_sum, i - 1, num_containers);
            hashmap[i] = 0;
            if (ret_val) {
                // Found a valid solution.
                return ret_val;
            }
            // Otherwise, continue;
        }
    }
    return 0;
}

long long get_qe(List* ls, char* hashmap) {
    long long product = 1;
    for (int i = 0; i < ls->len; i++) {
        if (hashmap[i]) {
            product *= list_get(ls, i);
        }
    }
    return product;
}

long long iterate_combinations(List* ls, char* hashmap, int desired_sum, 
                         int iterations, int current_sum, int last_i, int num_containers) {
    long long lowest = -1;
    for (int i = last_i; i >= 0; i--) {
        if (hashmap[i]) {
            // Already considered.
            continue;
        }
        int new_sum = current_sum + list_get(ls, i);
        if (new_sum < desired_sum) {
            if (iterations == 1) {
                // Since ls is ordered, all remaining will have less than
                // the desired sum.
                return lowest;
            } else {
                hashmap[i] = 1;
                long long returned_value = iterate_combinations(ls, hashmap, 
                        desired_sum, iterations - 1, new_sum, i - 1, num_containers);
                hashmap[i] = 0;
                if (returned_value != -1) {
                    if (lowest == -1) {
                        lowest = returned_value;
                    } else {
                        lowest = min(returned_value, lowest);
                    }
                }
            }
        } else if (new_sum == desired_sum) {
            if (iterations == 1) {
                // Found a valid subset. must check if it is possible to make the sum in
                // the other subset.
                hashmap[i] = 1;
                if (check_subset(ls, hashmap, desired_sum, 0, ls->len - 1, num_containers - 1)) {
                    if (lowest == -1) {
                        lowest = get_qe(ls, hashmap);
                    } else {
                        lowest = min(get_qe(ls, hashmap), lowest);
                    }
                }
                hashmap[i] = 0;
            } else {
                // Value is too big, and we need more than 1 iterations.
                continue;
            }
        } else {
            // sum is greater than the desired sum, so continue to lower values.
            continue;
        }
    }
    return lowest;
}

long long solve(List* ls, char* hashmap, int num_containers) {
    int sum = 0;
    for (int i = 0; i < ls->len; i++) {
        sum += list_get(ls, i);
    }
    if (sum % num_containers) {
        return -1;
    }
    long long best = -1;
    for (int i = 1; i <= ls->len; i++) {
        best = iterate_combinations(ls, hashmap, sum / num_containers, i, 0, ls->len - 1, num_containers);
        if (best != -1) {
            return best;
        }
    }
    return best;
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input24.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    List* ls = list_init();
    int max_num = 0;
    int num;

    while (fgets(line, MAX_CHAR, f)) {
        num = atoi(line);
        list_append(ls, num);
        max_num = max(num, max_num);
    }
    fclose(f);

    char* hashmap = malloc(ls->len * sizeof(char) + 1);
    memset(hashmap, 0, (ls->len * sizeof(char) + 1));
    long long quantum_entanglement1 = solve(ls, hashmap, 3);
    printf("Part 1: %lld\n", quantum_entanglement1);
    long long quantum_entanglement2 = solve(ls, hashmap, 4);
    printf("Part 2: %lld\n", quantum_entanglement2);
    return 0;
}
