import re

class FieldValidator:
    def __init__(self, ranges):
        self.ranges = ranges

    def verify(self, value):
        for r in self.ranges:
            if r[0] <= value <= r[1]:
                return True
        return False

class Field:
    def __init__(self, name, ranges):
        self.name = name
        self.field_validator = self.parse_range(ranges)

    def parse_range(self, ranges):
        valid_ranges = ranges.split(" or ")
        range1 = [int(x) for x in valid_ranges[0].split('-')]
        range2 = [int(x) for x in valid_ranges[1].split('-')]
        return FieldValidator([range1, range2])
    
    def verify(self, value):
        return self.field_validator.verify(value)

    def __repr__(self):
        return self.name

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day16(array):
    # Get all the fields
    fields = []
    i = 0
    while i < len(array):
        line = array[i]
        i += 1
        if line == "":
            break
        else:
            field_name, ranges = line.split(": ")
            fields.append(Field(field_name, ranges))
    
    # Skip the your ticket header
    i += 1
    my_ticket = [int(x) for x in array[i].split(',')]

    # Skip the nearby ticket header
    i += 3
    # Verify tickets
    error_rate = 0
    valid_tickets = []
    while i < len(array):
        is_invalid = False
        ticket = [int(x) for x in array[i].split(",")]
        for value in ticket:
            validity = 0
            for field in fields:
                validity += field.verify(value)
            if validity == 0:
                error_rate += value
                is_invalid = True
        if not is_invalid:
            valid_tickets.append(ticket)
        i += 1
    print("Part 1:", error_rate)
    
    field_order = [None for i in range(len(fields))]
    used_fields = set()
    changed = True
    while changed:
        changed = False
        for i in range(len(field_order)):
            if field_order[i] != None:
                continue
            valid_fields = []
            for field in fields:
                if field in used_fields:
                    continue
                is_correct_field = True
                for ticket in valid_tickets:
                    if field.verify(ticket[i]) == False:
                        is_correct_field = False
                        break
                if is_correct_field:
                    valid_fields.append(field)
            if len(valid_fields) == 1:
                field_order[i] = valid_fields[0]
                used_fields.add(valid_fields[0])
                changed = True

    result = 1
    for i in range(len(field_order)):
        field = field_order[i]
        if field.name.startswith("departure"):
            result *= my_ticket[i]
    print("Part 2:", result)

if __name__ == "__main__":
    filename = "input16.txt"
    arr = arrayise(filename)
    day16(arr)
