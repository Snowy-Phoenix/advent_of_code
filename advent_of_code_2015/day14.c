#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHAR 2048
#define MAX_NAME_LEN 64
#define max(a, b) ((a) > (b) ? (a) : (b))

enum status {RUNNING, SLEEPING};

struct reindeer {
    int distance;
    int sleep_clock;
    int run_clock;
    int speed;
    int sleep_time;
    int run_time;
    enum status status;
};

struct reindeer_list {
    struct reindeer* reindeer;
    struct reindeer_list* next;
};

void add_reindeer(struct reindeer_list* list, int speed, int run_time, int sleep_time) {
    struct reindeer* reindeer;
    if (list->reindeer == NULL) {
        list->reindeer = malloc(sizeof(struct reindeer));
    } else {
        while (list->next != NULL) {
            list = list->next;
        }
        list->next = malloc(sizeof(struct reindeer_list));
        list = list->next;
        list->reindeer = malloc(sizeof(struct reindeer));
        list->next = NULL;
    }
    reindeer = list->reindeer;

    reindeer->distance = 0;
    reindeer->run_clock = run_time;
    reindeer->run_time = run_time;
    reindeer->sleep_clock = 0;
    reindeer->sleep_time = sleep_time;
    reindeer->speed = speed;
    reindeer->status = RUNNING;
}

void tick(struct reindeer* reindeer) {
    if (reindeer->status == RUNNING) {
        if (reindeer->run_clock) {
            reindeer->distance += reindeer->speed;
            reindeer->run_clock--;
        } else {
            reindeer->status = SLEEPING;
            reindeer->sleep_clock = reindeer->sleep_time - 1;
        }
    } else {
        if (reindeer->sleep_clock) {
            reindeer->sleep_clock--;
        } else {
            reindeer->status = RUNNING;
            reindeer->run_clock = reindeer->run_time - 1;
            reindeer->distance += reindeer->speed;
        }
    }
}

int get_max_distance(struct reindeer_list* reindeers) {
    int maximum = 0;
    while (reindeers) {
        maximum = max(maximum, reindeers->reindeer->distance);
        reindeers = reindeers->next;
    }
    return maximum;
}

void simulate(struct reindeer_list* reindeers, int time, int n_reindeers) {
    struct reindeer_list* reindeer;
    int* scores = calloc(n_reindeers, sizeof(int));
    for (int i = 0; i < time; i++) {
        reindeer = reindeers;
        while (reindeer) {
            tick(reindeer->reindeer);
            reindeer = reindeer->next;
        }

        int max_distance = get_max_distance(reindeers);
        int j = 0;
        reindeer = reindeers;
        while (reindeer) {
            scores[j] += reindeer->reindeer->distance == max_distance;
            j++;
            reindeer = reindeer->next;
        }
    }
    int maximum = get_max_distance(reindeers);
    printf("Part 1: %d\n", maximum);

    maximum = 0;
    for (int i = 0; i < n_reindeers; i++) {
        maximum = max(maximum, scores[i]);
    }
    printf("Part 2: %d\n", maximum);
}

int main(int argc, char** argv) {
    FILE* f;
    if (argc == 1) {
        f = fopen("input14.txt", "r");
    } else {
        f = fopen(argv[1], "r");
    }
    if (f == NULL) {
        printf("Unable to open file.");
        return -1;
    }
    char line[MAX_CHAR];
    struct reindeer_list reindeers = {0};
    int n_reindeers = 0;
    while (fgets(line, MAX_CHAR, f)) {
        int speed;
        int run_time;
        int sleep_time;
        char* line_ptr = line;
        while (*line_ptr != ' ') {
            line_ptr++;
        }
        sscanf(line_ptr, " can fly %d km/s for %d seconds, but then must rest for %d seconds.\n", &speed, &run_time, &sleep_time);
        add_reindeer(&reindeers, speed, run_time, sleep_time);
        n_reindeers++;
    }
    fclose(f);
    simulate(&reindeers, 2503, n_reindeers);
    return 0;
}
