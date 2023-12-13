from collections import deque
from collections import defaultdict
import math

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def cmp(ls1, ls2):
    i = 0
    while i < len(ls1) and i < len(ls2):
        if type(ls1[i]) == int and type(ls2[i]) == int:
                if ls1[i] < ls2[i]:
                    return True
                elif ls1[i] > ls2[i]:
                    return False
        elif type(ls1[i]) == list and type(ls2[i]) == list:
            result = cmp(ls1[i], ls2[i])
            if result != None:
                return result
            
        elif type(ls1[i]) == int and type(ls2[i]) == list:
            result = cmp([ls1[i]], ls2[i])
            if result != None:
                return result
        else:
            result = cmp(ls1[i], [ls2[i]])
            if result != None:
                return result
        i += 1
    if (i == len(ls1) and i == len(ls2)):
        return None
    elif (i == len(ls1)):
        return True
    return False

class sort:
    def __init__(self, arr):
        self.arr = arr
    def __lt__(self, other):
        return cmp(self.arr, other.arr)
    def __eq__(self, other):
        return self.arr == other.arr
    def __repr__(self):
        return str(self.arr)

def solve_rushed(array):
    pair_n = 1
    i = 0
    summation = 0
    packets = []
    while i < len(array):
        ls1 = eval(array[i])
        ls2 = eval(array[i + 1])
        if cmp(ls1, ls2):
            summation += pair_n
        pair_n += 1
        i += 3
        packets.append(sort(ls1))
        packets.append(sort(ls2))
    print(summation)
    print(packets)
    packets.append(sort([[2]]))
    packets.append(sort([[6]]))
    packets = sorted(packets)
    print((packets.index(sort([[2]])) + 1) * (packets.index(sort([[6]])) + 1))


class Packet:
    def __init__(self):
        self.packets = []
    
    def append(self, packet):
        if not issubclass(type(packet), Packet):
            return
        self.packets.append(packet)
    
    def __lt__(self, other):
        if type(other) != type(self):
            p = Packet()
            p.append(other)
            other = p
        i = 0
        while i < len(self) and i < len(other):
            if self.packets[i] == other.packets[i]:
                i += 1
            elif self.packets[i] < other.packets[i]:
                return True
            else:
                return False
        if (i == len(self)):
            return True
        return False
    
    def __eq__(self, other):
        if issubclass(type(other), Packet):
            if (type(other) != type(self)):
                p = Packet()
                p.append(other)
                return self.packets == p.packets
            return self.packets == other.packets
        return False
    def __len__(self):
        return len(self.packets)
    def __repr__(self):
        return str(self.packets)

class IntegralPacket(Packet):
    def __init__(self, n):
        self.packets = [n]
    
    def __lt__(self, other):
        if type(other) == type(self):
            return self.packets[0] < other.packets[0]
        p = Packet()
        p.append(self)
        return p < other
    
    def __eq__(self, other):
        if issubclass(type(other), Packet):
            if (type(other) != type(self)):
                p = Packet()
                p.append(self)
                return p.packets == other.packets
            return self.packets == other.packets
        return False

def parse_decimal(line):
    n = 0
    for c in line:
        if c.isdecimal():
            n *= 10
            n += int(c)
        else:
            packet = IntegralPacket(n)
            return packet

def parse_packet(line):
    packet = Packet()
    depth = 0
    i = 1
    while i < len(line):
        c = line[i]
        if c == '[':
            if depth == 0:
                packet.append(parse_packet(line[i:]))
            depth += 1
        elif c == ']':
            if depth == 0:
                return packet
            depth -= 1
        elif c.isdecimal():
            if depth == 0:
                int_packet = parse_decimal(line[i:])
                packet.append(int_packet)
                i += len(str(int_packet.packets[0])) - 1
        i += 1
    return packet

def solve(arr):
    packets = []
    i = 0
    pair_n = 1
    pair_sums = 0
    while i < len(arr):
        packet1 = parse_packet(arr[i])
        packet2 = parse_packet(arr[i + 1])
        if packet1 < packet2:
            pair_sums += pair_n
        i += 3
        pair_n += 1
        packets.append(packet1)
        packets.append(packet2)
    print("Part 1", pair_sums)
    

    p1 = Packet()
    p1.append(IntegralPacket(2))
    p11 = Packet()
    p11.append(p1)

    p2 = Packet()
    p2.append(IntegralPacket(6))
    p22 = Packet()
    p22.append(p2)

    packets.append(p11)
    packets.append(p22)
    packets.sort()
    print("Part 2:", (packets.index(p11) + 1) * (packets.index(p22) + 1))
    
if __name__ == '__main__':
    filename = "input13.txt"
    arr = arrayise(filename)
    solve(arr)
    # solve_rushed(arr)
