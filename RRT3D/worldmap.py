import numpy as np
import datetime
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class WorldMap:
    def __init__(self, map_width, map_height, map_depth):
        self.map_width = map_width
        self.map_height = map_height
        self.map_depth = map_depth

        # Create 3D coordinates
        self.z_coords, self.y_coords, self.x_coords = np.meshgrid(np.arange(0, map_depth), np.arange(0, map_height), np.arange(0, map_width), indexing='ij')

        # Initialize map with zeros
        self.map = np.zeros((map_depth, map_height, map_width))

        # Define obstacle coordinates in 3D space
        self.obstacle_rect1 = (80, 90, 30, 60, 0, 10)  # right (x, y, z) = (70:90, 40:80, 0:10)
        
        # Set obstacle values in the map
        self.map[self.obstacle_rect1[4]:self.obstacle_rect1[5], self.obstacle_rect1[2]:self.obstacle_rect1[3], self.obstacle_rect1[0]:self.obstacle_rect1[1]] = 1
    
    def visualize_map(self):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        # filename_ts = os.path.join("C:\MJ\github\RRT_path", f"map_{self.timestamp}.png")
        filename_ts = os.path.join("/home/nishidalab07/github/RRT_3D_path", f"map_{self.timestamp}.png")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(self.map, edgecolor='k')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D World Map with Obstacles')

        # plt.savefig(filename_ts)

        plt.show()

# Example usage
# map_width = 100
# map_height = 100
# map_depth = 20
# world_map = WorldMap(map_width, map_height, map_depth)
# world_map.visualize_map()