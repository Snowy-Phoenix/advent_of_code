
def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def pairs(hand, usej=False):
    if (usej and "J" in hand):
        # hack!
        return 1
    a = set()
    pairs = set()
    for h in hand:
        if h in a:
            pairs.add(h)
        else:
            a.add(h)
    return len(pairs)

def is_three(hand, usej=False):
    a = dict()
    js = 0
    for h in hand:
        if (usej and h == 'J'):
            js += 1
        elif h in a:
            a[h] += 1
        else:
            a[h] = 1
    for b in a:
        if a[b] + js >= 3:
            return True
    return False

def is_four(hand, usej=False):
    a = dict()
    js = 0
    for h in hand:
        if (usej and h == 'J'):
            js += 1
        elif h in a:
            a[h] += 1
        else:
            a[h] = 1
    for b in a:
        if a[b] + js >= 4:
            return True
    return False

def is_five(hand, usej=False):
    a = dict()
    js = 0
    for h in hand:
        if (usej and h == 'J'):
            js += 1
            
        elif h in a:
            a[h] += 1
        else:
            a[h] = 1
    for b in a:
        if a[b] + js >= 5:
            return True
    return js >= 5

def is_full(hand, usejs=False):
    return pairs(hand) >= 2 and is_three(hand, usejs)

def high_card(hand):
    a = set()
    for h in hand:
        if h in a:
            return False
        a.add(h)
    return True

class Hand:
    def __init__(self, hand):
        self.hand = hand
    def __lt__(self, other):
        for i in range(len(self.hand)):
            c = self.hand[i]
            o = other.hand[i]
            if c == o:
                continue
            if (c == 'A' or o == 'A'):
                return o == 'A'
            if (c == 'K' or o == 'K'):
                return o == 'K'
            if (c == 'Q' or o == 'Q'):
                return o == 'Q'
            if (c == 'J' or o == 'J'):
                return c == 'J'
            if (c == 'T' or o == 'T'):
                return o == 'T'
            return c < o
    def __repr__(self):
        return self.hand


def sort(x):
    return x[0]

def solve1(array):
    fiveoakind = []
    fouroakind = []
    fullhouse = []
    threeoakind = []
    twopair = []
    onepair = []
    highcard = []
    for line in array:
        hand, bid = line.split()
        bid = int(bid)
        ((hand, bid))
        if is_five(hand):
            fiveoakind.append((Hand(hand), bid))
        elif is_four(hand):
            fouroakind.append((Hand(hand), bid))
        elif is_full(hand):
            fullhouse.append((Hand(hand), bid))
        elif is_three(hand):
            threeoakind.append((Hand(hand), bid))
        elif pairs(hand) >= 2:
            twopair.append((Hand(hand), bid))
        elif pairs(hand) == 1:
            onepair.append((Hand(hand), bid))
        else:
            highcard.append((Hand(hand), bid))
    fiveoakind.sort()
    fouroakind.sort()
    fullhouse.sort()
    threeoakind.sort()
    twopair.sort()
    onepair.sort()
    highcard.sort()
    i = 1
    sum = 0
    for h in highcard:
        sum += i * h[1]
        i += 1
    for h in onepair:
        sum += i * h[1]
        i += 1
    for h in twopair:
        sum += i * h[1]
        i += 1
    for h in threeoakind:
        sum += i * h[1]
        i += 1
    for h in fullhouse:
        sum += i * h[1]
        i += 1
    for h in fouroakind:
        sum += i * h[1]
        i += 1
    for h in fiveoakind:
        sum += i * h[1]
        i += 1
    print(sum)
        
def solve2(array):
    fiveoakind = []
    fouroakind = []
    fullhouse = []
    threeoakind = []
    twopair = []
    onepair = []
    highcard = []
    for line in array:
        hand, bid = line.split()
        bid = int(bid)
        
        if is_five(hand, True):
            fiveoakind.append((Hand(hand), bid))
        elif is_four(hand, True):
            fouroakind.append((Hand(hand), bid))
        elif is_full(hand, True):
            fullhouse.append((Hand(hand), bid))
        elif is_three(hand, True):
            threeoakind.append((Hand(hand), bid))
        elif pairs(hand, True) >= 2:
            twopair.append((Hand(hand), bid))
        elif pairs(hand, True) == 1:
            onepair.append((Hand(hand), bid))
        else:
            highcard.append((Hand(hand), bid))
    fiveoakind.sort()
    fouroakind.sort()
    fullhouse.sort()
    threeoakind.sort()
    twopair.sort()
    onepair.sort()
    highcard.sort()
    print(highcard)
    i = 1
    sum = 0
    for h in highcard:
        sum += i * h[1]
        i += 1
    for h in onepair:
        sum += i * h[1]
        i += 1
    for h in twopair:
        sum += i * h[1]
        i += 1
    for h in threeoakind:
        sum += i * h[1]
        i += 1
    for h in fullhouse:
        sum += i * h[1]
        i += 1
    for h in fouroakind:
        sum += i * h[1]
        i += 1
    for h in fiveoakind:
        sum += i * h[1]
        i += 1
    print(sum)

if __name__ == '__main__':
    filename = "input7.txt"
    arr = arrayise(filename)
    solve1(arr)
    solve2(arr)