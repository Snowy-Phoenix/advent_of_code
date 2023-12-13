#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048
#define max(a, b) ((a) > (b) ? (a) : (b))

enum instruction {hlf, tpl, inc, jmp, jie, jio};
enum param_type {REGA, REGB, VAL};

struct param {
    enum param_type type;
    long value;
};

struct line {
    struct line* prev;
    struct line* next;
    enum instruction type;
    struct param param1;
    struct param param2;
};

struct computer {
    struct line* current_line;
    unsigned long reg_a;
    unsigned long reg_b;
    int halted;
};

void init_computer(struct computer* computer) {
    computer->reg_a = 0;
    computer->reg_b = 0;
    computer->current_line = NULL;
    computer->halted = 0;
}

enum instruction parse_instruct(char* instruct_str) {
    if (instruct_str == NULL) {
        return -1;
    } else if (strcmp(instruct_str, "hlf") == 0) {
        return hlf;
    } else if (strcmp(instruct_str, "tpl") == 0) {
        return tpl;
    } else if (strcmp(instruct_str, "inc") == 0) {
        return inc;
    } else if (strcmp(instruct_str, "jmp") == 0) {
        return jmp;
    } else if (strcmp(instruct_str, "jie") == 0) {
        return jie;
    } else if (strcmp(instruct_str, "jio") == 0) {
        return jio;
    }
    return -1;
    
}
struct param parse_param(char* param_str) {
    struct param param;
    if (param_str == NULL) {
        param.type = -1;
        return param;
    } else if (*param_str == 0) {
        param.type = -1;
        return param;
    } else if (strcmp(param_str, "a") == 0) {
        param.type = REGA;
        return param;
    } else if (strcmp(param_str, "b") == 0) {
        param.type = REGB;
        return param;
    } else {
        char* endstr;
        long value = strtol(param_str, &endstr, 10);
        if (*endstr == 0 || *endstr == '\n') {
            param.type = VAL;
            param.value = value;
            return param;
        } else {
            param.type = -1;
            return param;
        }
    }
}

struct line* parse_line(char* raw_line, struct line* last_line) {
    struct line* parsed_line = malloc(sizeof(struct line));
    parsed_line->prev = last_line;
    parsed_line->next = NULL;
    if (last_line) {
        last_line->next = parsed_line;
    }
    char delineators[] = " ,+\n";
    char* instruct_str = strtok(raw_line, delineators);
    enum instruction instruct = parse_instruct(instruct_str);
    if (instruct == -1) {
        printf("Invalid instruction %s\n", raw_line);
        return NULL;
    }
    char* param1_str = strtok(NULL, delineators);
    struct param param1 = parse_param(param1_str);
    if (param1.type == -1) {
        printf("Invalid param %s\n", raw_line);
        return NULL;
    }
    char* param2_str = strtok(NULL, delineators);
    struct param param2 = parse_param(param2_str);

    parsed_line->param1 = param1;
    parsed_line->param2 = param2;
    parsed_line->type = instruct;
    return parsed_line;
}

