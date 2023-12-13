import copy
import re
import itertools


class Node:
    def __init__(self):
        self.rules = set()


class ContextFreeGrammar:

    class __Node:
        def __init__(self):
            self.matched_variables = set()

        def add_matches(self, variables):
            self.matched_variables = self.matched_variables.union(variables)

        def __repr__(self):
            return str(self.matched_variables)

    def __init__(self, rules, start='0'):
        self.rules = rules  # dict of Variable, productions
        self.remove_ge_two_producers()
        self.remove_unit_productions()
        self.rule_from_production = self.generate_rules_from_production_dict()

        self.rule_parent = self.generate_parents_of_productions()
        self.start = start
    
    def get_unusued_variables(self, count=1):
        unused_variables = []
        candidate_var = len(self.rules) + 1
        i = 0
        while i < count:
            if str(candidate_var) not in self.rules:
                unused_variables.append(candidate_var)
                candidate_var += 1
                i += 1
            else:
                candidate_var += 1

        unused_variables = [str(x) for x in unused_variables]
        return unused_variables


    def remove_ge_two_producers(self):

        # Verify that there are no rules with greater than 3 non-terminals.
        non_abiding_productions = set()
        for i in self.rules:
            for r in self.rules[i]:
                if len(r) > 2:
                    non_abiding_productions.add(i)
        if len(non_abiding_productions) == 0:
            return
        
        for rule in non_abiding_productions:
            # rule: 8
            productions = self.rules[rule]
            # Productions: [('1', '2', '3'), ('4', '5')]
            for i in range(len(productions)):
                p = productions[i]
                # p: ('1', '2', '3') or ('4', '5')
                if len(p) > 2:
                    new_variables = self.get_unusued_variables(len(p) - 2)

                    self.rules[rule][i] = (p[0], str(new_variables[0]))
                    for j in range(1, len(p) - 2):
                        self.rules[new_variables[j - 1]] = [(p[j - 1], new_variables[j])]
                    self.rules[new_variables[-1]] = [(p[-2], p[-1])]
        return
        

    def generate_parents_of_productions(self):
        dictionary = dict()
        for key in self.rules:
            productions = self.rules[key]
            for p in productions:
                for v in p:
                    if v in dictionary:
                        dictionary[v].add(key)
                    else:
                        key_set = set()
                        key_set.add(key)
                        dictionary[v] = key_set
        return dictionary

    def generate_rules_from_production_dict(self):
        dictionary = dict()
        for key in self.rules:
            productions = self.rules[key]
            for p in productions:
                if p in dictionary:
                    dictionary[p].add(key)
                else:
                    key_set = set()
                    key_set.add(key)
                    dictionary[p] = key_set
        return dictionary

    def remove_unit_productions(self):

        # Verify that grammar is in CNF: Check unit productions
        changed = True
        while changed:
            changed = False
            for i in self.rules:
                for j in range(len(self.rules[i])):
                    r = self.rules[i][j]
                    if len(r) == 1 and r[0].isdigit():
                        key = self.rules[i].pop(j)[0]
                        self.rules[i] += self.rules[key]
                        changed = True
                        

    def __gen_tri_array(self, length):
        table = []
        for i in range(length):
            table.append([self.__Node() for x in range(i + 1)])
        return table

    def __populate_bottom_row(self, table, string):
        bottom_row = table[len(table) - 1]
        for i in range(len(string)):
            char = tuple(string[i])
            bottom_row[i].add_matches(self.rule_from_production[char])

    def matches(self, string):
        table = self.__gen_tri_array(len(string))
        self.__populate_bottom_row(table, string)
        for row in range(len(table) - 2, -1, -1):
            tab_row = table[row]
            for col in range(len(tab_row)):
                tab_node = tab_row[col]
                num_rows_below_row = len(table) - row - 1
                for i in range(num_rows_below_row):
                    a_row = len(table) - 1 - i
                    a_col = col
                    b_row = row + 1 + i
                    b_col = col + 1 + i
                    node_a = table[a_row][a_col]
                    node_b = table[b_row][b_col]
                    matched_a = node_a.matched_variables
                    matched_b = node_b.matched_variables
                    for var_a in matched_a:
                        for var_b in matched_b:
                            production = (var_a, var_b)
                            if production in self.rule_from_production:
                                tab_node.add_matches(self.rule_from_production[production])
        # print(table)
        # print("=")
        # print(self.rules)
        # print("=")
        # print(self.rule_from_production)
        return self.start in table[0][0].matched_variables

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array


def day18(array):
    rules = dict()  # Variable, list of productions
    i = 0
    while i < len(array):
        line = array[i]
        if line == "":
            i += 1
            break
        variable, productions = line.split(": ")

        productions = productions.split(' | ')
        production_list = []
        for p in productions:
            if re.fullmatch('"."', p):
                production_list.append(tuple(p.strip('"')))
            else:
                production_list.append(tuple(p.split(" ")))
        rules[variable] = production_list
        i += 1

    grammar = ContextFreeGrammar(rules)

    matches = 0
    while i < len(array):
        line = array[i]
        matches += grammar.matches(line)
        i += 1
    # matches += grammar.matches(array[i])
    # matches += grammar.matches("aaaaaaaaaaaa")
    print("Total matches:", matches)


if __name__ == "__main__":
    filename1 = "input19a.txt"
    filename2 = "input19b.txt"

    arr1 = arrayise(filename1)
    arr2 = arrayise(filename2)
    day18(arr1)
    day18(arr2)
