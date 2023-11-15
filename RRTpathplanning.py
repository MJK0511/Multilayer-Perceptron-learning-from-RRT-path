import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, y, x):
        self.x = x
        self.y = y
        self.parent = None

class RRT:
    def __init__(self, map_width, map_height, start):
        #空きマップを生成
        self.map_width = map_width
        self.map_height = map_height
        self.map = np.zeros((map_width, map_height))
        self.tree = []
        self.root = Node(start[1], start[0])
        self.tree.append(self.root)

        #障害物の座標
        obstacle_rect1 = (15, 20, 30, 20) #left, up         (x,y) = (15:45, 20:40)
        obstacle_rect2 = (70, 40, 20, 30) #right            (x,y) = (70:90, 40:90)
        obstacle_rect3 = (20, 70, 30, 20) #left, down       (x,y) = (20:50, 70:90)
        #障害物生成
        self.map[obstacle_rect1[1]:obstacle_rect1[1] + obstacle_rect1[3], obstacle_rect1[0]:obstacle_rect1[0] + obstacle_rect1[2]] = 1
        self.map[obstacle_rect2[1]:obstacle_rect2[1] + obstacle_rect2[3], obstacle_rect2[0]:obstacle_rect2[0] + obstacle_rect2[2]] = 1
        self.map[obstacle_rect3[1]:obstacle_rect3[1] + obstacle_rect3[3], obstacle_rect3[0]:obstacle_rect3[0] + obstacle_rect3[2]] = 1

    #ノードを追加する関数
    def add_node(self, y, x, parent):
        node = Node(y, x)
        node.parent = parent
        self.tree.append(node)
        return node

    #衝突を確認する
    def is_collision_free(self, y, x):
        if x < 0 or x >= self.map_width or y < 0 or y >= self.map_height:
            return False
        if self.map[y, x] == 1.0:
            return False
        return True

    #ランダムに座標を生成
    def generate_random_point(self):
        max_attempts = 1000  # Set a limit on the number of attempts to avoid infinite loop
        for _ in range(max_attempts):
            x = np.random.randint(0, self.map_width)
            y = np.random.randint(0, self.map_height)

            # ランダム座標が障害物と衝突するか確認
            if self.is_collision_free(y, x):
                return y, x

    # If no collision-free point is found after the maximum attempts, return None
        return None

    #一番近いノードを探す
    def find_nearest_node(self, y, x):
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
            y_rand, x_rand = self.generate_random_point()
            #最も近いノードを見つける
            nearest_node = self.find_nearest_node(y_rand, x_rand)
            
            #ノードを拡張して新しいノードを生成:step_size 分だけ移動する
            x_new = int(round(nearest_node.x + step_size * np.cos(np.arctan2(y_rand - nearest_node.y, x_rand - nearest_node.x))))
            y_new = int(round(nearest_node.y + step_size * np.sin(np.arctan2(y_rand - nearest_node.y, x_rand - nearest_node.x))))
        
            #生成した新しいノードが障害物と衝突していない場合、ツリーに追加
            if not self.is_collision_free((y_new), (x_new)):
                continue

            new_node = self.add_node(y_new, x_new, nearest_node)
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

rrt = RRT(map_width, map_height, start)

path = rrt.plan_path(goal)

if path:
    print("Path : [y,x]")
    print(path)

    # Visualizing map and path
    plt.imshow(rrt.map, cmap='Greys', extent=[0, map_width, map_height, 0])
    plt.plot([node[1] for node in path], [node[0] for node in path], color='red', linewidth=2)
    plt.scatter([node[1] for node in path], [node[0] for node in path], color='yellow', marker='o', label='Path Points')  # 경로 좌표를 노란 점으로 표시
    plt.scatter(start[1], start[0], color='green', marker='o', label='Start')
    plt.scatter(goal[1], goal[0], color='blue', marker='o', label='Goal')
    plt.legend()
    plt.title("RRT Path Planning")
    plt.show()
else:
    print("Path not found.")
