import os


def point(a: list, consumer) -> list:
    a2 = []
    for e in a:
        a2.append(consumer(e))
    return a2


def collect_pois(poi_dir):
    ls = []
    for file in os.listdir(poi_dir):
        if not file.endswith(".xml"):
            continue
        fd = open(poi_dir + os.sep + file, "r")
        while True:
            line = fd.readline()
            if not line:
                break
            z = line.find("name=\"Zoning\"")
            if z != -1:
                l = len(line)
                v = line.find("value=", z, l) + 7
                zone = line[v:line.find("\"", v, l)]
                if zone not in ls:
                    ls.append(zone)
                    print(zone)

    # fug


if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2:
        print("Usage: ./util.py poi_list")
    collect_pois(argv[1])
