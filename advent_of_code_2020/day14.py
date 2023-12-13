import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day14a(array):
    mask = ""
    memory = dict() # Address, value
    for line in array:
        token, value = line.split(" = ")
        if token == "mask":
            mask = value
        else:
            address = re.fullmatch("mem\[(\d+)\]", token).group(1)
            result = 0
            number = int(value)
            for i in range(len(mask)):
                result = result << 1
                bit = number & (1 << (len(mask) - 1 - i))
                bit = bit >> (len(mask) - 1 - i)

                if mask[i] == 'X':
                    result = result + bit
                elif mask[i] == '1':
                    result = result + 1
            memory[address] = result & ((1 << 36) - 1)

    print("Part 1:", sum(memory.values()))

def get_memory_addresses(mask, address):
    
    floating_bits = []
    non_floating_address = 0

    for i in range(len(mask)):
        non_floating_address <<= 1
        shift = 1 << (len(mask) - 1 - i)
        bit = address & (shift)
        bit = bit >> (len(mask) - 1 - i)
        if mask[i] == "0":
            non_floating_address = non_floating_address + bit
        elif mask[i] == "1":
            non_floating_address = non_floating_address + 1
        else:
            floating_bits.append(shift)

    addresses = [non_floating_address]
    while len(floating_bits) > 0:
        floating_bit = floating_bits.pop()
        for i in range(len(addresses)):
            addresses.append(addresses[i] + floating_bit)
    return addresses
                

def day14b(array):
    mask = ""
    memory = dict() # Address, value
    for line in array:
        token, value = line.split(" = ")
        if token == "mask":
            mask = value
        else:
            address = re.fullmatch("mem\[(\d+)\]", token).group(1)
            number = int(value)
            address = int(address)
            memory_addresses = get_memory_addresses(mask, address)
            for a in memory_addresses:
                memory[a] = number
    print("Part 2:", sum(memory.values()))

if __name__ == "__main__":
    filename = "input14.txt"
    arr = arrayise(filename)
    day14a(arr)
    day14b(arr)