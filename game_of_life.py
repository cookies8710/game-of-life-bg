import png
import os
import time
import random
from functools import reduce
import operator

GOL_W, GOL_H = 384, 216
PNG_W, PNG_H = 1920, 1080

def game_of_life(arr):
    w, h = len(arr[0]), len(arr)
    def neigh(arr, x, y):
        def get_cell(arr, x, y):
            x %= w
            y %= h
            return arr[y][x]
        alive = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if (dx or dy) and get_cell(arr, x + dx, y + dy):
                    alive += 1 
        return alive

    # nextgen - start with empty
    ret = [[False for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            # now for each cell count neighbours and decide cell presence in next gen
            ne = neigh(arr, x, y)
            if arr[y][x]:
                next = ne in (2, 3)
            else:
                next = ne == 3
            ret[y][x] = next
    return ret

def map_boolean_to_values(arr, a, b):
    return [[a if x else b for x in y] for y in arr]

def stretch(array, w, h):
  # stretches 2D 'array' to 'w' x 'h' by copying as much as it can and padding the rest with zeros
  aw, ah = len(array[0]), len(array)
  mw, mh = w // aw, h // ah

  def mul(arr, n):
      # multiplies elements of 'arr' by 'n' e.g. mul([1,2,3], 2) yields [1,1,2,2,3,3]
     return reduce(operator.add, [[x] * n for x in arr])

  def pad(src, unit, target):
      # pads 'src' to match target 'width' using 'unit'
      current = len(src)
      padding = target - current
      pad1 = padding // 2
      pad2 = padding - pad1
      return unit * pad1 + src + unit * pad2

  return pad(mul([pad(mul(row, mw), [0], w) for row in array], mh), [[0] * w], h)

# initialize Game Of Life by random cells
game_of_life_lattice = [[random.random() > 0.5 for x in range(GOL_W)] for y in range(GOL_H)]

generation = 0
dtime = time.time()

while True:
    image = map_boolean_to_values(game_of_life_lattice, 167, 31)
    game_of_life_lattice = game_of_life(game_of_life_lattice)

    with open('game_of_life_backbuffer.png', 'wb') as file:
        writer = png.Writer(PNG_W, PNG_H, greyscale=True)
        writer.write(file, stretch(image, PNG_W, PNG_H))

    # "front" buffer
    os.rename('game_of_life_backbuffer.png', 'game_of_life_frontbuffer.png')

    gps = 1 / (time.time() - dtime)
    dtime = time.time()
    print(f"Generation #{generation}, generations per second {gps:.1f}")
    generation += 1
