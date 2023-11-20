import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import datetime
import csv

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
    
    def __str__(self):
        return f"Node: ({self.x}, {self.y})"

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

class RRT:
    def __init__(self, world_map, start):
        self.tree = []
        self.map = world_map.map
        self.obstacle_rect1 = world_map.obstacle_rect1
        self.obstacle_rect2 = world_map.obstacle_rect2
        self.obstacle_rect3 = world_map.obstacle_rect3
        self.map_width = world_map.map_width
        self.map_height = world_map.map_height
        self.root = Node(start[1], start[0])
        self.tree.append(self.root)

    #ノードを追加する関数
    def add_node(self, x, y, parent):
        node = Node(x, y)
        node.parent = parent
        self.tree.append(node)
        return node

    #衝突を確認する
    def is_collision_free(self, x, y):
        if x < 0 or x >= self.map_width or y < 0 or y >= self.map_height:
            return False
        if self.map[y, x] == 1.0:
            return False
        return True
    
    def calculate_line_equation(self, parent_node, new_node):
        # 直線方程式計算
        x1, y1 = parent_node.x, parent_node.y
        x2, y2 = new_node.x, new_node.y

        if x2 - x1 != 0:
            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1
            return slope, intercept
        else:
            # 直線が垂直である場合
            return float('inf'), x1
        

    def is_collision_free_rectangle(self, parent_node, new_node, obstacle_rect):
        # 親ノードと子ノードの間の直線方程式を計算
        slope, intercept = self.calculate_line_equation(parent_node, new_node)

        # 障害物の頂点座標
        x1, y1, x2, y2 = obstacle_rect[0], obstacle_rect[2], obstacle_rect[1], obstacle_rect[3]
        x3, y3, x4, y4 = x1, y2, x2, y1

        # すべての頂点が直線の上にあればTrue
        above_line = all([y > slope * x + intercept for x, y in [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]])
    
        return above_line


    #ランダムに座標を生成
    def generate_random_point(self):
        max_attempts = 1000  # Set a limit on the number of attempts to avoid infinite loop
        for _ in range(max_attempts):
            x = np.random.randint(0, self.map_width)
            y = np.random.randint(0, self.map_height)

            # ランダム座標が障害物と衝突するか確認
            if self.is_collision_free(x, y):
                return x, y

    # If no collision-free point is found after the maximum attempts, return None
        return None

    #一番近いノードを探す
    def find_nearest_node(self, x, y):
        #距離計算
        distances = [np.sqrt((node.x - x)**2 + (node.y - y)**2) for node in self.tree]
        #最小値を出す
        min_index = np.argmin(distances)
        return self.tree[min_index]

    #パス生成
    #step_sizeでwaypointの数を調整できる
    def plan_path(self, goal, max_iter=1000, step_size=20):
        for _ in range(max_iter):
            #ランダムな点 (x_rand, y_rand) を生成
            x_rand, y_rand = self.generate_random_point()
            #最も近いノードを見つける
            n = self.find_nearest_node(x_rand, y_rand) # n : nearest_node
            
            #ノードを拡張して新しいノードを生成:step_size 分だけ移動する
            x_new = int(round(n.x + step_size * np.cos(np.arctan2(y_rand - n.y, x_rand - n.x))))
            y_new = int(round(n.y + step_size * np.sin(np.arctan2(y_rand - n.y, x_rand - n.x))))
        
            #生成した新しいノードが障害物と衝突していない場合、ツリーに追加
            if not self.is_collision_free((x_new), (y_new)):
                continue

            new_node = Node(x_new, y_new)

            # 正方形との衝突を確認
            if not self.is_collision_free_rectangle(n, new_node, self.obstacle_rect1):
                continue
            if not self.is_collision_free_rectangle(n, new_node, self.obstacle_rect2):
                continue
            if not self.is_collision_free_rectangle(n, new_node, self.obstacle_rect3):
                continue

            new_node = self.add_node(x_new, y_new, n)

            #新しいノードが目標に十分に近い場合、目標ノードをツリーに追加し、計画されたパスを返す
            if np.sqrt((new_node.x - goal[0])**2 + (new_node.y - goal[1])**2) < step_size:
                goal_node = self.add_node(goal[1], goal[0], new_node)
                return self.extract_path(goal_node)

        return None

    #パスを抽出
    def extract_path(self, goal_node):
        path = []
        current_node = goal_node
        while current_node is not None:
            path.append((current_node.y, current_node.x))
            current_node = current_node.parent
        return path[::-1]


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
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
        filename_ts = f"{filename}_{timestamp}.png"

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

        # Save the map as an image file
        canvas.print_figure(filename_ts, format='png')


# Example usage:
map_width = 100
map_height = 100
start = (1, 1)
goal = (99, 99)

world_map = WorldMap(map_width, map_height)

rrt = RRT(world_map, start)
path = rrt.plan_path(goal)

if path:
    print("Path : [y,x]")
    print(path)

    print("Values at Path[y,x]:")
    values_at_path = [rrt.map[node[0], node[1]] for node in path]
    print(values_at_path)

    # マップ・パスを視覚化
    image_map = ImageMap(world_map, path, map_width, map_height)
    image_map.visualize_map('map_image')

    # Save the coordinates as a CSV file with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
    csv_filename_with_timestamp = f"coordinates_{timestamp}.csv"
    with open(csv_filename_with_timestamp, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Y', 'X'])  # Header row
        csvwriter.writerows(path)

else:
    print("Path not found.")