import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day8a(array):
    digit_map = {"abcefg":0, "cf":1, "acdeg":2, "acdfg":3, "bcdf":4, "abdfg":5, "abdefg":6, "acf":7, "abcdefg":8, "abcdfg":9}
    count = 0
    for line in array:
        digits = line.split(" | ")
        output = digits[1]
        output_digits = output.split(" ")
        for number in output_digits:
            if len(number) == 2:
                count += 1
            elif len(number) == 4:
                count += 1
            elif len(number) == 3:
                count += 1
            elif len(number) == 7:
                count += 1
    print(count)

def day8b(array):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    digit_map = {"abcefg":0, "cf":1, "acdeg":2, "acdfg":3, "bcdf":4, "abdfg":5, "abdefg":6, "acf":7, "abcdefg":8, "abcdfg":9}
    output_sum = 0
    for line in array:
        encodings, output = line.split(" | ")
        encodings = encodings.split(' ')
        output = output.split(' ')

        one = None
        four = None
        seven = None
        eight = None
        unknown_sets = []
        frequencies = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0}
        for e in encodings:
            for char in e:
                frequencies[char] += 1
            if len(e) == 2:
                one = set(e)
            elif len(e) == 4:
                four = set(e)
            elif len(e) == 3:
                seven = set(e)
            elif len(e) == 8:
                eight = set(e)
            else:
                unknown_sets.append(set(e))
        alphabet_set = set(alphabet)

        # Get e from frequencies.
        e = None
        for i in frequencies:
            if frequencies[i] == 4:
                e = i
        
        # Get f from frequencies.
        f = None
        for i in frequencies:
            if frequencies[i] == 9:
                f = i
        
        # Get b from frequencies.
        b = None
        for i in frequencies:
            if frequencies[i] == 6:
                b = i

        # Get a.
        a = seven.difference(one).pop()

        # Get c from frequencies
        c = None
        for i in frequencies:
            if frequencies[i] == 8 and i != a:
                c = i

        # Get g
        g = None
        for i in unknown_sets:
            if (len(i) == 6):
                temp = i.difference(four)
                temp = temp.difference(set(a))
                if len(temp) == 1:
                    g = temp.pop()
                    break
        
        # Get d
        d = None
        for i in frequencies:
            if frequencies[i] == 7 and i not in g:
                d = i
        
        remapper = {a:'a',b:'b',c:'c',d:'d',e:'e',f:'f',g:'g'}

        output_num = 0
        for digit in output:
            output_num *= 10
            string = []
            for di in digit:
                string.append(remapper[di])
            string = sorted(string)
            actual_digit = ""
            for char in string:
                actual_digit += char
            output_num += digit_map[actual_digit]
        output_sum += output_num
    print(output_sum)

if __name__ == "__main__":
    filename = "input8.txt"
    arr = arrayise(filename)
    day8a(arr)
    day8b(arr)

