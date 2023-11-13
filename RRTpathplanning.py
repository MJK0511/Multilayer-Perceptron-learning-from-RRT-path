import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, x, y):
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
        self.root = Node(start[0], start[1])
        self.tree.append(self.root)

        #障害物の座標
        obstacle_rect1 = (15, 20, 30, 20)
        obstacle_rect2 = (70, 40, 20, 30)
        obstacle_rect3 = (20, 70, 30, 20)
        #障害物生成
        self.map[obstacle_rect1[1]:obstacle_rect1[1] + obstacle_rect1[3], obstacle_rect1[0]:obstacle_rect1[0] + obstacle_rect1[2]] = 1
        self.map[obstacle_rect2[1]:obstacle_rect2[1] + obstacle_rect2[3], obstacle_rect2[0]:obstacle_rect2[0] + obstacle_rect2[2]] = 1
        self.map[obstacle_rect3[1]:obstacle_rect3[1] + obstacle_rect3[3], obstacle_rect3[0]:obstacle_rect3[0] + obstacle_rect3[2]] = 1

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
        if self.map[int(round(y)), int(round(x))] == 1:
            return False
        return True

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
    def plan_path(self, start, goal, max_iter=1000, step_size=20):
        for _ in range(max_iter):
            #ランダムな点 (x_rand, y_rand) を生成
            x_rand, y_rand = self.generate_random_point()
            #最も近いノードを見つける
            nearest_node = self.find_nearest_node(x_rand, y_rand)

            #ノードを拡張して新しいノードを生成:step_size 分だけ移動する
            x_new = nearest_node.x + step_size * np.cos(np.arctan2(y_rand - nearest_node.y, x_rand - nearest_node.x))
            y_new = nearest_node.y + step_size * np.sin(np.arctan2(y_rand - nearest_node.y, x_rand - nearest_node.x))

            #生成した新しいノードが障害物と衝突していない場合、ツリーに追加
            if not self.is_collision_free(int(x_new), int(y_new)):
                continue

            new_node = self.add_node(int(x_new), int(y_new), nearest_node)
            
            #新しいノードが目標に十分に近い場合、目標ノードをツリーに追加し、計画されたパスを返す
            if np.sqrt((new_node.x - goal[0])**2 + (new_node.y - goal[1])**2) < step_size:
                goal_node = self.add_node(goal[0], goal[1], new_node)
                return self.extract_path(goal_node)

        return None

    #パスを抽出
    def extract_path(self, goal_node):
        path = []
        current_node = goal_node
        while current_node is not None:
            path.append((current_node.x, current_node.y))
            current_node = current_node.parent
        return path[::-1]

# Example usage:
map_width = 100
map_height = 100
start = (1, 99)
goal = (99, 1)

rrt = RRT(map_width, map_height, start)

path = rrt.plan_path(start, goal)

if path:
    print("Path found!")
    print(path)

    # Visualizing map and path
    plt.imshow(rrt.map, cmap='Greys', extent=[0, map_width, 0, map_height])
    plt.plot([node[0] for node in path], [node[1] for node in path], color='red', linewidth=2)
    plt.scatter(start[0], start[1], color='green', marker='o', label='Start')
    plt.scatter(goal[0], goal[1], color='blue', marker='o', label='Goal')
    plt.legend()
    plt.title("RRT Path Planning")
    plt.show()
else:
    print("Path not found.")
