import math
import re
import numpy as np
import copy
import itertools
import heapq

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def read_packet(binary_packet):
    packet_version = binary_packet[0:3]
    binary_packet = binary_packet[3:]
    packet_pointer = 0
    has_read_type = False
    last_read_type = None

    packet_bits = []
    packet_annotation = []
    packet_bits.append("")
    packet_annotation.append("begin")
    packet_bits.append(packet_version)
    packet_annotation.append("version")

    while packet_pointer < len(binary_packet):
        if not has_read_type:
            packet_type = binary_packet[packet_pointer:packet_pointer + 3]
            packet_bits.append(packet_type)
            last_read_type = packet_type
            packet_pointer += 3
            has_read_type = True
        else:
            if last_read_type == "100":
                packet_annotation.append("type literal")
                is_last_value = False
                while not is_last_value:
                    leading_bit = binary_packet[packet_pointer]
                    if leading_bit == '0':
                        is_last_value = True
                    packet_bits.append(binary_packet[packet_pointer: packet_pointer + 5])
                    packet_annotation.append("literal")
                    packet_pointer += 5
                packet_bits.append("")
                packet_annotation.append("end")
                return packet_bits, packet_annotation

            else:
                packet_annotation.append("type operator")
                length_type_id = binary_packet[packet_pointer]
                packet_pointer += 1
                packet_bits.append(length_type_id)
                packet_annotation.append("length id")
                if length_type_id == '0':
                    length = binary_packet[packet_pointer: packet_pointer + 15]
                    packet_pointer += 15
                    packet_bits.append(length)
                    packet_annotation.append("length encoding")
                    length_number = int(length, base=2)
                    read_length = 0
                    while read_length < length_number:
                        sub_packet_bits, sub_packet_annotations = read_packet(binary_packet[packet_pointer:])
                        for i in range(len(sub_packet_bits)):
                            read_length += len(sub_packet_bits[i])
                            packet_bits.append(sub_packet_bits[i])
                            packet_annotation.append(sub_packet_annotations[i])
                        packet_pointer += read_length
                        length_number -= read_length
                        read_length = 0
                    packet_bits.append("")
                    packet_annotation.append("end")
                    return packet_bits, packet_annotation
                else:
                    sub_packets = binary_packet[packet_pointer: packet_pointer + 11]
                    packet_pointer += 11
                    packet_bits.append(sub_packets)
                    packet_annotation.append("sub-packets encoding")
                    sub_packets_number = int(sub_packets, base=2)
                    for _ in range(sub_packets_number):
                        read_length = 0
                        sub_packet_bits, sub_packet_annotations = read_packet(binary_packet[packet_pointer:])
                        for i in range(len(sub_packet_bits)):
                            read_length += len(sub_packet_bits[i])
                            packet_bits.append(sub_packet_bits[i])
                            packet_annotation.append(sub_packet_annotations[i])
                        packet_pointer += read_length
                    packet_bits.append("")
                    packet_annotation.append("end")
                    return packet_bits, packet_annotation
    

def evaluate_packet(packet_bits, annotations):

    nesting = 0
    packet_pointer = 1
    operator = None
    cumulative_value = 0
    first_packet = True
    inequality_value = 0
    while packet_pointer < len(packet_bits):
        if nesting < 0:
            return cumulative_value
        annotation = annotations[packet_pointer]
        if annotation == "type literal" and operator == None:
            operator = packet_bits[packet_pointer]
        elif annotation == "literal" and nesting == 0:
            cumulative_value = cumulative_value << 4
            literal = int(packet_bits[packet_pointer], base=2)
            literal = literal & 15
            cumulative_value += literal
        elif annotation == "type operator" and operator == None:
            operator = packet_bits[packet_pointer]
        elif annotation == "begin":
            if nesting == 0:
                value = evaluate_packet(packet_bits[packet_pointer:], annotations[packet_pointer:])
                if operator == "000":
                    cumulative_value += value
                elif operator == "001":
                    if first_packet:
                        cumulative_value = value
                        first_packet = False
                    else:
                        cumulative_value *= value
                elif operator == "010":
                    if first_packet:
                        cumulative_value = value
                        first_packet = False
                    else:
                        cumulative_value = min(cumulative_value, value)
                elif operator == "011":
                    if first_packet:
                        cumulative_value = value
                        first_packet = False
                    else:
                        cumulative_value = max(cumulative_value, value)
                elif operator == "101":
                    if first_packet:
                        cumulative_value = 1
                        inequality_value = value
                        first_packet = False
                    elif inequality_value <= value:
                        cumulative_value = 0
                elif operator == "110":
                    if first_packet:
                        cumulative_value = 1
                        inequality_value = value
                        first_packet = False
                    elif inequality_value >= value:
                        cumulative_value = 0
                elif operator == "111":
                    if first_packet:
                        cumulative_value = 1
                        inequality_value = value
                        first_packet = False
                    elif inequality_value != value:
                        cumulative_value = 0
            nesting += 1
        elif annotation == "end":
            nesting -= 1
        packet_pointer += 1
    return cumulative_value

def day16(array):

    binary_packet = ""
    for c in array[0]:
        n = bin(int(c, base=16))
        n = n[2:]
        while len(n) < 4:
            n = '0' + n
        binary_packet += n
    
    packet_bits, packet_annotation = read_packet(binary_packet)
    cumsum = 0
    for i in range(len(packet_annotation)):
        if packet_annotation[i] == "version":
            cumsum += int(packet_bits[i], base=2)

    print("Part 1:", cumsum)

    print("Part 2:", evaluate_packet(packet_bits, packet_annotation))
    
if __name__ == "__main__":
    filename = "input16.txt"
    arr = arrayise(filename)
    day16(arr)

