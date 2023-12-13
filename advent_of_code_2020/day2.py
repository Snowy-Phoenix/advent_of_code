def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def verify_password1(password, character, minimum, maximum):
    count = password.count(character)
    return minimum <= count and count <= maximum

def verify_password2(password, character, minimum, maximum):
    pass_len = len(password)
    if pass_len < minimum:
        return False
    elif pass_len < maximum:
        return password[minimum - 1] == character
    else:
        count = (password[minimum - 1] == character) + (password[maximum - 1] == character)
        return count == 1


def day2(array, part2=False):
    valid_passwords = 0
    for line in array:
        raw = line.split(": ")
        params = raw[0].split(' ')
        minimum, maximum = params[0].split('-')
        minimum = int(minimum)
        maximum = int(maximum)
        password = raw[1]
        character = params[1]
        if part2:
            if (verify_password2(password, character, minimum, maximum)):
                valid_passwords += 1
        else:
            if (verify_password1(password, character, minimum, maximum)):
                valid_passwords += 1

    return valid_passwords

if __name__ == "__main__":
    filename = "input2.txt"
    arr = arrayise(filename)
    print(day2(arr, False))
    print(day2(arr, True))
    
