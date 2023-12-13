import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def clean_bag_names(name):
    b = name.rstrip(".")
    b = b.rstrip("s")
    b = b.rstrip(" bag")
    digit = 0
    if (name[0].isdigit()):
        b = b[2:]
        digit = int(name[0])
    return (b, digit)

def day7(array):
    parent_map = dict() # bag colour, set of bags
    child_map = dict() # bag colour, dict of bags and quantities
    for line in array:
        bags = line.split(" contain ")
        contained_bags = bags[1]
        curr_bag = clean_bag_names(bags[0])[0]

        if curr_bag not in parent_map:
            parent_map[curr_bag] = set()
        if curr_bag not in child_map:
            child_map[curr_bag] = dict()

        if (contained_bags != "no other bags."):
            raw_contained_bags_arr = contained_bags.split(", ")
            contained_bags_arr = []
            amount = 0
            for bag in raw_contained_bags_arr:
                b, amount = clean_bag_names(bag)
                contained_bags_arr.append(b)
                child_map[curr_bag][b] = amount
            for bag in contained_bags_arr:
                if bag in parent_map:
                    parent_map[bag].add(curr_bag)
                else:
                    parent_map[bag] = (set([curr_bag]))
    
    total = 0
    seen_parents = set(["shiny gold"])
    stack = ["shiny gold"]
    while (len(stack) > 0):
        curr_bag = stack.pop()
        seen_parents.add(curr_bag)
        for parent in parent_map[curr_bag]:
            if parent not in seen_parents:
                total += 1
                seen_parents.add(parent)
                stack.append(parent)
    print("Part 1:", total)

    total = 0
    queue = {"shiny gold":1} # Bag, quantity of that bag
    while (len(queue) > 0):
        curr_bag, quantity = queue.popitem()
        for child in child_map[curr_bag]:
            total += child_map[curr_bag][child] * quantity
            if (child in queue):
                queue[child] += child_map[curr_bag][child] * quantity
            else:
                queue[child] = child_map[curr_bag][child] * quantity
    print("Part 2:", total)



if __name__ == "__main__":
    filename = "input7.txt"
    arr = arrayise(filename)
    day7(arr)

    
