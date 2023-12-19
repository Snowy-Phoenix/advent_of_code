from collections import deque

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

class Rule:
    def __init__(self, rules):
        self.else_function = rules[-1]
        self.comparisons = [] # (param, operator, value, output if true)
        for r in rules[:-1]:
            comparison, output = r.split(':')
            if comparison[1] == '>':
                param, num = comparison.split('>')
                self.comparisons.append((param, '>', int(num), output))
            else:
                param, num = comparison.split('<')
                self.comparisons.append((param, '<', int(num), output))
    def apply(self, part):
        for cmp in self.comparisons:
            param = part.x
            if cmp[0] == 'm':
                param = part.m
            elif cmp[0] == 'a':
                param = part.a
            elif cmp[0] == 's':
                param = part.s
            
            if cmp[1] == '<':
                if (param < cmp[2]):
                    return cmp[3]
            elif cmp[1] == '>':
                if (param > cmp[2]):
                    return cmp[3]
        return self.else_function
                

class Part:
    def __init__(self, part):
        tokens = part[1:-1].split(',')

        self.x = int(tokens[0].split('=')[1])
        self.m = int(tokens[1].split('=')[1])
        self.a = int(tokens[2].split('=')[1])
        self.s = int(tokens[3].split('=')[1])

class Range:
    def __init__(self, xmin, xmax, mmin, mmax, amin, amax, smin, smax):

        self.xmin = xmin
        self.xmax = xmax
        self.mmin = mmin
        self.mmax = mmax
        self.amin = amin
        self.amax = amax
        self.smin = smin
        self.smax = smax
    
    def separate(self, cmp):
        # Comparison: (param, operator, value, output if true)
        mint = self.xmin
        maxt = self.xmax
        if cmp[0] == 'm':
            mint = self.mmin
            maxt = self.mmax
        elif cmp[0] == 'a':
            mint = self.amin
            maxt = self.amax
        elif cmp[0] == 's':
            mint = self.smin
            maxt = self.smax
        minf = mint
        maxf = maxt

        t_notexists = False
        f_notexists = False
        if cmp[1] == '<':
            mint = min(mint, cmp[2])
            maxt = min(maxt, cmp[2] - 1)
            if (mint == cmp[2]):
                t_notexists = True
            
            minf = max(minf, cmp[2])
            maxf = max(maxf, cmp[2] - 1)
            if (maxf == cmp[2] - 1):
                f_notexists = True
        elif cmp[1] == '>':
            mint = max(mint, cmp[2] + 1)
            maxt = max(maxt, cmp[2])
            if (maxt == cmp[2]):
                t_notexists = True

            minf = min(minf, cmp[2] + 1)
            maxf = min(maxf, cmp[2])
            if (minf == cmp[2] + 1):
                f_notexists = True
        
        r1 = self.copy()
        r2 = self.copy()
        if (t_notexists):
            r1 = None
        else:
            if cmp[0] == 'm':
                r1.mmin = mint
                r1.mmax = maxt
            elif cmp[0] == 'a':
                r1.amin = mint
                r1.amax = maxt
            elif cmp[0] == 's':
                r1.smin = mint
                r1.smax = maxt
            else:
                r1.xmin = mint
                r1.xmax = maxt
        if (f_notexists):
            r2 = None
        else:
            if cmp[0] == 'm':
                r2.mmin = minf
                r2.mmax = maxf
            elif cmp[0] == 'a':
                r2.amin = minf
                r2.amax = maxf
            elif cmp[0] == 's':
                r2.smin = minf
                r2.smax = maxf
            else:
                r2.xmin = minf
                r2.xmax = maxf
        return [r1, r2]
    def copy(self):
        return Range(self.xmin, self.xmax, self.mmin, self.mmax, self.amin, self.amax, self.smin, self.smax)
    def combos(self):
        return (self.xmax - self.xmin + 1)*(self.mmax - self.mmin + 1)*(self.amax - self.amin + 1) *(self.smax - self.smin + 1)

def solve_part2_helper(r, name, functions):
    if (r == None):
        return 0
    elif (name == 'R'):
        return 0
    elif (name == 'A'):
        return r.combos()
    func = functions[name]
    summation = 0
    curr_range = r
    for rule in func.comparisons:
        true_range, false_range = curr_range.separate(rule)
        summation += solve_part2_helper(true_range, rule[3], functions)
        curr_range = false_range
        if (curr_range == None):
            break
    return summation + solve_part2_helper(curr_range, func.else_function, functions)

def solve_part2(functions):
    r = Range(1, 4000, 1, 4000, 1, 4000, 1, 4000)
    print(solve_part2_helper(r, 'in', functions))


def solve(lines):
    rules = []
    parts = []
    currarr = rules

    
    for i, line in enumerate(lines):
        if line == '':
            currarr = parts
        else:
            currarr.append(line)
    
    functions = dict()
    parts_obj = []
    for r in rules:
        name, func = r.split('{')
        func = func[:-1]
        cmps = func.split(',')
        
        functions[name] = Rule(cmps)
    for p in parts:
        parts_obj.append(Part(p))
    
    summation = 0
    for p in parts_obj:
        rule = 'in'
        while True:
            if rule == 'R':
                break
            if rule == 'A':
                summation += p.x + p.m + p.a + p.s
                break
            rule = functions[rule].apply(p)
    print(summation)

    solve_part2(functions)

if __name__ == '__main__':
    filename = "input19.txt"
    arr = arrayise(filename)
    solve(arr)