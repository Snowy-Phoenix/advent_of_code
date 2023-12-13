class Ranges:
    def __init__(self, conversion):
        self.destination_range_start = int(conversion[0])
        self.source_range_start = int(conversion[1])
        self.range_len = int(conversion[2])
    def __lt__(self, other):
        return self.source_range_start < other.source_range_start
    def __repr__(self):
        return str([self.destination_range_start, self.source_range_start, self.range_len])
    

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def solve(array):
    seeds = list(map(int, array[0].split()[1:]))
    array = array[3:]
    seed2soil = []
    i = 0
    for line in array:
        if line == "":
            break
        seed2soil.append(Ranges(line.split()))
        i += 1
    seed2soil.sort()
    array = array[i + 2:]
    i = 0
    soil2fert = []
    for line in array:
        if line == "":
            break
        soil2fert.append(Ranges(line.split()))
        i += 1
    array = array[i + 2:]
    i = 0
    soil2fert.sort()
    fert2water = []
    for line in array:
        if line == "":
            break
        fert2water.append(Ranges(line.split()))
        i += 1
    fert2water.sort()
    array = array[i + 2:]
    i = 0
    water2light = []
    for line in array:
        if line == "":
            break
        water2light.append(Ranges(line.split()))
        i += 1
    water2light.sort()
    array = array[i + 2:] 
    i = 0
    light2temp = []
    for line in array:
        if line == "":
            break
        light2temp.append(Ranges(line.split()))
        i += 1
    light2temp.sort()
    array = array[i + 2:] 
    i = 0
    temp2hum = []
    for line in array:
        if line == "":
            break
        temp2hum.append(Ranges(line.split()))
        i += 1 
    temp2hum.sort()
    array = array[i + 2:]
    i = 0
    hum2loc = []
    for line in array:
        if line == "":
            break
        hum2loc.append(Ranges(line.split()))
        i += 1 
    minloc = 2**31
    hum2loc.sort()
    # Dest range start, source range start, range
    for seed in seeds:

        soil = get_conversion(seed, seed2soil)
        fert = get_conversion(soil, soil2fert)
        water = get_conversion(fert, fert2water)
        light = get_conversion(water, water2light)
        temp = get_conversion(light, light2temp)
        hum = get_conversion(temp, temp2hum)
        loc = get_conversion(hum, hum2loc)
        minloc = min(loc, minloc)
    print(minloc)

    ranges = []
    for i in range(1, len(seeds), 2):
        ranges.append((seeds[i - 1], seeds[i - 1] + seeds[i] - 1))
    ranges = get_ranges(ranges, seed2soil)
    ranges = get_ranges(ranges, soil2fert)
    ranges = get_ranges(ranges, fert2water)
    ranges = get_ranges(ranges, water2light)
    ranges = get_ranges(ranges, light2temp)
    ranges = get_ranges(ranges, temp2hum)
    ranges = get_ranges(ranges, hum2loc)
    min_r = 2**31
    for r in ranges:
        min_r = min(min_r, r[0])
    print(min_r)
def get_ranges(ranges, a2b):
    ls_ranges = []
    for r in ranges:
        r_ls = [r[0], r[1]]
        finished = False
        for a in a2b:
            if (finished):
                break
            low_overlap = a.source_range_start <= r[0] < a.source_range_start + a.range_len
            high_overlap = a.source_range_start <= r[1] < a.source_range_start + a.range_len
            if (not low_overlap and not high_overlap):
                # Non overlapping, low
                if (r[1] < a.source_range_start):
                    ls_ranges.append(tuple(r_ls))
                    finished = True
                elif (r[0] < a.source_range_start and r[1] >= a.source_range_start + a.range_len):
                    # Overlap:
                    # ----|||||||--------
                    # --||||||||||-------
                    ls_ranges.append((r_ls[0], a.source_range_start - 1))
                    ls_ranges.append((a.destination_range_start, a.destination_range_start + a.range_len - 1))
                    r_ls[0] = a.source_range_start + a.range_len
            elif (not low_overlap and high_overlap):
                # Overlap:
                # ----|||||||--------
                # --|||||------------
                ls_ranges.append((r_ls[0], a.source_range_start - 1))
                ls_ranges.append((a.destination_range_start,
                                  a.destination_range_start + r_ls[1] - a.source_range_start))
                finished = True
            elif (low_overlap and high_overlap):
                # Overlap:
                # ----|||||||--------
                # -----|||||---------
                ls_ranges.append((a.destination_range_start + r_ls[0] - a.source_range_start,
                                  a.destination_range_start + r_ls[1] - a.source_range_start))
                finished = True
            elif (low_overlap and not high_overlap):
                # Overlap:
                # ----|||||||--------
                # ---------|||||-----
                ls_ranges.append((a.destination_range_start + r_ls[0] - a.source_range_start,
                                  a.destination_range_start + a.range_len - 1))
                r_ls[0] = a.source_range_start + a.range_len
        if (finished == False):
            ls_ranges.append(tuple(r_ls))
    return ls_ranges
            



def get_conversion(a, a2b):
    for ranges in a2b:
        if (ranges.source_range_start <= a < ranges.source_range_start + ranges.range_len):
            offset = a - ranges.source_range_start
            return ranges.destination_range_start + offset
    return a


if __name__ == '__main__':
    filename = "input5.txt"
    arr = arrayise(filename)
    solve(arr)