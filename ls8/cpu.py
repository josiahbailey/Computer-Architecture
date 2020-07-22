"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0] * 256
        self.reg = [0] * 8
        self.running = False

    def ram_read(self, register):
        return self.memory[register]

    def ram_write(self, value, register):
        self.memory[register] = value

    def load(self, file_):
        """Load a program into memory."""

        program = []

        with open(f'ls8/examples/{file_}') as f:
            for line in f:
                line = line.split("#")
                try:
                    v = int(line[0])
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

    def binaryToDecimal(self, binary):
        binary1 = binary
        decimal, i, n = 0, 0, 0
        while(binary != 0):
            dec = binary % 10
            decimal = decimal + dec * pow(2, i)
            binary = binary//10
            i += 1
        return decimal

    def run(self):
        """Run the CPU."""
        self.running = True

        def HLT():
            self.running = False

        def LDI(register, value):
            self.reg[register] = value

        def PRN(register):
            print(self.reg[register])

        def MLT(op, reg_1, reg_2):
            self.alu(op, reg_1, reg_2)

        ops = {
            1: ["HLT", 0, None],
            130: ["LDI", 2, None],
            71: ["PRN", 1, None],
            162: ["MLT", 2, "ALU"]
        }

        ops_func = {
            "HLT": HLT,
            "LDI": LDI,
            "PRN": PRN,
            "MLT": MLT
        }

        address = 0

        while self.running:
            memory_value1 = self.binaryToDecimal(self.ram_read(address))
            memory_value2 = self.binaryToDecimal(self.ram_read(address + 1))
            memory_value3 = self.binaryToDecimal(self.ram_read(address + 2))
            operation = ops[memory_value1]
            operation_func = ops_func[operation[0]]

            if operation[1] == 0:
                operation_func()
            elif operation[1] == 1:
                operation_func(memory_value2)
                address += 1
            elif operation[1] == 2:
                if operation[2] == "ALU":
                    operation_func(operation[0], memory_value2, memory_value3)
                else:
                    operation_func(memory_value2, memory_value3)
                address += 2

            address += 1


cpu = CPU()
cpu.load('mult.ls8')
cpu.run()
