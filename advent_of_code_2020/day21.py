import re
import numpy as np

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array


def day21(array):

    all_ingredients = dict() # ingredient, occurrences
    all_allergens = dict() # Allergen, set of ingredients
    for line in array:
        re_groups = re.fullmatch("(^[\\w ]+)(\\([\\w, ]+\\))", line)
        ingredients = re_groups.group(1).strip()
        ingredients_list = ingredients.split(' ')
        allergens = re_groups.group(2)
        allergens = re.match("\\(contains (.+)\\)", allergens).group(1)
        allergens_list = allergens.split(", ")

        for ingredient in ingredients_list:
            if ingredient in all_ingredients:
                all_ingredients[ingredient] += 1
            else:
                all_ingredients[ingredient] = 1
        for allergen in allergens_list:
            if allergen not in all_allergens:
                all_allergens[allergen] = set(ingredients_list)
            else:
                all_allergens[allergen] = all_allergens[allergen].intersection(ingredients_list)
    
    safe_ingredients = set(all_ingredients)
    for allergen in all_allergens:
        safe_ingredients = safe_ingredients.difference(all_allergens[allergen])
    cumsum = 0
    for ingredient in safe_ingredients:
        cumsum += all_ingredients[ingredient]
    print("Part 1:", cumsum)

    changed = True
    while changed:
        changed = False
        for allergen1 in all_allergens:
            ingredients1 = all_allergens[allergen1]
            if len(ingredients1) == 1:
                for allergen2 in all_allergens:
                    if allergen1 != allergen2:
                        ingredients2 = all_allergens[allergen2]
                        if len(ingredients1.intersection(ingredients2)) != 0:
                            changed = True
                            all_allergens[allergen2] = ingredients2.difference(ingredients1)

    allergen_names = sorted(all_allergens.keys())
    final_string = ""
    for i in range(len(allergen_names)):
        allergen = allergen_names[i]
        final_string += list(all_allergens[allergen])[0]
        if i != len(allergen_names) - 1:
            final_string += ","
    print("Part 2:", final_string)

if __name__ == "__main__":
    filename = "input21.txt"
    arr = arrayise(filename)
    day21(arr)
