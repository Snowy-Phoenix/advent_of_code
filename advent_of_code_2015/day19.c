#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 512
#define max(a, b) ((a) > (b) ? (a) : (b))
#define BUCKETS 10007

struct bucket {
    char string[MAX_CHAR];
    struct bucket* next;
};

struct hashset {
    struct bucket* buckets;
    int size;
    int n_buckets;
};

struct subs {
    char from[3];
    char to[50];
    struct subs* next;
};

struct queue_node {
    struct queue_node* next;
    int depth;
    int cost;
    int heuristic;
    char string[MAX_CHAR];
};
struct queue_head {
    struct queue_node* last;
    struct queue_node* front;
    int size;
};

unsigned long hash(unsigned char *str) {
    // djb2 hash function from http://www.cse.yorku.ca/~oz/hash.html
    unsigned long hash = 5381;
    int c;
    while (c = *str++)
        hash = ((hash << 5) + hash) + c;
    return hash;
}

int hashset_add(struct hashset* hashset, char buffer[MAX_CHAR]) {
    int bucket_i = hash(buffer) % hashset->n_buckets;
    struct bucket* hash_bucket = hashset->buckets + bucket_i;
    while (1) {
        if (*hash_bucket->string) {
            if (strcmp(hash_bucket->string, buffer) == 0) {
                return 0;
            } else {
                if (hash_bucket->next == NULL) {
                    hash_bucket->next = malloc(sizeof(struct bucket));
                    hash_bucket = hash_bucket->next;
                    *hash_bucket->string = 0;
                    hash_bucket->next = NULL;
                } else {
                    hash_bucket = hash_bucket->next;
                }
            }
        } else {
            strncpy(hash_bucket->string, buffer, MAX_CHAR);
            hashset->size++;
            return 1;
        }
    }
}

void queue_append_node(struct queue_head* queue, struct queue_node* node) {
    if (queue->size == 0) {
        queue->front = node;
        queue->last = node;
    } else {
        queue->last->next = node;
        queue->last = node;
    }
    queue->size++;
}
void queue_append_data(struct queue_head* queue, char* string, int depth,
                       int cost, int heuristic) {
    struct queue_node* node = malloc(sizeof(struct queue_node));
    if (node == NULL) {
        printf("Unable to allocate.\n");
        return;
    }
    node->depth = depth;
    node->next = NULL;
    node->cost = cost;
    node->heuristic = heuristic;
    strncpy(node->string, string, MAX_CHAR);
    queue_append_node(queue, node);
}
struct queue_node* queue_pop(struct queue_head* queue) {
    struct queue_node* node;
    if (queue->size == 0) {
        return NULL;
    }
    node = queue->front;
    queue->front = node->next;
    queue->size--;
    return node;
}
struct queue_node* queue_pop_astar(struct queue_head* queue) {
    struct queue_node* prev = NULL;
    struct queue_node* best_node_prev = NULL;
    struct queue_node* best_node = queue->front;
    struct queue_node* curr = best_node->next;
    while (curr) {
        if (curr->cost + curr->heuristic < best_node->cost +  best_node->heuristic) {
            best_node_prev = prev;
            best_node = curr;
        }
        prev = curr;
        curr = curr->next;
    }
    if (best_node_prev == NULL) {
        // Front of the queue.
        queue->front = best_node->next;
    } else if (best_node->next == NULL) {
        // back of the queue.
        queue->last = best_node_prev;
        best_node_prev->next = NULL;
    } else {
        // Middle.
        best_node_prev->next = best_node->next;
    }
    queue->size--;
    return best_node;
}

struct subs* append_subs(struct subs** substitutions, 
                      char* from, char* to) {
    struct subs* substitution = *substitutions;
    if (substitution == NULL) {
        *substitutions = malloc(sizeof(struct subs));
        substitution = *substitutions;
    } else {
        while (substitution->next) {
            substitution = substitution->next;
        }
        substitution->next = malloc(sizeof(struct subs));
        substitution = substitution->next;
    }
    strncpy(substitution->from, from, 3);
    strncpy(substitution->to, to, 50);
    substitution->next = NULL;
    return *substitutions;
}

void hash_subs(char* line, int i, char element[3], 
        struct subs* substitutions, struct hashset* hashset,
        struct queue_head* queue) {
    char buffer[MAX_CHAR] = {0};

    if (i > MAX_CHAR - 1) {
        i = MAX_CHAR - 1;
    }
    if (strlen(line) >= MAX_CHAR - 1) {
        return;
    }
    while (substitutions) {
        if (strcmp(substitutions->from, element) == 0) {
            int ptr = 0;
            for (;ptr < i; ptr++) {
                buffer[ptr] = line[ptr];
            }
            char* to_c = substitutions->to;
            while ((ptr < MAX_CHAR - 1) && *to_c) {
                buffer[ptr] = *to_c;
                ptr++;
                to_c++;
            }
            size_t line_len = strlen(line);
            int line_i = i + strlen(element);
            while ((ptr < MAX_CHAR - 1) && (line_i < line_len)) {
                buffer[ptr] = line[line_i];
                ptr++;
                line_i++;
            }
            buffer[ptr] = 0;
            if (hashset_add(hashset, buffer) && queue) {
                queue_append_data(queue, buffer, 0, strlen(substitutions->to), 0);
            }
        }
        substitutions = substitutions->next;
    }
}

