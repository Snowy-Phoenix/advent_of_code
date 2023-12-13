#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_CHAR 100

struct Gate;
struct Wire;
struct GateList;

enum operator {AND, OR, LSHIFT, RSHIFT, NOT};

typedef struct Gate {
    u_int16_t (*operation)(u_int16_t, u_int16_t);
    struct Wire* input1;
    struct Wire* input2;
    struct Wire* output;
} Gate;

typedef struct Wire {
    u_int16_t signal;
    u_int32_t identifier;
    struct Gate* source;
    struct GateList* destination;
    char evaluated;
} Wire;

typedef struct GateList {
    Gate** gates;
    int len;
    int arr_len;
} GateList;

typedef struct WireMap {
    Wire** wires;
    int len;
} WireMap;

u_int16_t and(u_int16_t i, u_int16_t j) {
    return i & j;
}
u_int16_t or(u_int16_t i, u_int16_t j) {
    return i | j;
}
u_int16_t not(u_int16_t i, u_int16_t j) {
    return ~i;
}
u_int16_t lshift(u_int16_t i, u_int16_t j) {
    return i << j;
}
u_int16_t rshift(u_int16_t i, u_int16_t j) {
    return i >> j;
}

GateList* create_gate_list(int len) {
    GateList* list = malloc(sizeof(GateList));
    list->arr_len = len;
    list->len = 0;
    list->gates = malloc(len * sizeof(Gate**));
    return list;
}

void add_gate(GateList* list, Gate* gate) {
    if (list->len == list->arr_len) {
        list->gates = realloc(list->gates, 2 * list->arr_len * sizeof(Gate**));
        list->arr_len *= 2; 
    }
    list->gates[list->len] = gate;
    list->len++;
}

int parse_literal(char** line) {
    int dest = 0;
    while(**line) {
        char d = **line;
        if (d == ' ') {
            *line = *line + 1;
            break;
        }
        dest = (dest * 10) + (d - '0');
        *line = *line + 1;
    }
    return dest;
}

int parse_identifier(char** line) {
    int id = 0;
    while (**line) {
        char c = **line;
        if (c == 0) {
            break;
        }
        if (0 <= c - 'a' && c - 'a' < 26) {
            id = (id*26) + (c - 'a') + 1;
            *line = *line + 1;
        } else {
            *line = *line + 1;
            break;
        }
    }
    return id;
}

enum operator parse_operator(char** line) {
    if (**line == 'O') {
        *line = *line + 3;
        return OR;
    } else if (**line == 'A') {
        *line = *line + 4;
        return AND;
    } else if (**line == 'L') {
        *line = *line + 7;
        return LSHIFT;
    } else {
        *line = *line + 7;
        return RSHIFT;
    }
}

void add_wire(Wire* w, WireMap* wires) {
    int hash = w->identifier;
    if (wires->len < hash) {
        int new_len = 2 * hash;
        wires->wires = realloc(wires->wires, new_len * sizeof(Wire**));
    }
    wires->wires[w->identifier] = w;
}

Wire* create_wire(int id) {
    Wire* w = malloc(sizeof(Wire));
    w->destination = create_gate_list(5);
    w->source = NULL;
    w->identifier = id;
    w->signal = 0;
    w->evaluated = 0;
    return w;
}

Wire* get_wire(int id, WireMap* wires) {
    if (id < 0) {
        return NULL;
    } else if (id > wires->len) {
        Wire* w = create_wire(id);
        add_wire(w, wires);
        return w;
    } else if (wires->wires[id]) {
        return wires->wires[id];
    } else {
        Wire* w = create_wire(id);
        add_wire(w, wires);
        return w;
    }
}

u_int16_t (*get_operation(enum operator op))(u_int16_t, u_int16_t) {
    switch(op) {
        case AND:
            return &and;
        case OR:
            return &or;
        case LSHIFT:
            return &lshift;
        case RSHIFT:
            return &rshift;
        case NOT:
            return &not;
    }
    return NULL;
}

void parse_ins(char* line, WireMap* wires) {
    char c = *line;
    if (0 <= c - '0' && c - '0' <= 9) {
        int literal = parse_literal(&line);
        if (*line == '-') {
            line += 3;
            Wire* w = get_wire(parse_identifier(&line), wires);
            w->source = NULL;
            w->signal = literal;
        } else {
            enum operator op = parse_operator(&line);
            Wire* w1 = create_wire(0);
            w1->signal = literal;
            Wire* w2 = get_wire(parse_identifier(&line), wires);
            line += 3;
            Wire* out_wire = get_wire(parse_identifier(&line), wires);
            Gate* g = malloc(sizeof(Gate));
            g->input1 = w1;
            g->input2 = w2;
            g->operation = get_operation(op);
            g->output = out_wire;
            add_gate(w1->destination, g);
            add_gate(w2->destination, g);
            out_wire->source = g;
        }
    }else if (0 <= c - 'a' && c - 'a' < 26) {
        Wire* w1 = get_wire(parse_identifier(&line), wires);
        Wire* w2;
        enum operator op = parse_operator(&line);
        if (op == LSHIFT || op == RSHIFT) {
            w2 = create_wire(0);
            w2->signal = parse_literal(&line);
        } else {
            w2 = get_wire(parse_identifier(&line), wires);
        }
        line += 3;
        Wire* out_wire = get_wire(parse_identifier(&line), wires);
        Gate* g = malloc(sizeof(Gate));
        g->input1 = w1;
        g->input2 = w2;
        g->output = out_wire;
        g-> operation = get_operation(op);
        add_gate(w1->destination, g);
        add_gate(w2->destination, g);
        out_wire->source = g;
    } else {
        Gate* g = malloc(sizeof(Gate));
        line += 4;
        Wire* w = get_wire(parse_identifier(&line), wires);
        line += 3;
        Wire* out = get_wire(parse_identifier(&line), wires);
        g->input1 = w;
        g->input2 = NULL;
        g->operation = &not;
        g->output = out;
        add_gate(w->destination, g);
        out->source = g;
    }
}

int evaluate(Wire* w) {
    if (w == NULL) {
        return 0;
    }
    if (w->evaluated) {
        return w->signal;
    }
    Gate* source = w->source;
    if (source == NULL) {
        return w->signal;
    }
    u_int16_t w1_signal = evaluate(source->input1);
    u_int16_t w2_signal = evaluate(source->input2);
    w->signal = source->operation(w1_signal, w2_signal);
    w->evaluated = 1;
    return w->signal;

}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input7.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    WireMap wires;
    wires.len = 27*27;
    wires.wires = calloc(27*27, sizeof(Wire**));
    while (fgets(line, MAX_CHAR, f)) {
        parse_ins(line, &wires);

    }
    printf("Part 1: %d\n", evaluate(get_wire(1, &wires)));
    return 0;
}