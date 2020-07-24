"""CPU functionality."""


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0] * 256
        self.reg = [0] * 8
        self.stack = -1
        self.address = 0
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
                    program.append(v)
                except ValueError:
                    continue

                for instruction in program:
                    self.ram_write(instruction, self.address)
                    self.address += 1

                self.address = 0

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

    def run(self):
        """Run the CPU."""
        self.running = True

        def HLT(x, y):
            self.running = False

        def LDI(register, value):
            self.reg[register] = value

        def PRN(register, y):
            print(self.reg[register])

        def MLT(reg_1, reg_2):
            self.alu("MLT", reg_1, reg_2)

        def ADD(reg_1, reg_2):
            self.alu("ADD", reg_1, reg_2)

        def PSH(register, y):
            self.memory.append(self.reg[register])
            self.stack -= 1
            del self.memory[self.stack]

        def POP(register, y):
            LDI(register, self.memory.pop())
            self.stack += 1
            self.memory.insert(self.stack, 0)

        def CAL(register, y):
            LDI(7, self.address)
            PSH(7, y)
            self.address = self.reg[register]

        def RET(x, y):
            POP(7, y)
            self.address = self.reg[7]

        ops = {
            1: [HLT, 0],
            17: [RET, 1],
            69: [PSH, 1],
            70: [POP, 1],
            71: [PRN, 1],
            80: [CAL, -1],
            130: [LDI, 2],
            160: [ADD, 2],
            162: [MLT, 2]
        }

        while self.running:
            memory_value1 = self.ram_read(self.address)
            memory_value2 = self.ram_read(self.address + 1)
            memory_value3 = self.ram_read(self.address + 2)
            operation = ops[memory_value1]

            operation[0](memory_value2, memory_value3)

            self.address += operation[1] + 1


cpu = CPU()
cpu.load('call.ls8')
cpu.run()
