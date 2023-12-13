#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_CHAR 512
#define max(a, b) ((a) > (b) ? (a) : (b))
#define min(a, b) ((a) < (b) ? (a) : (b))
#define MISSILE_COST 53
#define DRAIN_COST 73
#define SHIELD_COST 113
#define SHIELD_TURNS 6
#define POISON_COST 173
#define POISON_TURNS 6
#define RECHARGE_COST 229
#define RECHARGE_TURNS 5
#define RECHARGE_AMOUNT 101

struct state {
    int mana;
    int boss_hp;
    int player_hp;
    int shield;
    int poison;
    int recharge;
};

struct queue_node {
    struct queue_node* next;
    int cost;
    struct state state;
};

struct queue_head {
    struct queue_node* last;
    struct queue_node* front;
    int size;
};

void queue_append(struct queue_head* queue, struct queue_node* node) {
    if (queue->size == 0) {
        queue->front = node;
        queue->last = node;
    } else {
        queue->last->next = node;
        queue->last = node;
    }
    queue->size++;
}

int queue_append_state(struct queue_head* queue, struct state* curr_state, int cost) {
    struct queue_node* node = malloc(sizeof(struct queue_node));
    if (node == NULL) {
        printf("Unable to allocate.\n");
        return 0;
    }
    node->next = NULL;
    node->cost = cost;
    node->state.boss_hp = curr_state->boss_hp;
    node->state.player_hp = curr_state->player_hp;
    node->state.shield = curr_state->shield;
    node->state.poison = curr_state->poison;
    node->state.recharge = curr_state->recharge;
    node->state.mana = curr_state->mana;
    queue_append(queue, node);
    return 1;
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

void cpy_state(struct state* from, struct state* to) {
    to->boss_hp = from->boss_hp;
    to->mana = from->mana;
    to->player_hp = from->player_hp;
    to->poison = from->poison;
    to->recharge = from->recharge;
    to->shield = from->shield;
}

void tick_poison(struct state* state) {
    if (state->poison > 0) {
        state->boss_hp = max(state->boss_hp - 3, 0);
        state->poison--;
    }
}
void tick_recharge(struct state* state) {
    if (state->recharge > 0) {
        state->mana += RECHARGE_AMOUNT;
        state->recharge--;
    }
}
void tick_shield(struct state* state) {
    if (state->shield > 0) {
        state->shield--;
    }
}
void tick_boss_turn(struct state* state, int boss_damage) {
    tick_poison(state);
    tick_recharge(state);
    tick_shield(state);
    if (state->boss_hp == 0) {
        // Boss died to poison damage
        return;
    }
    int armour = (state->shield > 0 ? 7 : 0);
    state->player_hp = max(0, state->player_hp - max(1, boss_damage - armour));
}

void use_magic_missile(struct state* curr_state, int curr_cost, 
                       struct state* next_states, int* next_costs,
                       int boss_damage) {
    cpy_state(curr_state, next_states);
    tick_poison(next_states);
    tick_recharge(next_states);
    tick_shield(next_states);
    if (next_states->boss_hp == 0) {
        // Boss died to poison damage
        *next_costs = curr_cost;
        return;
    }
    if (next_states->mana < MISSILE_COST) {
        // Out of mana
        *next_costs = -1;
        return;
    }
    next_states->boss_hp = max(next_states->boss_hp - 4, 0);
    next_states->mana -= MISSILE_COST;
    *next_costs = curr_cost + MISSILE_COST;
    tick_boss_turn(next_states, boss_damage);
    if (next_states->player_hp == 0) {
        // Player died
        *next_costs = -1;
    }
}
void use_drain(struct state* curr_state, int curr_cost, 
               struct state* next_states, int* next_costs,
               int boss_damage) {
    cpy_state(curr_state, next_states);
    tick_poison(next_states);
    tick_recharge(next_states);
    tick_shield(next_states);
    if (next_states->boss_hp == 0) {
        // Boss died to poison damage
        *next_costs = curr_cost;
        return;
    }
    if (next_states->mana < DRAIN_COST) {
        // Out of mana
        *next_costs = -1;
        return;
    }
    next_states->boss_hp = max(next_states->boss_hp - 2, 0);
    next_states->player_hp += 2;
    next_states->mana -= DRAIN_COST;
    *next_costs = curr_cost + DRAIN_COST;
    tick_boss_turn(next_states, boss_damage);
    if (next_states->player_hp == 0) {
        // Player died
        *next_costs = -1;
    }
}
void use_shield(struct state* curr_state, int curr_cost, 
               struct state* next_states, int* next_costs,
               int boss_damage) {
    cpy_state(curr_state, next_states);
    tick_poison(next_states);
    tick_recharge(next_states);
    tick_shield(next_states);
    if (next_states->boss_hp == 0) {
        // Boss died to poison damage
        *next_costs = curr_cost;
        return;
    }
    if (next_states->mana < SHIELD_COST || next_states->shield > 0) {
        // Out of mana or ability already active
        *next_costs = -1;
        return;
    }
    *next_costs = curr_cost + SHIELD_COST;
    next_states->mana -= SHIELD_COST;
    next_states->shield = SHIELD_TURNS;
    tick_boss_turn(next_states, boss_damage);
    if (next_states->player_hp == 0) {
        // Player died
        *next_costs = -1;
    }
}
void use_poison(struct state* curr_state, int curr_cost, 
                struct state* next_states, int* next_costs,
                int boss_damage) {
    cpy_state(curr_state, next_states);
    tick_poison(next_states);
    tick_recharge(next_states);
    tick_shield(next_states);
    if (next_states->boss_hp == 0) {
        // Boss died to poison damage
        *next_costs = curr_cost;
        return;
    }
    if (next_states->mana < POISON_COST || next_states->poison > 0) {
        // Out of mana or ability already active
        *next_costs = -1;
        return;
    }
    *next_costs = curr_cost + POISON_COST;
    next_states->poison = POISON_TURNS;
    next_states->mana -= POISON_COST;
    tick_boss_turn(next_states, boss_damage);
    if (next_states->player_hp == 0) {
        // Player died
        *next_costs = -1;
    }
}
void use_recharge(struct state* curr_state, int curr_cost, 
                  struct state* next_states, int* next_costs,
                  int boss_damage) {
    cpy_state(curr_state, next_states);
    tick_poison(next_states);
    tick_recharge(next_states);
    tick_shield(next_states);
    if (next_states->boss_hp == 0) {
        // Boss died to poison damage
        *next_costs = curr_cost;
        return;
    }
    if (next_states->mana < RECHARGE_COST || next_states->recharge > 0) {
        // Out of mana or ability already active
        *next_costs = -1;
        return;
    }
    *next_costs = curr_cost + RECHARGE_COST;
    next_states->recharge = RECHARGE_TURNS;
    next_states->mana -= RECHARGE_COST;
    tick_boss_turn(next_states, boss_damage);
    if (next_states->player_hp == 0) {
        // Player died
        *next_costs = -1;
    }
}

void get_next_states(struct state* curr_state, int curr_cost, 
                     struct state* next_states, int* next_costs,
                     int boss_damage) {
    use_magic_missile(curr_state, curr_cost, 
                      next_states, next_costs, boss_damage);
    use_drain(curr_state, curr_cost, 
              next_states + 1, next_costs + 1, boss_damage);
    use_shield(curr_state, curr_cost, 
               next_states + 2, next_costs + 2, boss_damage);
    use_poison(curr_state, curr_cost, 
               next_states + 3, next_costs + 3, boss_damage);
    use_recharge(curr_state, curr_cost, 
                 next_states + 4, next_costs + 4, boss_damage);
}

void print_state(struct state* state) {
    printf("Player has %d hp, %d mana\n", state->player_hp, state->mana);
    printf("Boss has %d hp\n", state->boss_hp);
    printf("Poison timer is %d\n", state->poison);
    printf("Recharge timer is %d\n", state->recharge);
    printf("Shield timer is %d\n", state->shield);
}

int is_boss_dead(struct queue_node* node) {
    return node->state.boss_hp == 0;
}

int simulate(struct state* init_state, int boss_damage, int hard_mode) {
    struct queue_head queue;
    int curr_cost = 0;
    int next_costs[5] = {-1, -1, -1, -1, -1};
    struct state next_states[5];
    int best_cost = __INT32_MAX__;

    queue.size = 0;
    queue_append_state(&queue, init_state, 0);
    while (queue.size) {
        struct queue_node* curr_node = queue_pop(&queue);
        if (curr_node == NULL) {
            puts("Null node in queue!");
            return -1;
        }
        if (is_boss_dead(curr_node)) {
            best_cost = min(best_cost, curr_node->cost);
            free(curr_node);
            continue;
        }
        if (hard_mode) {
            curr_node->state.player_hp--;
            if (curr_node->state.player_hp == 0) {
                // Player died to hard mode.
                free(curr_node);
                continue;
            }
        }
        curr_cost = curr_node->cost;
        get_next_states(&curr_node->state, curr_cost, next_states, 
                        next_costs, boss_damage);
        for (int i = 0; i < 5; i++) {
            if (next_costs[i] == -1 || next_costs[i] >= best_cost) {
                // Disallow illegal and moves that cost more mana than the best cost.
                continue;
            }
            queue_append_state(&queue, next_states + i, next_costs[i]);
        }
        free(curr_node);
    }
    return best_cost;
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input22.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        puts("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    int boss_hp;
    int boss_damage;
    int player_hp = 50;
    int player_mana = 500;

    if (!fscanf(f, "Hit Points: %d\n", &boss_hp) ||
        !fscanf(f, "Damage: %d\n", &boss_damage)) {
            puts("Unable to parse input.");
            return -1;
        };
    fclose(f);

    struct state init_state;
    init_state.boss_hp = boss_hp;
    init_state.mana = player_mana;
    init_state.player_hp = player_hp;
    init_state.poison = 0;
    init_state.recharge = 0;
    init_state.shield = 0;

    int best_cost_part1 = simulate(&init_state, boss_damage, 0);
    printf("Part 1: %d\n", best_cost_part1);
    int best_cost_part2 = simulate(&init_state, boss_damage, 1);
    printf("Part 2: %d\n", best_cost_part2);
    return 0;
}
