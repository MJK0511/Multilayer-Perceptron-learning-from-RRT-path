import numpy as np
import csv
import os
import random
from worldmap import WorldMap
from RRT import RRT

# Example usage:
map_width = 100
map_height = 100
map_depth = 100
start = (random.randint(1, 20), random.randint(1, 20), random.randint(1, 20))
goal = (random.randint(80, 99), random.randint(80, 99), random.randint(80, 99))

world_map = WorldMap(map_width, map_height, map_depth)

rrt = RRT(world_map, start)
path = rrt.plan_path(goal)

if path:
    print("Path : [x, y, z]")
    print(path)

    print("Values at Path[x,y,z]:")
    values_at_path = [rrt.map[node[0], node[1], node[2]] for node in path]
    print(values_at_path)

    # マップ・パスを視覚化
    world_map.visualize_map(path)

    # ディレクトリーとファイル名を指定
    # filename_csv = os.path.join("C:\MJ\github\RRT_path", f"coordinates_f{image_map.timestamp}.csv")
    filename_csv = os.path.join("/home/nishidalab07/github/RRT_3D_path", f"coordinates_f{world_map.timestamp}.csv")

    with open(filename_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['X', 'Y', 'Z'])
        csvwriter.writerows(path)

else:
    print("Path not found.")