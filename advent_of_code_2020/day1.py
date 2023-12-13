def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def get2(array, sum):
    numbers = set()  
    for n in array:
        if sum - n in numbers:
            return (sum - n, n)
        else:
            numbers.add(n)
    return None

def get3(array, sum):
    numbers = set(array)
    for n in numbers:
        results = get2(array, sum - n)
        if results != None:
            return (n, results[0], results[1])
    return None

if __name__ == "__main__":
    filename = "input1.txt"
    arr = arrayise(filename)
    arr = [int(x) for x in arr]
    ans1 = get2(arr, 2020)
    print(ans1[0] * ans1[1])
    ans2 = get3(arr, 2020)
    print(ans2[0] * ans2[1] * ans2[2])
