import numpy as np
import datetime
import os
import matplotlib.pyplot as plt

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
        self.obstacle_rect1 = (80, 90, 30, 60, 10, 20) # right (x, y, z) = (80:90, 30:60, 10:20)
        self.obstacle_rect2 = (20, 40, 50, 70, 80, 90) # right (x, y, z) = (20:40, 50:70, 80:90)

        # Set obstacle values in the map
        self.map[self.obstacle_rect1[0]:self.obstacle_rect1[1], self.obstacle_rect1[2]:self.obstacle_rect1[3], self.obstacle_rect1[4]:self.obstacle_rect1[5]] = 1
        self.map[self.obstacle_rect2[0]:self.obstacle_rect2[1], self.obstacle_rect2[2]:self.obstacle_rect2[3], self.obstacle_rect2[4]:self.obstacle_rect2[5]] = 1
    
    def visualize_map(self, path):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        # filename_ts = os.path.join("C:\MJ\github\RRT_path", f"map_{self.timestamp}.png")
        filename_ts = os.path.join("/home/nishidalab07/github/RRT_3D_path", f"map_{self.timestamp}.png")

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.voxels(self.map, edgecolor='k', label='Obstacles')  # 볼륨에 레이블 추가

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('3D World Map with Obstacles')

        # plt.savefig(filename_ts)
        # RRT path 시각화
        path_handle = None  # 변수를 초기화
        path = np.array(path)
        path_handle, = ax.plot(path[:, 0], path[:, 1], path[:, 2], '-ro', label='RRT Path')

        ax.legend(handles=[path_handle], labels=['RRT Path'])
        plt.show()