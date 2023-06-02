#!/usr/bin/env python3
from PIL import Image


def main(heightmap_path, prefabs_path, output_path):
    heightmap = Image.open(heightmap_path).convert("L")
    center = int(heightmap.size[0]/2)
    prefabs = open(prefabs_path, "r")
    output = open(output_path, "w")

    while True:
        line = prefabs.readline()
        output.write(line)
        if not line or "<prefabs>" in line:
            break

    while True:
        line = prefabs.readline()
        if not line or "</prefabs>" in line:
            break
        position = line[line.find("position=")+10:line.rfind("rotation")-2]
        xz = position.split(",")
        x = int(xz[0])
        z = int(xz[2])
        y = heightmap.getpixel((center + x, center + z)) - 1
        position2 = str(x) + "," + str(y) + "," + str(z)
        output.write(line.replace(position, position2))
    output.write("</prefabs>\n")


if __name__ == "__main__":
    from sys import argv

    if len(argv) < 4:
        print("fix_prefabs.py - change prefab elevation in reference to a heightmap\n\tUsage: ./fix_prefabs.py [heightmap png] [prefabs xml] [output xml]")
        exit(1)
    main(argv[1], argv[2], argv[3])
