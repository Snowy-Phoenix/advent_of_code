import re
import numpy as np
import copy

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def play1(start_p1, start_p2):
    p1 = copy.copy(start_p1)
    p2 = copy.copy(start_p2)
    seen_hands = set() # Tuple of two tuples of hand 1 and 2.

    while len(p1) > 0 and len(p2) > 0:
        hand_tuple = (tuple(p1), tuple(p2))
        if hand_tuple in seen_hands:
            print("infinite loop at play1")
            break
        seen_hands.add(hand_tuple)

        p1_n = p1.pop()
        p2_n = p2.pop()
        if p1_n > p2_n:
            p1.insert(0, p1_n)
            p1.insert(0, p2_n)
        else:
            p2.insert(0, p2_n)
            p2.insert(0, p1_n)
    
    points = 0
    winner = p1
    winning_player = "Player 1"
    if len(p2) > len(p1):
        winner = p2
        winning_player = "Player 2"
    for i in range(len(winner)):
        points += winner[i] * (i + 1)
    
    print("{} wins with {} points.".format(winning_player, points))
    print("Deck:", winner)

def play2(start_p1, start_p2, is_recursed=False):
    p1 = copy.copy(start_p1)
    p2 = copy.copy(start_p2)
    seen_hands = set() # Tuple of two tuples of hand 1 and 2.
    winner_override = False
    p1_winner_override = False
    while len(p1) > 0 and len(p2) > 0:
        hand_tuple = (tuple(p1), tuple(p2))
        if hand_tuple in seen_hands:
            winner_override = True
            p1_winner_override = True
            break
        seen_hands.add(hand_tuple)
        p1_n = p1.pop()
        p2_n = p2.pop()
        if p1_n <= len(p1) and p2_n <= len(p2):
            drawn_cards1 = []
            drawn_cards2 = []
            for i in range(len(p1) - p1_n, len(p1)):
                drawn_cards1.append(p1[i])
            for i in range(len(p2) - p2_n, len(p2)):
                drawn_cards2.append(p2[i])
            p1_won = play2(drawn_cards1, drawn_cards2, is_recursed=True)
            if p1_won:
                p1.insert(0, p1_n)
                p1.insert(0, p2_n)
            else:
                p2.insert(0, p2_n)
                p2.insert(0, p1_n)
        elif p1_n > p2_n:
            p1.insert(0, p1_n)
            p1.insert(0, p2_n)
        else:
            p2.insert(0, p2_n)
            p2.insert(0, p1_n)
    
    if is_recursed:
        p1_winner = True
        if winner_override:
            p1_winner = p1_winner_override
        else:
            p1_winner = len(p1) > 0
        return p1_winner

    points = 0
    winner = p1
    winning_player = "Player 1"
    if winner_override:
        if not p1_winner_override:
            winner = p2
            winning_player = "Player 2"
    elif len(p2) > len(p1):
        winner = p2
        winning_player = "Player 2"
    for i in range(len(winner)):
        points += winner[i] * (i + 1)
    
    print("{} wins with {} points.".format(winning_player, points))
    print("Deck:", winner)
    return len(p1) > 0

def day22(array):
    player_1_hand = []
    player_2_hand = []
    is_player_1 = True
    is_header = True
    for line in array:
        if is_header:
            is_header = False
            continue
        elif line == "":
            is_header = True
            is_player_1 = False
        elif is_player_1:
            player_1_hand.insert(0, int(line))
        else:
            player_2_hand.insert(0, int(line))
    
    play1(player_1_hand, player_2_hand)
    play2(player_1_hand, player_2_hand)

if __name__ == "__main__":
    filename = "input22.txt"
    arr = arrayise(filename)
    day22(arr)
