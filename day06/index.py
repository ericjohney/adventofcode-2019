from typing import List, Tuple, Optional
from enum import Enum

file = open("day06/input.txt", mode="r")
input = file.readlines()
file.close()
orbits = [orbit.strip().split(")") for orbit in input]

class Node:
  name: str
  children: List["Node"]
  parent: "Node"
  depth: int
  def __init__(self, name: str):
    self.name = name
    self.children = []
    self.depth = 0
    self.parent = None
  def add_child(self, child: "Node"):
    self.children.append(child)
    child.parent = self
    def deepen(child):
      child.depth += self.depth + 1
      for subchild in child.children:
          deepen(subchild)
    deepen(child)
  def get_address(self):
    address = []
    def add_address(parent):
      address.insert(0, parent.name)
      if parent.parent:
        add_address(parent.parent)
    add_address(self.parent)
    return address



def part1(orbits: List[str]) -> int:
  objects = {}
  for orbit in orbits:
    parent = objects.get(orbit[0], Node(orbit[0]))
    child = objects.get(orbit[1], Node(orbit[1]))
    objects[parent.name] = parent
    objects[child.name] = child
    parent.add_child(child)

  orbit_count = 0
  for name, orbit in objects.items():
    orbit_count += orbit.depth

  print(objects["C21"].depth)
  return orbit_count


def part2(wires: List[str]) -> int:
  objects = {}
  for orbit in orbits:
    parent = objects.get(orbit[0], Node(orbit[0]))
    child = objects.get(orbit[1], Node(orbit[1]))
    objects[parent.name] = parent
    objects[child.name] = child
    parent.add_child(child)

  you = objects["YOU"].get_address()
  san = objects["SAN"].get_address()
  diff = list(set(you) - set(san)) + list(set(san) - set(you))
  print(f"diff {diff}")

  return len(diff)



print(f"Part 1: {part1(orbits)}")
print(f"Part 2: {part2(orbits)}")
