def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day6a(array):
    cumsum = 0
    seen_answers = set()
    for line in array:
        if line == "":
            cumsum += len(seen_answers)
            seen_answers.clear()
            continue
        for answer in line:
            seen_answers.add(answer)
    cumsum += len(seen_answers)
    print("Part 1:", cumsum)

def day6b(array):
    cumsum = 0
    common_answers = set()
    curr_answers = set()
    has_answers = False
    for line in array:

        curr_answers.clear()
        if line == "":
            cumsum += len(common_answers)
            common_answers.clear()
            has_answers = False
            continue
        for answer in line:
            curr_answers.add(answer)
        if has_answers:
            common_answers = common_answers.intersection(curr_answers)
        else:
            common_answers = common_answers.union(curr_answers)
            has_answers = True
    cumsum += len(common_answers)
    print("Part 2:", cumsum)

if __name__ == "__main__":
    filename = "input6.txt"
    arr = arrayise(filename)
    day6a(arr)
    day6b(arr)

    
