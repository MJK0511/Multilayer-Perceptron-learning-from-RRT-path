import numpy as np
import csv
import os
from WorldMap import WorldMap
from ImageMap import ImageMap
from RRTpathplanning import RRT

# Example usage:
map_width = 100
map_height = 100
start = (1, 1)
goal = (99, 99)

waypoint_count = 8

world_map = WorldMap(map_width, map_height)

rrt = RRT(world_map, start)
path = rrt.plan_path(goal, waypoint_count)

if path:
    print("Path : [y,x]")
    print(path)

    print("Values at Path[y,x]:")
    values_at_path = [rrt.map[node[0], node[1]] for node in path]
    print(values_at_path)

    # マップ・パスを視覚化
    image_map = ImageMap(world_map, path, map_width, map_height)
    image_map.visualize_map('map_image')

    # ディレクトリーとファイル名を指定
    filename_csv = os.path.join("C:\MJ\github\path", f"coordinates_f{image_map.timestamp}.csv")

    with open(filename_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Y', 'X'])
        csvwriter.writerows(path)

else:
    print("Path not found.")