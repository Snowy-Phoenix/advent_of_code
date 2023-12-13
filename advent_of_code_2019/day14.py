import math
import re
import numpy as np
import itertools


def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day14(array):
    output_ingredients = dict() # key: output
                     # Value: list of 2-tuples of input, quantity
    output_quantities = dict() # Key: Output, quantity of output produced
    for line in array:
        input_chemicals, output_chemicals = line.split(" => ")
        output_quantity, output_chemical_element = output_chemicals.split(" ")
        output_quantity = int(output_quantity)

        input_chemical_list = input_chemicals.split(", ")
        input_tuples = []
        for input_chemical in input_chemical_list:
            input_quantity, input_chemical_element = input_chemical.split(" ")
            input_quantity = int(input_quantity)
            input_tuples.append((input_chemical_element, input_quantity))
        output_ingredients[output_chemical_element] = input_tuples
        output_quantities[output_chemical_element] = output_quantity
    print("Part 1:", calculate_ores("FUEL", 1, output_ingredients, output_quantities, storage=dict()))

    value = 1000000000000
    lower_i = 1
    upper_i = 1
    while calculate_ores("FUEL", upper_i, output_ingredients, output_quantities, storage=dict()) < value:
        upper_i *= 2

    while lower_i != upper_i:
        midpoint = (upper_i + lower_i) // 2
        result = calculate_ores("FUEL", midpoint, output_ingredients, output_quantities, storage=dict())
        if result < value:
            lower_i = midpoint + 1
        else:
            upper_i = midpoint - 1
    print("Part 2:", lower_i)

def calculate_ores(product, quantity, ingredient_map, quantities_map, storage):
    if product in storage:
        if quantity > storage[product]:
            quantity -= storage[product]
            storage[product] = 0
        else:
            storage[product] -= quantity
            return 0
    else:
        storage[product] = 0
    times_made = math.ceil(quantity / quantities_map[product])
    product_excess = quantities_map[product] * times_made - quantity
    storage[product] += product_excess
    ingredients_tuple = ingredient_map[product]
    ores_required = 0
    for ingredient in ingredients_tuple:
        element, quantity = ingredient
        if element == "ORE":
            ores_required += times_made * quantity
        else:
            ores_required += calculate_ores(element, quantity * times_made, ingredient_map, quantities_map, storage)
    return ores_required

if __name__ == "__main__":
    filename = "input14.txt"
    arr = arrayise(filename)

    day14(arr)
    

