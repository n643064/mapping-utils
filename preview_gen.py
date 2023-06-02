#!/usr/bin/env python3
import os
from io import BytesIO
import cairo
from os import sep
from PIL import Image



def main(world_dir):
    if world_dir[len(world_dir) - 1] != sep:
        world_dir += sep

    biomes = Image.open(world_dir + "biomes.png")
    splat3 = Image.open(world_dir + "splat3.png")
    splat4 = Image.open(world_dir + "splat4.png")

    w = biomes.width
    h = biomes.height
    red = splat3.getchannel(0)
    green = splat3.getchannel(1)
    blue = splat4.getchannel(2)

    data = list(zip(red.point(lambda i: i * 5).getdata(), green.point(lambda i: i * 3).getdata(), blue.point(lambda i: i * 7).getdata()))
    overlay = Image.new("RGBA", (w, h))
    overlay.putdata(data)
    mask = Image.frombytes("RGBA", overlay.size, overlay.tobytes())
    mask = mask.convert("L")
    biomes.paste(overlay, mask=mask)
    tmp = BytesIO()
    biomes.save(tmp, format="PNG")

    background = cairo.ImageSurface.create_from_png(tmp)
    ctx = cairo.Context(background)
    # TODO:
    #   - POIs
    #   - POI color coding
    #   - Spawnpoints



if __name__ == "__main__":
    from sys import argv

    main(argv[1])
