#!/usr/bin/env python3
import os
from io import BytesIO

import PIL.Image
import cairo
from os import sep

import numpy
from PIL import Image
import numpy as np

SCALE = 1


def saturate(c):
    return c != 0 and 255


colors = {
    "trader": (1.0, 0.0, 1.0),
    "rural": (0.70, 0.70, 0.00),
    "wilderness": (0.00, 0.00, 0.00),
    "downtown": (0.40, 0.10, 1.00),
    "remnant": (0.00, 0.33, 0.40),
    "oldwest": (0.40, 0.20, 0.00),
    "perishton": (0.30, 0.53, 1.00),
    "industrial": (0.65, 0.73, 0.81),
    "modern": (0.60, 0.67, 1.00),
    "victorian": (0.31, 0.00, 0.61),
    "army": (0.25, 0.30, 0.00),
    "factory": (1.00, 0.40, 0.10),
    "gun": (1.00, 0.40, 0.10),
    "station": (1.00, 0.20, 0.33),
    "survivor": (0.00, 1.00, 0.67),
    "farm": (0.60, 0.90, 0.00),
    "barn": (0.60, 0.90, 0.00),
    "burnt": (1.00, 0.70, 0.40)
}


def main(world_dir, output_path):
    if world_dir[len(world_dir) - 1] != sep:
        world_dir += sep

    biomes = Image.open(world_dir + "biomes.png")
    size = biomes.width

    dtm_f = open(world_dir + "dtm.raw", "rb")
    dtm_s = dtm_f.read()
    dtm = Image.frombytes("L", (size, size), dtm_s, 'raw', "L;16")
    dtm = dtm.convert("RGBA")

    splat3 = Image.open(world_dir + "splat3.png").resize((size, size))
    splat4 = Image.open(world_dir + "splat4.png").resize((size, size))

    center = size / 2
    red = splat3.getchannel(0).point(saturate)
    green = splat3.getchannel(1).point(saturate)
    blue = splat4.getchannel(2).point(saturate)

    data = list(zip(red.getdata(), green.getdata(), blue.getdata()))
    overlay = Image.new("RGBA", (size, size))
    overlay.putdata(data)

    a = np.array(overlay)

    r = (a[:, :, 0] > 0) * 255
    g = (a[:, :, 1] > 0) * 255
    b = (a[:, :, 2] > 0) * 56
    f = (r | g | b)
    mask = Image.fromarray((f).astype(np.uint8))
    biomes = Image.composite(overlay, biomes, mask)
    tmp = BytesIO()
    biomes = Image.blend(biomes, dtm, 0.2)
    biomes.save(tmp, format="PNG")
    tmp.seek(0)
    tmp.flush()
    background = cairo.ImageSurface.create_from_png(tmp)
    ctx = cairo.Context(background)




    prefabs = open(world_dir + "prefabs.xml")

    while True:
        line = prefabs.readline()
        if not line or "<prefabs>" in line:
            break
    while True:
        line = prefabs.readline()
        if not line or "</prefabs>" in line:
            break
        line_length = len(line)
        name_start = line.find("name=") + 6
        name = line[name_start:line.find("\"", name_start, line_length)]
        position_start = line.find("position=") + 10
        position = line[position_start:line.find("\"", position_start, line_length)].split(",")
        # print(name, position)
        x = center + int(position[0]) * SCALE
        z = center - int(position[2]) * SCALE
        # print(x, z)
        elements = name.split("_")
        shape = 0
        ctx.set_source_rgba(0, 0, 0, 255)
        for e in elements:
            if e in colors:
                # print(*colors[e])
                ctx.set_source_rgb(*colors[e])
        ctx.rectangle(x - 15, z - 15, 30, 30)
        ctx.fill()

    spawnpoints = open(world_dir + "spawnpoints.xml")
    while True:
        line = spawnpoints.readline()
        if not line or "<spawnpoints>" in line:
            break
    while True:
        line = spawnpoints.readline()
        if not line or "</spawnpoints>" in line:
            break
        position_start = line.find("position=") + 10
        position = line[position_start:line.find("\"", position_start, len(line))].split(",")
        # print(name, position)
        x = center + int(position[0]) * SCALE
        z = center - int(position[2]) * SCALE

        ctx.set_source_rgba(0, 0, 0, 1)
        ctx.rectangle(x - 10, z - 10, 20, 20)
        ctx.fill()
        ctx.set_source_rgba(1, 1, 1, 1)
        ctx.rectangle(x - 8, z - 8, 16, 16)
        ctx.fill()
    background.flush()
    background.write_to_png(output_path)


if __name__ == "__main__":
    from sys import argv

    if len(argv) < 3:
        print("Usage: ./preview_gen [world dir] [output file]")
        exit(1)
    main(argv[1], argv[2])
