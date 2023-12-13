#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_CHAR 512
#define max(a, b) ((a) > (b) ? (a) : (b))
#define min(a, b) ((a) < (b) ? (a) : (b))

int simulate(int bhp, int bdmg, int bdef, int php, int pdmg, int pdef) {
    while (1) {
        bhp -= max(pdmg - bdef, 1);
        if (bhp <= 0) {
            return 1;
        }
        php -= max(bdmg - pdef, 1);
        if (php <= 0) {
            return 0;
        }
    }
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input21.txt", "r");
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
    int boss_armour;
    int player_hp = 100;
    if (!fscanf(f, "Hit Points: %d\n", &boss_hp) ||
        !fscanf(f, "Damage: %d\n", &boss_damage) ||
        !fscanf(f, "Armor: %d", &boss_armour)) {
            puts("Unable to parse input.");
            return -1;
        };
    fclose(f);

    char* weapon_name[5] = {"Dagger", "Shortsword", "Warhammer", "Longsword", "Greataxe"};
    int weapon_cost[5] = {8,10,25,40,74};
    int weapon_damage[5] = {4,5,6,7,8};
    char* armour_name[6] = {"None", "Leather", "Splintmail", "Bandedmail", "Platemail"};
    int armour_cost[6] = {0,13,31,53,75,102};
    int armour_defence[6] = {0,1,2,3,4,5};
    char* ring_name[7] = {"Nothing", "Damage +1", "Damage +2", "Damage +3", "Defense +1", "Defense +2", "Defense +3"};
    int ring_cost[7] = {0,25,50,100,20,40,80};
    int ring_damage[7] = {0,1,2,3,0,0,0};
    int ring_defence[7] = {0,0,0,0,1,2,3};

    int min_cost = __INT_MAX__;
    int min_armour;
    int min_weapon;
    int min_ring1;
    int min_ring2;
    int max_cost = 0;
    int max_armour;
    int max_weapon;
    int max_ring1;
    int max_ring2;
    for (int weapon_i = 0; weapon_i < 5; weapon_i++) {
        for (int armour_i = 0; armour_i < 6; armour_i++) {
            for (int ring1_i = 0; ring1_i < 7; ring1_i++) {
               for (int ring2_i = 0; ring2_i < 7; ring2_i++) {
                    if (ring1_i == ring2_i && ring1_i != 0) {
                        continue;
                    }
                    int total_cost = weapon_cost[weapon_i]
                                     + armour_cost[armour_i]
                                     + ring_cost[ring1_i]
                                     + ring_cost[ring2_i];
                    int total_damage = weapon_damage[weapon_i]
                                       + ring_damage[ring1_i]
                                       + ring_damage[ring2_i];
                    int total_defence = armour_defence[armour_i]
                                        + ring_defence[ring1_i]
                                        + ring_defence[ring2_i];
                    if (simulate(boss_hp, boss_damage, boss_armour,
                                 player_hp, total_damage, total_defence)) {
                        if (min_cost > total_cost) {
                            min_cost = total_cost;
                            min_armour = armour_i;
                            min_weapon = weapon_i;
                            min_ring1 = ring1_i;
                            min_ring2 = ring2_i;
                        }
                    } else {
                        if (max_cost < total_cost) {
                            max_cost = total_cost;
                            max_armour = armour_i;
                            max_weapon = weapon_i;
                            max_ring1 = ring1_i;
                            max_ring2 = ring2_i;
                        }
                    }
                } 
            }
        }
    }

    printf("Part 1: %d\n", min_cost);
    printf("Selection:\nWeapon: %s\nArmour: %s\nRing 1: %s\nRing 2: %s\n\n",
           weapon_name[min_weapon],
           armour_name[min_armour],
           ring_name[min_ring1],
           ring_name[min_ring2]);
    printf("Part 2: %d\n", max_cost);
    printf("Selection:\nWeapon: %s\nArmour: %s\nRing 1: %s\nRing 2: %s\n\n",
           weapon_name[max_weapon],
           armour_name[max_armour],
           ring_name[max_ring1],
           ring_name[max_ring2]);

    return 0;
}
