import copy

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def init_map(bin_length):
    m = dict()
    for i in range(bin_length):
        m[i] = 0
    return m

def decode(dictionary):
    bin_length = len(dictionary)
    gamma = 0
    epsilon = 0
    for i in range(bin_length):
        bit = dictionary[i]
        if bit < 0:
            gamma = gamma << 1
            epsilon = (epsilon << 1) + 1 
        else:
            gamma = (gamma << 1) + 1
            epsilon = epsilon << 1
    
    return (gamma, epsilon)

def get_bit_frequencies(bin_numbers):
    bin_length = len(bin_numbers[0])
    dictionary = init_map(bin_length)
    for line in bin_numbers:
        for i in range(len(line)):
            bit = line[i]
            if (bit == '0'):
                dictionary[i] -= 1
            else:
                dictionary[i] += 1
    return dictionary


def day3a(array):
    dictionary = get_bit_frequencies(array)
    gamma, epsilon = decode(dictionary)
    return gamma * epsilon

def filter_bit(array, bit, index, dictionary=None):
    j = 0
    while (j < len(array)):
        if array[j][index] == bit:
            n = array.pop(j)
            for k in range(len(n)):
                if (n[k] == '0'):
                    dictionary[k] += 1
                else:
                    dictionary[k] -= 1
        else:
            j += 1

def get_oxy_value(array):
    arr = copy.copy(array)
    dictionary = get_bit_frequencies(array)
    i = 0
    while True:
        if len(arr) == 0:
            return None
        if len(arr) == 1:
            return arr[0]
        sign = dictionary[i]
        if sign < 0:
            filter_bit(arr, '1', i, dictionary)
        else:
            filter_bit(arr, '0', i, dictionary)
        i += 1
                
def get_co2_value(array):
    arr = copy.copy(array)
    dictionary = get_bit_frequencies(array)
    i = 0
    while True:
        if len(arr) == 0:
            return None
        if len(arr) == 1:
            return arr[0]
        sign = dictionary[i]
        if sign < 0:
            filter_bit(arr, '0', i, dictionary)
        else:
            filter_bit(arr, '1', i, dictionary)
        i += 1

def day3b(array):

    oxy = get_oxy_value(array)
    co2 = get_co2_value(array)
    return int(oxy, 2) * int(co2, 2)



if __name__ == "__main__":
    filename = "input3.txt"
    arr = arrayise(filename)
    print(day3a(arr))
    print(day3b(arr))


