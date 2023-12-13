def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(int(line.strip()))
    return array

def day1a(array):
    total_increases = 0
    a = array[0]
    for n in array[1:]:
        b = n
        if (a < b):
            total_increases += 1
        a = b
    return total_increases
        
def day1b(array):
    total_increases = 0
    sum_before = 2**31
    for i in range(2, len(array)):
        sum = array[i] + array[i - 1] + array[i - 2]
        if (sum_before < sum):
            total_increases += 1
        sum_before = sum
    return total_increases

if __name__ == '__main__':
    filename = "input1.txt"
    arr = arrayise(filename)
    print("Part 1: " + str(day1a(arr)))
    print("Part 2: " + str(day1b(arr)))
    