void __free_bucket(struct bucket* bucket) {
    if (bucket) {
        if (bucket->next) {
            __free_bucket(bucket->next);
            free(bucket->next);
        }
    }
}

void clear_hashset(struct hashset* hashset) {
    for (int i = 0; i < hashset->n_buckets; i++) {
        hashset->buckets[i].string[0] = 0;
        __free_bucket(hashset->buckets->next);
        hashset->buckets[i].next = NULL;
    }
    hashset->size = 0;
}

void get_all_substitutions(char* molecule, 
                           struct subs* substitutions,
                           struct hashset* hashset,
                           struct queue_head* queue) {
    char element[3] = {0};
    int elem_size;
    int i = 0;
    size_t len = strlen(molecule);
    while (i < len) {
        char c = molecule[i];
        if (c == '\n') {
            break;
        }
        elem_size = 1;
        element[0] = c;
        if (i + 1 < len) {
            c = molecule[i + 1];
            element[1] = 0;
            if ('a' <= c && c <= 'z') {
                element[1] = c;
                elem_size = 2;
            }
        } else {
            element[1] = 0;
        }
        hash_subs(molecule, i, element, substitutions, hashset, queue);
        i += elem_size;
    }
}

int heuristic(char* goal, char* molecule) {
    /* Not admissible. Consider the example,
        ABCDFGHIJKLMN
    and goal,
        ABCDEFGHIJKLMN
    with rule:
        D => DE.
    
    It is 1 away from goal, but the heuristic will
    overestimate as 9.

    Making an admissible heuristic requires using
    Levenshtein distances and substitution costs of the length
    of 'to'.
    */

    int len = strlen(goal);
    for (int i = 0; i < len; i++) {
        if (!(molecule[i])) {
            return len - i;
        }
        if (goal[i] != molecule[i]) {
            return len - i;
        }
    }
    return 0;
}

void part1(char* molecule, struct subs* substitutions, struct hashset* hashset) {
    get_all_substitutions(molecule, substitutions, hashset, NULL);
    printf("Part 1: %d\n", hashset->size);
}

void part2_astar(char* molecule, struct subs* substitutions, struct hashset* hashset) {
    struct queue_head queue;
    struct queue_head next_subs;
    struct subs* sub_ptr;
    struct queue_node* q;
    size_t molecule_len = strlen(molecule);
    queue.front = NULL;
    queue.last = NULL;
    queue.size = 0;
    next_subs.front = NULL;
    next_subs.last = NULL;
    next_subs.size = 0;

    sub_ptr = substitutions;
    while (sub_ptr) {
        if (strcmp(sub_ptr->from, "e") == 0) {
            queue_append_data(&queue, sub_ptr->to, 1, 
                strlen(sub_ptr->from), 
                heuristic(molecule, sub_ptr->from));
        }
        sub_ptr = sub_ptr->next;
    }
    int curr_depth = 0;
    while (q = queue_pop_astar(&queue)) {
        if (strlen(q->string) > molecule_len) {
            free(q);
            continue;
        }else if (strcmp(q->string, molecule) == 0) {
            printf("Part 2: %d\n", q->depth);
            return;
        } else {
            get_all_substitutions(q->string, substitutions, hashset, &next_subs);
            struct queue_node* new_node;
            while (new_node = queue_pop(&next_subs)) {
                new_node->depth = q->depth + 1;
                new_node->cost = new_node->cost + q->cost;
                new_node->heuristic = heuristic(molecule, new_node->string);
                queue_append_node(&queue, new_node);
            }
            free(q);
        }
    }
    printf("No solutions found.\n");
}