void run_hlf(struct computer* computer) {
    switch (computer->current_line->param1.type) {
        case REGA:
            computer->reg_a /= 2;
            break;
        case REGB:
            computer->reg_b /= 2;
            break;
        default:
            computer->halted = 1;
            printf("HLF: Invalid parameter %d\n", computer->current_line->param1.type);
            return;
    }
    computer->current_line = computer->current_line->next;
}
void run_tpl(struct computer* computer) {
    switch (computer->current_line->param1.type) {
        case REGA:
            computer->reg_a *= 3;
            break;
        case REGB:
            computer->reg_b *= 3;
            break;
        default:
            computer->halted = 1;
            printf("TPL: Invalid parameter %d\n", computer->current_line->param1.type);
            return;
    }
    computer->current_line = computer->current_line->next;
}
void run_inc(struct computer* computer) {
    switch (computer->current_line->param1.type) {
        case REGA:
            computer->reg_a++;
            break;
        case REGB:
            computer->reg_b++;
            break;
        default:
            computer->halted = 1;
            printf("TPL: Invalid parameter %d\n", computer->current_line->param1.type);
            return;
    }
    computer->current_line = computer->current_line->next;
}
void run_jmp(struct computer* computer) {
    if (computer->current_line->param1.type != VAL) {
        computer->halted = 1;
        printf("JMP: Invalid parameter %d\n", computer->current_line->param1.type);
        return;
    }
    long offset = computer->current_line->param1.value;
    while (offset > 0) {
        if (computer->current_line == NULL) {
            computer->halted = 1;
            return;
        }
        computer->current_line = computer->current_line->next;
        offset--;
    }
    while (offset < 0) {
        if (computer->current_line == NULL) {
            computer->halted = 1;
            return;
        }
        computer->current_line = computer->current_line->prev;
        offset++;
    }
}
void run_jie(struct computer* computer) {
    int reg_val;
    switch (computer->current_line->param1.type) {
        case REGA:
            reg_val = computer->reg_a;
            break;
        case REGB:
            reg_val = computer->reg_b;
            break;
        default:
            computer->halted = 1;
            printf("JIE: Invalid parameter1 %d\n", computer->current_line->param1.type);
            return;
    }
    if (computer->current_line->param2.type != VAL) {
        computer->halted = 1;
        printf("JIE: Invalid parameter2 %d\n", computer->current_line->param2.type);
        return;
    }
    if (reg_val % 2 != 0) {
        computer->current_line = computer->current_line->next;
        return;
    } 
    long offset = computer->current_line->param2.value;
    while (offset > 0) {
        if (computer->current_line == NULL) {
            computer->halted = 1;
            return;
        }
        computer->current_line = computer->current_line->next;
        offset--;
    }
    while (offset < 0) {
        if (computer->current_line == NULL) {
            computer->halted = 1;
            return;
        }
        computer->current_line = computer->current_line->prev;
        offset++;
    }
}
void run_jio(struct computer* computer) {
    int reg_val;
    switch (computer->current_line->param1.type) {
        case REGA:
            reg_val = computer->reg_a;
            break;
        case REGB:
            reg_val = computer->reg_b;
            break;
        default:
            computer->halted = 1;
            printf("JIE: Invalid parameter1 %d\n", computer->current_line->param1.type);
            return;
    }
    if (computer->current_line->param2.type != VAL) {
        computer->halted = 1;
        printf("JIE: Invalid parameter2 %d\n", computer->current_line->param2.type);
        return;
    }
    if (reg_val != 1) {
        computer->current_line = computer->current_line->next;
        return;
    } 
    long offset = computer->current_line->param2.value;
    while (offset > 0) {
        if (computer->current_line == NULL) {
            computer->halted = 1;
            return;
        }
        computer->current_line = computer->current_line->next;
        offset--;
    }
    while (offset < 0) {
        if (computer->current_line == NULL) {
            computer->halted = 1;
            return;
        }
        computer->current_line = computer->current_line->prev;
        offset++;
    }
}

void print_instruction(struct line* instruct) {
    switch(instruct->type) {
        case hlf:
            printf("HLF ");
            break;
        case tpl:
            printf("TPL ");
            break;
        case inc:
            printf("INC ");
            break;
        case jmp:
            printf("JMP ");
            break;
        case jie:
            printf("JIE ");
            break;
        case jio:
            printf("JIO ");
            break;
    }
}

void run(struct computer* computer) {
    while (!computer->halted) {
        if (computer->current_line == NULL) {
            computer->halted = 1;
            return;
        }
        switch (computer->current_line->type) {
            case hlf:
                run_hlf(computer);
                break;
            case tpl:
                run_tpl(computer);
                break;
            case inc:
                run_inc(computer);
                break;
            case jmp:
                run_jmp(computer);
                break;
            case jie:
                run_jie(computer);
                break;
            case jio:
                run_jio(computer);
                break;
            default:
                computer->halted = 1;
                printf("Computer encountered an unknown instruction %d\n", 
                computer->current_line->type);
        }
    }
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input23.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    struct computer computer;
    struct line* first_line;
    init_computer(&computer);
    struct line* last_line = NULL;
    struct line* curr_line;
    while (fgets(line, MAX_CHAR, f)) {
        curr_line = parse_line(line, last_line);
        if (computer.current_line == NULL) {
            computer.current_line = curr_line;
            first_line = curr_line;
        }
        last_line = curr_line;
    }
    fclose(f);

    run(&computer);
    printf("Part 1: %d\n", computer.reg_b);
    init_computer(&computer);
    computer.current_line = first_line;
    computer.reg_a = 1;
    run(&computer);
    printf("Part 2: %d\n", computer.reg_b);
    return 0;
}
