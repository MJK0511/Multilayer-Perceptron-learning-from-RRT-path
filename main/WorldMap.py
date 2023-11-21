import numpy as np
class WorldMap:
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.y_coords, self.x_coords = np.meshgrid(np.arange(0, map_height), np.arange(0, map_width), indexing='ij')
        self.map = np.zeros((map_width, map_height))

        #障害物の座標
        self.obstacle_rect1 = (15, 45, 20, 40) #left, up         (x,y) = (15:45, 20:40)
        self.obstacle_rect2 = (70, 90, 40, 80) #right            (x,y) = (70:90, 40:80)
        self.obstacle_rect3 = (20, 50, 70, 90) #left, down       (x,y) = (20:50, 70:90)

        #障害物生成 map[y, x]
        self.map[self.obstacle_rect1[2]:self.obstacle_rect1[3], self.obstacle_rect1[0]:self.obstacle_rect1[1]] = 1
        self.map[self.obstacle_rect2[2]:self.obstacle_rect2[3], self.obstacle_rect2[0]:self.obstacle_rect2[1]] = 1
        self.map[self.obstacle_rect3[2]:self.obstacle_rect3[3], self.obstacle_rect3[0]:self.obstacle_rect3[1]] = 1