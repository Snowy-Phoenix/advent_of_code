class IntcodeInterpreter:
    
    def __init__(self, program):
        self.rom = [x for x in program]
        self.memory = []
        self.relative_base = 0
        self.max_address = len(self.rom) - 1
        self.input_stream = None
        self.input_stream_ptr = 0
        self.output_stream = None
        self.pc = 0
        self.halted = False
        self.errored = False
        self.awaiting_input = False
        self.infinite_memory = False
        self.print_ascii_output = False

    def set_infinite_memory(self, boolean):
        self.infinite_memory = boolean
    
    def parse_opcode(self):
        full_opcode = self.memory[self.pc]
        opcode = (full_opcode % 10) + ((full_opcode // 10) % 10)
        all_param_modes = full_opcode // 100
        param_modes = []
        while all_param_modes > 0:
            param_modes.append(all_param_modes % 10)
            all_param_modes = all_param_modes // 10
        return opcode, param_modes

    def get_params(self, num_params):
        if self.pc + num_params > self.max_address:
            self.errored = True
            return None
        params = []
        for i in range(num_params):
            params.append(self.memory[self.pc + i + 1])
        return params

    def get_values(self, addresses, param_modes=[]):
        if addresses == None:
            self.errored = True
            return None
        values = []
        for i in range(len(addresses)):
            if i < len(param_modes):
                if param_modes[i] == 1:
                    values.append(self.memory[self.pc + 1 + i])
                    continue
                elif param_modes[i] == 2:
                    if self.relative_base + addresses[i] > self.max_address:
                        if self.infinite_memory:
                            self.memory.extend([0 for _ in range(self.relative_base + addresses[i] - self.max_address + 1)])
                            self.max_address = len(self.memory) - 1
                        else:
                            self.errored = True
                            return None
                    values.append(self.memory[self.relative_base + addresses[i]])
                    continue
            addr = addresses[i]
            if addr < 0:
                self.errored = True
                return None
            if addr > self.max_address:
                if self.infinite_memory:
                    self.memory.extend([0 for _ in range(addr - self.max_address + 1)])
                    self.max_address = len(self.memory) - 1
                else:
                    self.errored = True
                    return None
            
            values.append(self.memory[addr])
        return values

    def setval(self, address, value, param_mode=0):
        if param_mode == 0 and address > self.max_address:
            if self.infinite_memory:
                self.memory.extend([0 for _ in range(address - self.max_address)])
                self.max_address = address
            else:
                self.errored = True
                return None
        elif param_mode == 2 and address + self.relative_base > self.max_address:
            if self.infinite_memory:
                self.memory.extend([0 for _ in range(address + self.relative_base - self.max_address)])
                self.max_address = address + self.relative_base

        if param_mode == 2:
            self.memory[address + self.relative_base] = value
        else:
            self.memory[address] = value

    def opadd(self, param_modes):
        params = self.get_params(3)
        if params == None:
            return
        values = self.get_values(params[0:2], param_modes)
        if values == None:
            return
        val1 = values[0]
        val2 = values[1]
        param_mode = 0
        if len(param_modes) == 3:
            param_mode = param_modes[2]
        self.setval(params[2], val1 + val2, param_mode)
        self.pc += 4
        return

    def opmul(self, param_modes):
        params = self.get_params(3)
        if params == None:
            return
        values = self.get_values(params[0:2], param_modes)
        if values == None:
            return
        val1 = values[0]
        val2 = values[1]
        param_mode = 0
        if len(param_modes) == 3:
            param_mode = param_modes[2]
        self.setval(params[2], val1 * val2, param_mode)
        self.pc += 4
        return

    def get_user_input(self):
        try:
            val = input("Enter an integer or character: ")
            if len(val) == 1:
                if val.isdigit():
                    return int(val)
                return ord(val)
            return int(val)
        except ValueError:
            print("Invalid input.")
            self.errored = True
            return 0

    def opinput(self, param_modes):
        params = self.get_params(1)
        if params == None:
            return

        address = params[0]
        val = 0

        if self.input_stream == None:
            val = self.get_user_input()
        else:
            if self.input_stream_ptr < len(self.input_stream):
                val = self.input_stream[self.input_stream_ptr]
                self.input_stream_ptr += 1
            else:
                self.input_stream = None
                self.input_stream_ptr = 0
                val = self.awaiting_input = True
                return
        if self.errored:
            return
        param_mode = 0
        if len(param_modes) > 0:
            param_mode = param_modes[0]
        self.setval(address, int(val), param_mode)
        self.pc += 2

    def opoutput(self, param_modes, force_print=False):
        params = self.get_params(1)
        values = self.get_values(params, param_modes)
        if values == None:
            return
        
        if force_print or self.output_stream == None:
            if self.print_ascii_output:
                if values[0] > 255:
                    print(values[0])
                else:
                    print(chr(values[0]), end="")
            else:
                print(values[0])
        if self.output_stream != None:
            self.output_stream.append(values[0])
        self.pc += 2

    def opjmpifnzero(self, param_modes):
        params = self.get_params(2)
        values = self.get_values(params, param_modes)
        if values == None:
            return
        if values[0] != 0:
            self.pc = values[1]
        else:
            self.pc += 3

    def opjmpifzero(self, param_modes):
        params = self.get_params(2)
        values = self.get_values(params, param_modes)
        if values == None:
            return
        if values[0] == 0:
            self.pc = values[1]
        else:
            self.pc += 3

    def oplt(self, param_modes):
        params = self.get_params(3)
        if params == None:
            return
        values = self.get_values(params[0:2], param_modes)
        if values == None:
            return

        param_mode = 0
        if len(param_modes) == 3:
            param_mode = param_modes[2]

        if values[0] < values[1]:
            self.setval(params[2], 1, param_mode)
        else:
            self.setval(params[2], 0, param_mode)
        self.pc += 4
        

    def opeq(self, param_modes):
        params = self.get_params(3)
        if params == None:
            return
        values = self.get_values(params[0:2], param_modes)
        if values == None:
            return

        param_mode = 0
        if len(param_modes) == 3:
            param_mode = param_modes[2]

        if values[0] == values[1]:
            self.setval(params[2], 1, param_mode)
        else:
            self.setval(params[2], 0, param_mode)
        self.pc += 4

    def opadjustbase(self, param_modes):
        params = self.get_params(1)
        values = self.get_values(params, param_modes)
        if values == None:
            return
        self.relative_base += values[0]
        self.pc += 2

    def initialise(self, program, input_stream, output_stream):
        self.input_stream = input_stream
        self.input_stream_ptr = 0
        self.output_stream = output_stream
        self.halted = False

        if not self.awaiting_input:
            self.pc = 0
            self.errored = False
            self.relative_base = 0
            if program != None:
                self.memory = [x for x in program]
            else:
                self.memory = [x for x in self.rom]
        else:
            self.awaiting_input = False
        self.max_address = len(self.memory) - 1

    def run(self, program=None, input_stream=None, output_stream=None, print_console=False):
        
        self.initialise(program, input_stream, output_stream)
            
        memory = self.memory
        
        while True:
            if self.pc >= len(memory):
                if print_console:
                    print("End of program.")
                break
            opcode, param_modes = self.parse_opcode()
            if opcode == 1:
                self.opadd(param_modes)            
            elif opcode == 2:
                self.opmul(param_modes)
            elif opcode == 3:
                self.opinput(param_modes)
            elif opcode == 4:
                self.opoutput(param_modes, print_console)
            elif opcode == 5:
                self.opjmpifnzero(param_modes)
            elif opcode == 6:
                self.opjmpifzero(param_modes)
            elif opcode == 7:
                self.oplt(param_modes)
            elif opcode == 8:
                self.opeq(param_modes)
            elif opcode == 9:
                self.opadjustbase(param_modes)
            elif opcode == 99:
                if print_console:
                    print("Halted.")
                break
            else:
                if print_console:
                    print("Unknown opcode:", opcode)
                    self.errored = True
                    memory[0] = -1
                break
            
            if self.errored:
                if print_console:
                    print("Errored")
                memory[0] = -1
                break

            if self.awaiting_input:
                return self.output_stream
        self.halted = True
        if output_stream == None:
            return memory[0]
        else:
            return self.output_stream