void part2_reverse(char* molecule, struct subs* substitutions, struct hashset* hashset) {
    /* The branching factor going forwards is too high. Lets try
    and get to e by removing substitutions.*/
    struct queue_head queue;
    struct queue_node* q;
    struct subs* curr_sub;
    char buffer[MAX_CHAR];
    queue.size = 0;
    queue.front = NULL;
    queue.last = NULL;
    queue_append_data(&queue, molecule, 0, 0, 0);
    int depth = 0;
    while (q = queue_pop(&queue)) {
        if (q->depth > depth) {
            printf("Depth: %d\n", q->depth);
            depth = q->depth;
        }
        curr_sub = substitutions;
        while (curr_sub) {
            char* to_ptr = q->string;
            int to_ptr_offset = 0;
            while (to_ptr = strstr(to_ptr, curr_sub->to)) {
                if (*curr_sub->from == 'e') {
                    if (strcmp(curr_sub->to, q->string) == 0) {
                        printf("Part 2: %d\n", q->depth + 1);
                    } else {
                        break;
                    }
                }
                int i = 0;
                char* q_ptr = q->string;
                while (q_ptr != to_ptr && (i < MAX_CHAR - 1)) {
                    buffer[i] = *q_ptr;
                    q_ptr++;
                    i++;
                }
                char* from_ptr = curr_sub->from;
                while (*from_ptr && (i < MAX_CHAR - 1)) {
                    buffer[i] = *from_ptr;
                    from_ptr++;
                    i++;
                }
                q_ptr = to_ptr + strlen(curr_sub->to);
                to_ptr = q_ptr;
                while (*q_ptr && (i < MAX_CHAR - 1)) {
                    buffer[i] = *q_ptr;
                    i++;
                    q_ptr++;
                }
                buffer[i] = 0;
                if (hashset_add(hashset, buffer)) {
                    queue_append_data(&queue, buffer, q->depth + 1, 0, 0);
                }
            }
            curr_sub = curr_sub->next;
        }
        free(q);
    }
}

void part2_dfs(char* molecule, struct subs* substitutions, struct hashset* hashset, int depth) {
    // Left-right parser. Reads from left to right.
    // If a match is found, it recursively reduces the molecule.
    struct subs* curr_sub;
    char buffer[MAX_CHAR];
    char* mol_ptr = molecule;
    while (*mol_ptr) {
        if (depth == 0) {
            printf("At %s\n", mol_ptr);
        }
        curr_sub = substitutions;
        while (curr_sub) {
            if (strncmp(mol_ptr, curr_sub->to, strlen(curr_sub->to)) == 0) {
                // printf("%s: %s %s %s %d, %d\n", molecule, mol_ptr, curr_sub->from, curr_sub->to,  strlen(curr_sub->to),strncmp(mol_ptr, curr_sub->to, strlen(curr_sub->to)));
                int to_ptr_offset = 0;
                if (*curr_sub->from == 'e') {
                    // printf("molecule: %s\n", molecule);
                    if (strcmp(curr_sub->to, molecule) == 0) {
                        printf("Part 2: %d\n", depth + 1);
                        return;
                    } else {
                        curr_sub = curr_sub->next;
                        continue;
                    }
                }
                int i = 0;
                char* q_ptr = molecule;
                while (q_ptr != mol_ptr && (i < MAX_CHAR - 1)) {
                    buffer[i] = *q_ptr;
                    q_ptr++;
                    i++;
                }
                char* from_ptr = curr_sub->from;
                while (*from_ptr && (i < MAX_CHAR - 1)) {
                    buffer[i] = *from_ptr;
                    from_ptr++;
                    i++;
                }
                q_ptr = mol_ptr + strlen(curr_sub->to);
                while (*q_ptr && (i < MAX_CHAR - 1)) {
                    buffer[i] = *q_ptr;
                    i++;
                    q_ptr++;
                }
                buffer[i] = 0;
                // printf("%s\n", buffer);
                if (hashset_add(hashset, buffer)) {
                    part2_dfs(buffer, substitutions, hashset, depth + 1);
                }
            }
            curr_sub = curr_sub->next;
        }
        mol_ptr++;
    }
    return;
}


int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input19.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    struct subs* substitutions = NULL;
    while (fgets(line, MAX_CHAR, f)) {
        if (*line != '\n') {
            char* from = strtok(line, " => \n");
            char* to = strtok(NULL, " => \n");
            substitutions = append_subs(&substitutions, from, to);
        } else {
            break;
        }
    }
    fgets(line, MAX_CHAR, f);
    fclose(f);
    int line_len = strlen(line);
    if (line[line_len - 1] == '\n') {
        line[line_len - 1] = 0;
    }
    struct hashset hashset;
    hashset.buckets = calloc(BUCKETS, sizeof(struct bucket));
    hashset.size = 0;
    hashset.n_buckets = BUCKETS;

    
    part1(line, substitutions, &hashset);
    // part2_dfs(line, substitutions, &hashset, 0);

    // See day19.txt for explanation.
    int steps = 0;
    char* l_ptr = line;
    while (*l_ptr) {
        if (*l_ptr == 'Y') {
            steps -= 2;
        } else if ((*l_ptr == 'R') && (*(l_ptr + 1) == 'n')) {
            steps -= 1;
            l_ptr++;
        } else if ((*l_ptr == 'A') && (*(l_ptr + 1) == 'r')) {
            steps -= 1;
            l_ptr++;
        } else if ('a' <= *(l_ptr + 1) && *(l_ptr + 1) <= 'z') {
            l_ptr++;
        }
        steps++;
        l_ptr++;
    }
    steps--;
    printf("Part 2: %d\n", steps);
    return 0;
}
