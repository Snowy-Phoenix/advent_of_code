#include <stdio.h>
#include <stdlib.h>
#define MAX_CHAR 100
#define MAX_NAME_LEN 20
#define MAX_NODES 20


typedef struct Node {
    char name[MAX_NAME_LEN];
    struct Node* edges[MAX_NODES];
    int weights[MAX_NODES];
    int edge_len;
} Node;


char* tokenize(char** string, char* delimiter) {
    if (**string == 0) {
        return NULL;
    }
    char* original_pointer = *string;
    while (**string) {
        int i = 0;
        while (delimiter[i]) {
            if ((*string)[i] == delimiter[i]) {
                i++;
                if (delimiter[i] == 0) {
                    *(*string ) = 0;
                    *string = *string + i;
                    return original_pointer;
                }
                continue;
            } else {
                break;
            }
        }
        *string = *string + 1;
    }
    return original_pointer;
}

int streq(char* c1, char* c2) {
    while (*c1 && *c2) {
        if (*c1 == *c2) {
            c1++;
            c2++;
        } else {
            return 0;
        }
    }
    if (*c1 == 0 && *c2 == 0) {
        return 1;
    }
    return 0;
}

void fill_node_details(Node* n, char* name) {
    n->edge_len = 0;
    int i = 0;
    while (name[i]) {
        n->name[i] = name[i];
        i++;
    }
    n->name[i] = 0;
}

int compute_longest_path(Node* curr_node, Node* nodes, int nlen, Node** visited, int vlen) {
    if (nlen == vlen + 1) {
        return 0;
    }
    int longest = 0;
    if (curr_node == NULL) {
        for (int i = 0; i < nlen; i++) {
            int path = compute_longest_path(nodes + i, nodes, nlen, visited, vlen);
            if (path > longest) {
                longest = path;
            }
        }
    } else {
        for (int i = 0; i < curr_node->edge_len; i++) {
            int unvisited = 1;
            for (int j = 0; j < vlen; j++) {
                if (streq(visited[j]->name, curr_node->edges[i]->name)) {
                    unvisited = 0;
                    break;
                }
            }
            if (unvisited) {
                visited[vlen] = curr_node;
                int path = curr_node->weights[i];
                path += compute_longest_path(curr_node->edges[i], nodes, nlen, visited, vlen + 1);
                if (path > longest) {
                    longest = path;
                }
            }
        }
    }
    return longest;
}

int compute_shortest_path(Node* curr_node, Node* nodes, int nlen, Node** visited, int vlen) {
    if (nlen == vlen + 1) {
        return 0;
    }
    int shortest = __INT_MAX__;
    if (curr_node == NULL) {
        for (int i = 0; i < nlen; i++) {
            int path = compute_shortest_path(nodes + i, nodes, nlen, visited, vlen);
            if (path < shortest) {
                shortest = path;
            }
        }
    } else {
        for (int i = 0; i < curr_node->edge_len; i++) {
            int unvisited = 1;
            for (int j = 0; j < vlen; j++) {
                if (streq(visited[j]->name, curr_node->edges[i]->name)) {
                    unvisited = 0;
                    break;
                }
            }
            if (unvisited) {
                visited[vlen] = curr_node;
                int path = curr_node->weights[i];
                path += compute_shortest_path(curr_node->edges[i], nodes, nlen, visited, vlen + 1);
                if (path < shortest) {
                    shortest = path;
                }
            }
        }
    }
    return shortest;
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input9.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    Node* cities = malloc(MAX_CHAR * sizeof(Node));
    int cities_len = 0;
    char* line = malloc(MAX_CHAR * sizeof(char));
    while (fgets(line, MAX_CHAR, f)) {
        char* c1_name = tokenize(&line, " to ");
        char* c2_name = tokenize(&line, " = ");
        int weight = atoi(tokenize(&line, " to "));
        char c1_i = -1;
        char c2_i = -1;
        int i = 0;
        while ((c1_i == -1 || c2_i == -1) && (i < cities_len)) {
            Node c = cities[i];
            if (streq(c.name, c1_name)) {
                c1_i = i;
            } else if (streq(c.name, c2_name)) {
                c2_i = i;
            }
            i++;
        }
        if (c1_i == -1) {
            c1_i = cities_len;
            fill_node_details(cities + c1_i, c1_name);
            cities_len++;
        }
        if (c2_i == -1) {
            c2_i = cities_len;
            fill_node_details(cities + c2_i, c2_name);
            cities_len++;
        }
        Node* c1 = cities + c1_i;
        Node* c2 = cities + c2_i;
        c1->edges[c1->edge_len] = c2;
        c1->weights[c1->edge_len] = weight;
        c1->edge_len++;
        c2->edges[c2->edge_len] = c1;
        c2->weights[c2->edge_len] = weight;
        c2->edge_len++;

    }

    Node** visited = malloc(MAX_CHAR * sizeof(Node*));
    int shortest = compute_shortest_path(NULL, cities, cities_len, visited, 0);
    int longest = compute_longest_path(NULL, cities, cities_len, visited, 0);
    printf("Part 1: %d\n", shortest);
    printf("Part 2: %d\n", longest);
    free(visited);
    free(cities);
    free(line);
    return 0;
}