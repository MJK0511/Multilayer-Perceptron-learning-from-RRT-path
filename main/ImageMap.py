import numpy as np
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class ImageMap:
    def __init__(self, world_map, path, map_width, map_height):
        #イメージ座標系でマップを生成
        self.y_coords, self.x_coords = np.meshgrid(np.arange(0, map_height), np.arange(0, map_width), indexing='ij')
        self.image_map = world_map
        self.image_map.map_width = map_width 
        self.image_map.map_height = map_height
        self.image_map.x = self.image_map.x_coords
        self.image_map.y = -self.image_map.y_coords + self.image_map.map_height
        self.image_map_origin = (0, 0) 

        #イメージ座標系でパスを生成
        if path:
            self.image_path_x, self.image_path_y = zip(*[(x, y) for x, y in path])

    def visualize_map(self, filename):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        filename_ts = os.path.join("C:\MJ\github\path", f"map_{self.timestamp}.png")

        fig = plt.figure(figsize=(6, 6))
        canvas = FigureCanvas(fig)

        # Image map 視覚化
        plt.imshow(self.image_map.map, cmap='gray', origin='lower', extent=[self.image_map_origin[0], self.image_map.map_width, self.image_map_origin[1], self.image_map.map_height])

        # RRT path 視覚化
        if hasattr(self, 'image_path_x') and hasattr(self, 'image_path_y'):
            plt.plot(self.image_path_y, self.image_path_x, '-ro', label='RRT Path')

        plt.title('World Map with RRT Path')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.legend()
        plt.show()

        # pngでマップを保存
        canvas.print_figure(filename_ts, format='png')
