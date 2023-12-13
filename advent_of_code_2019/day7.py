import math
import re
import numpy as np
import itertools
from intcode import IntcodeInterpreter

def arrayise(filename):
    array = []
    f = open(filename, "r")
    for line in f:
        array.append(line.strip())
    return array

def day7(array):
    interpreter = IntcodeInterpreter(array)
    phase_settings = [0,1,2,3,4]
    max_thruster_output = 0
    phase_setting_sequence = tuple()
    for permutation in itertools.permutations(phase_settings):
        last_signal = 0
        for setting in permutation:
            amplifier_input = [setting, last_signal]
            amplifier_output = []
            interpreter.run(input_stream=amplifier_input, output_stream=amplifier_output)
            last_signal = amplifier_output[0]
        if last_signal > max_thruster_output:
            max_thruster_output = last_signal
            phase_setting_sequence = permutation
    print("Part 1:", phase_setting_sequence, max_thruster_output)

    assert max_thruster_output == 70597

    phase_settings = [5,6,7,8,9]
    max_thruster_output = 0
    phase_setting_sequence = tuple()

    amplifiers = [IntcodeInterpreter(array) for _ in range(len(phase_settings))]
    num_amplifiers = len(amplifiers)
    for permutation in itertools.permutations(phase_settings):
        thruster_output = 0
        for i in range(num_amplifiers):
            ampi = amplifiers[i]
            settingi = permutation[i]
            amp_input = [settingi, thruster_output]
            amp_output = []
            ampi.run(input_stream=amp_input, output_stream=amp_output)
            thruster_output = amp_output[0]
        
        current_amplifier = 0
        while not amplifiers[num_amplifiers - 1].halted:
            amp_input = [thruster_output]
            amp_output = []
            curr_amp = amplifiers[current_amplifier]
            curr_amp.run(input_stream=amp_input, output_stream=amp_output)
            thruster_output = amp_output[0]
            current_amplifier = (current_amplifier + 1) % num_amplifiers
        
        if thruster_output > max_thruster_output:
            max_thruster_output = thruster_output
            phase_setting_sequence = permutation

    print("Part 2:", phase_setting_sequence, max_thruster_output)
    
    assert max_thruster_output == 30872528

        

if __name__ == "__main__":
    filename = "input7.txt"
    arr = arrayise(filename)
    arr = arr[0].split(',')
    arr = [int(i) for i in arr]
    day7(arr)
    

