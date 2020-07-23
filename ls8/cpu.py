"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0] * 256
        self.reg = [0] * 8
        self.stack = -1
        self.running = False

    def ram_read(self, address):
        return self.memory[address]

    def ram_write(self, value, address):
        self.memory[address] = value

    def load(self, file_):
        """Load a program into memory."""

        program = []

        with open(f'ls8/examples/{file_}') as f:
            for line in f:
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                    # print(v)
                    program.append(v)
                except ValueError:
                    continue

                address = 0

                for instruction in program:
                    self.ram_write(instruction, address)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MLT":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True

        def HLT(z, x):
            self.running = False

        def LDI(register, value):
            self.reg[register] = value

        def PRN(register, z):
            print(self.reg[register])

        def MLT(op, reg_1, reg_2):
            self.alu(op, reg_1, reg_2)

        def PSH(register, z):
            self.memory.append(self.reg[register])
            self.stack -= 1
            del self.memory[self.stack]

        def POP(register, z):
            LDI(register, self.memory.pop())
            self.stack += 1
            self.memory.insert(self.stack, 0)

        ops = {
            1: ["HLT", 0, None],
            130: ["LDI", 2, None],
            71: ["PRN", 1, None],
            162: ["MLT", 2, "ALU"],
            69: ["PSH", 1, "STK"],
            70: ["POP", 1, "STK"]
        }

        ops_func = {
            "HLT": HLT,
            "LDI": LDI,
            "PRN": PRN,
            "MLT": MLT,
            "PSH": PSH,
            "POP": POP
        }

        address = 0

        while self.running:
            memory_value1 = self.ram_read(address)
            memory_value2 = self.ram_read(address + 1)
            memory_value3 = self.ram_read(address + 2)
            operation = ops[memory_value1]
            operation_func = ops_func[operation[0]]

            if operation[2] == "ALU":
                operation_func(operation[0], memory_value2, memory_value3)
            else:
                operation_func(memory_value2, memory_value3)

            address += operation[1]
            address += 1


cpu = CPU()
cpu.load('stack.ls8')
cpu.run()
