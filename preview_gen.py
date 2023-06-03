#!/usr/bin/env python3
import os
from io import BytesIO
import cairo
from os import sep
from PIL import Image


def saturate(c):
    return c != 0 and 255


def main(world_dir, poi_list_path, output_path):
    if world_dir[len(world_dir) - 1] != sep:
        world_dir += sep

    biomes = Image.open(world_dir + "biomes.png")
    splat3 = Image.open(world_dir + "splat3.png")
    splat4 = Image.open(world_dir + "splat4.png")

    size = biomes.width
    center = size/2
    red = splat3.getchannel(0).point(saturate)
    green = splat3.getchannel(1).point(saturate)
    blue = splat4.getchannel(2).point(saturate)

    data = list(zip(red.getdata(), green.getdata(), blue.getdata()))
    overlay = Image.new("RGBA", (size, size))
    overlay.putdata(data)
    mask = Image.frombytes("RGBA", overlay.size, overlay.tobytes())
    mask = mask.convert("L")
    biomes.paste(overlay, mask=mask)
    tmp = BytesIO()
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
        print(name, position)
        x = center + int(position[0])
        z = center + int(position[2])
        print(x, z)
        ctx.set_source_rgb(0, 0, 0)
        ctx.rectangle(x-10, z-10, 20, 20)
        ctx.fill()

    background.flush()
    background.write_to_png("out.png")


if __name__ == "__main__":
    from sys import argv
    if len(argv) < 4:
        print("Usage: ./preview_gen [world dir] [poi list] [output file]")
        exit(1)
    main(argv[1], argv[2], argv[3])
