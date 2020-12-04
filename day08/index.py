from typing import List, Tuple, Optional
from enum import Enum

file = open("day08/input.txt", mode="r")
input = file.readlines()
file.close()
pixels = "".join(input).strip()


def part1(pixels: str) -> int:
  width = 25
  height = 6
  layers = []
  layer_frequency_counts = []
  for i in range(0, len(pixels), width * height):
    layer = pixels[i:i+(width*height)]
    layers.append(layer)

    freq_count = {}
    for s in layer:
      count = freq_count.get(s, 0)
      freq_count[s] = count + 1
    layer_frequency_counts.append(freq_count)

  min_zero_layer = layer_frequency_counts[0]
  for i, counts in enumerate(layer_frequency_counts):
    if counts.get('0', 0) <= min_zero_layer.get('0', 0):
      min_zero_layer = counts

  return int(min_zero_layer['1']) * int(min_zero_layer['2'])



def part2(pixels: str) -> int:
  width = 25
  height = 6
  layers = []
  for i in range(0, len(pixels), width * height):
    layer = pixels[i:i+(width*height)]
    layers.append(layer)


  image = []
  for y in range(0, height):
    output = ""
    for x in range(0, width):
      for layer in layers:
        pixel = layer[x + (width * y)]
        if pixel == '2':
          continue
        output += pixel
        break
    image.append(output)
  print("\n".join(image).replace("1", "#").replace("0", " "))
  return


print(f"Part 1: {part1(pixels)}")
print(f"Part 2: {part2(pixels)}")
