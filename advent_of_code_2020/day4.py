import re

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def verify_byr(val):
    return 1920 <= int(val) <= 2002

def verify_iyr(val):
    return 2010 <= int(val) <= 2020

def verify_eyr(val):
    return 2020 <= int(val) <= 2030

def verify_hgt(val):
    match = re.fullmatch("(\\d+)(cm|in)", val)
    if match == None:
        return False
    value = int(match.group(1))
    unit = match.group(2)
    if (unit == "cm"):
        return 150 <= value <= 193
    elif (unit == "in"):
        return 59 <= value <= 76
    return False

def verify_hcl(val):
    return re.fullmatch("#[0-9a-f]{6}", val) != None

def verify_ecl(val):
    colours = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])
    return val in colours

def verify_pid(val):
    return re.fullmatch("[0-9]{9}", val) != None

def verify_passport(passport, error_check):
    if error_check:
        passed_checks = 0
    else:
        passed_checks = 7
    keywords = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    for keyword in keywords:
        if keyword not in passport:
            return False
        elif error_check:
            if keyword == "byr":
                passed_checks += verify_byr(passport[keyword])
            elif keyword == "iyr":
                passed_checks += verify_iyr(passport[keyword])
            elif keyword == "eyr":
                passed_checks += verify_eyr(passport[keyword])
            elif keyword == "hgt":
                passed_checks += verify_hgt(passport[keyword])
            elif keyword == "hcl":
                passed_checks += verify_hcl(passport[keyword])
            elif keyword == "ecl":
                passed_checks += verify_ecl(passport[keyword])
            elif keyword == "pid":
                passed_checks += verify_pid(passport[keyword])
    if passed_checks != 7:
        return False
    return True

def day4(arr, part2=False):
    valid_passports = 0
    lines = 0
    passport = dict()
    for line in arr:
        if line == '':
            lines += 1
            if (verify_passport(passport, part2)):
                valid_passports += 1
            passport.clear()
        else:
            entries = line.split(' ')
            for field in entries:
                key, value = field.split(':')
                passport[key] = value
    return valid_passports + verify_passport(passport, part2)

if __name__ == "__main__":
    filename = "input4.txt"
    arr = arrayise(filename)
    print(day4(arr, part2=False))
    print(day4(arr, part2=True))

    
