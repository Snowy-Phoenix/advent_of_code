import copy

class LanturnFishSimulator:

    def __init__(self, start):
        self.numbers = dict() # key: Stage, Value: Number of fish at that stage
        for i in start:
            n = int(i)
            if self.numbers.get(n):
                self.numbers[n] += 1
            else:
                self.numbers[n] = 1

    def simulate_days(self, time):
        prev_generation = copy.copy(self.numbers)
        for i in range(time):
            new_generation = dict()
            for i in range(9):
                new_generation[i] = 0
            for stage in prev_generation.keys():
                if stage == 0:
                    new_generation[6] += prev_generation[stage]
                    new_generation[8] += prev_generation[stage]
                else:
                    new_generation[stage - 1] += prev_generation[stage]
            prev_generation = new_generation
        return LanturnFishSimulator.get_total_fish(new_generation)

    def get_total_fish(fish_numbers):
        total = 0
        for i in fish_numbers.values():
            total += i
        return total

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day6(arr):
    initial = arr[0].split(',')
    simulator = LanturnFishSimulator(initial)
    print(simulator.simulate_days(80))
    print(simulator.simulate_days(256))
    print(simulator.simulate_days(1028))




if __name__ == "__main__":
    filename = "input6.txt"
    arr = arrayise(filename)
    day6(arr)
