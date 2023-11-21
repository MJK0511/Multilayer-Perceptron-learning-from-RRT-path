import numpy as np
import datetime
import csv
import os
from WorldMap import WorldMap
from Node import Node
from ImageMap import ImageMap


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

    # CSVファイルを保存
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
    csv_filename_with_timestamp = f"coordinates_{timestamp}.csv"

    # ファイルをセーブするパスを設定
    save_directory = r"C:\MJ\github\path"

    # ディレクトリーのパス生成
    full_path = os.path.join(save_directory, csv_filename_with_timestamp)

    with open(csv_filename_with_timestamp, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Y', 'X'])
        csvwriter.writerows(path)

else:
    print("Path not found.")