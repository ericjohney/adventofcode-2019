from typing import List
import math

file = open("day01/input.txt", mode="r")
lines = [int(line) for line in file.read().splitlines()]
file.close()


def compute_fuel(mass: int) -> int:
    return max(math.floor(mass / 3) - 2, 0)


def part1(masses: List[int]) -> int:
    fuel_required = [compute_fuel(mass) for mass in masses]
    return sum(fuel_required)


def part2(masses: List[int]) -> int:
    sum = 0
    for mass in masses:
        fuel = compute_fuel(mass)
        while fuel > 0:
            sum += fuel
            fuel = compute_fuel(fuel)
    return sum


print(f"Part 1: {part1(lines)}")
print(f"Part 2: {part2(lines)}")
