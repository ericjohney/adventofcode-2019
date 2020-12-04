from typing import List, Tuple, Optional
import numpy as np
from itertools import permutations
from enum import Enum

file = open("day07/input.txt", mode="r")
input = file.read().strip()
file.close()
opcodes: List[int] = [int(o) for o in input.split(",")]

Opcodes = List[int]

class Opcode(Enum):
	Add = 1
	Multiply = 2
	Input = 3
	Output = 4
	JumpIfTrue = 5
	JumpIfFalse = 6
	LessThan = 7
	Equals = 8
	End = 99

class Parameter:
	raw_value: int
	mode: int
	def __init__(self, raw_value: int, mode: int):
		self.raw_value = raw_value
		self.mode = mode

	def get_value(self, opcodes: Opcodes) -> int:
		if self.mode == ParameterMode.Position.value:
			return opcodes[self.raw_value]
		if self.mode == ParameterMode.Immediate.value:
			return self.raw_value

class ParameterMode(Enum):
	Position = 0
	Immediate = 1


OPCODE_PARAMETERS = {
	Opcode.Add.value: 3,
	Opcode.Multiply.value: 3,
	Opcode.Input.value: 1,
	Opcode.Output.value: 1,
	Opcode.JumpIfTrue.value: 2,
	Opcode.JumpIfFalse.value: 2,
	Opcode.LessThan.value: 3,
	Opcode.Equals.value: 3,
	Opcode.End.value: 0,
}



class Computer:
	pointer: int
	output: List[int]
	inp: List[int]
	pause: bool

	def __init__(self, opcodes: Opcodes):
		self.opcodes = list(opcodes)
		self.pause = False
		self.pointer = 0
		self.inp = []
		self.output = []

	def do_add(self, parameters: List[Parameter]) -> int:
		*values, save_location = parameters
		values = [v.get_value(self.opcodes) for v in values]
		self.opcodes[save_location.raw_value] = sum(values)
		self.advance_pointer(parameters)

	def do_multiply(self, parameters: List[Parameter]) -> int:
		*values, save_location = parameters
		values = [v.get_value(self.opcodes) for v in values]
		self.opcodes[save_location.raw_value] = values[0] * values[1]
		self.advance_pointer(parameters)

	def do_input(self, parameters: List[Parameter]) -> int:
		save_location = parameters[0]
		if len(self.inp) > 0:
			self.opcodes[save_location.raw_value] = self.inp.pop(0)
			self.advance_pointer(parameters)
		else:
			self.running = False


	def do_output(self, parameters: List[Parameter]) -> int:
		value = parameters[0].get_value(self.opcodes)
		self.output.append(value)
		self.advance_pointer(parameters)

	def do_jump_if_true(self, parameters: List[Parameter]) -> int:
		values = [v.get_value(self.opcodes) for v in parameters]
		self.advance_pointer(parameters)
		if values[0] != 0:
			self.pointer = values[1]

	def do_jump_if_false(self, parameters: List[Parameter]) -> int:
		values = [v.get_value(self.opcodes) for v in parameters]
		self.advance_pointer(parameters)
		if values[0] == 0:
			self.pointer = values[1]

	def do_less_than(self, parameters: List[Parameter]) -> int:
		*values, save_location = parameters
		values = [v.get_value(self.opcodes) for v in values]
		if values[0] < values[1]:
			self.opcodes[save_location.raw_value] = 1
		else:
			self.opcodes[save_location.raw_value] = 0
		self.advance_pointer(parameters)

	def do_equals(self, parameters: List[Parameter]) -> int:
		*values, save_location = parameters
		values = [v.get_value(self.opcodes) for v in values]
		if values[0] == values[1]:
			self.opcodes[save_location.raw_value] = 1
		else:
			self.opcodes[save_location.raw_value] = 0
		self.advance_pointer(parameters)

	def do_halt(self, parameters: List[Parameter]) -> int:
		self.running = False
		self.pointer = len(self.opcodes)

	def advance_pointer(self, parameters: List[Parameter]):
		self.pointer += 1 + len(parameters)

	def next_instruction(self) -> Tuple[int, List[Parameter]]:
		raw_opcode = self.opcodes[self.pointer]
		opcode = int(str(raw_opcode)[-2:])
		num_params = OPCODE_PARAMETERS[opcode]
		raw_parameter_modes = str(raw_opcode)[::-1][2:].ljust(num_params, '0')

		parameter_modes: List[int] = np.zeros(num_params, dtype=int)
		for i in range(len(raw_parameter_modes)):
			parameter_modes[i] = int(raw_parameter_modes[i])

		parameters = self.opcodes[self.pointer + 1 : self.pointer + 1 + num_params]

		for i, param in enumerate(parameters):
			parameters[i] = Parameter(param, parameter_modes[i])

		return self.execute_opcode(opcode, parameters)


	def execute_opcode(self, opcode: int, parameters: List[Parameter]):
		if opcode == Opcode.End.value:
			return self.do_halt(parameters)

		if opcode == Opcode.Add.value:
			return self.do_add(parameters)
		if opcode == Opcode.Multiply.value:
			return self.do_multiply(parameters)
		if opcode == Opcode.Input.value:
			return self.do_input(parameters)
		if opcode == Opcode.Output.value:
			return self.do_output(parameters)
		if opcode == Opcode.JumpIfTrue.value:
			return self.do_jump_if_true(parameters)
		if opcode == Opcode.JumpIfFalse.value:
			return self.do_jump_if_false(parameters)
		if opcode == Opcode.LessThan.value:
			return self.do_less_than(parameters)
		if opcode == Opcode.Equals.value:
			return self.do_equals(parameters)

	def is_done(self) -> bool:
		return not self.pointer < len(self.opcodes)

	def compute(self) -> Opcodes:
		self.running = True
		while not self.is_done() and self.running == True:
			self.next_instruction()
		self.running = False

		return self.opcodes


def permute(arr: List[int]) -> List[int]:
	return permutations(arr)



def part1(input: Opcodes) -> int:
	max_signal = 0
	seqs = permute([0,1,2,3,4])
	for seq in seqs:
		last_output = 0
		for i in seq:
			computer = Computer(opcodes)
			computer.compute()
			last_output = computer.output.pop()
		if last_output > max_signal:
			max_signal = last_output

	return max_signal


def part2(input: Opcodes) -> int:
	max_signal = 0
	seqs = permute([5,6,7,8,9])
	# seqs = [[9,8,7,6,5]]
	for seq in seqs:
		seq = list(seq)
		computers = [Computer(opcodes) for i in seq]
		initial_input = 0
		last_computer = None
		while True:
			for computer in computers:
				if len(seq) > 0:
					computer.inp.append(seq.pop(0))
				if initial_input != None:
					computer.inp.append(initial_input)
					initial_input = None
				if last_computer:
					while len(last_computer.output) > 0:
						computer.inp.append(last_computer.output.pop(0))
				computer.compute()
				last_computer = computer

			done_computers = [computer for computer in computers if computer.is_done()]
			if len(done_computers) == len(computers):
				break
		if last_computer.output[::-1][0] > max_signal:
			max_signal = last_computer.output[::-1][0]

	return max_signal


# print(f"Part 1: {part1(opcodes)}")
print(f"Part 2: {part2(opcodes)}")
