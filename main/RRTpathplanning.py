import numpy as np
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
        parent.children.append(node)
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
            slope = float('inf')
            intercept = float('inf') if y2 > y1 else float('-inf')
            return slope, intercept
        

    def is_collision_free_rectangle(self, parent_node, new_node, obstacle_rect):
        x1, y1, x2, y2 = obstacle_rect[0], obstacle_rect[2], obstacle_rect[1], obstacle_rect[3]

        # ラインセグメントが長方形の辺と交差するか確認
        if self.do_line_segments_intersect(x1, y1, x2, y2, parent_node.x, parent_node.y, new_node.x, new_node.y):
            return False

        if self.do_line_segments_intersect(x2, y2, x1, y1, parent_node.x, parent_node.y, new_node.x, new_node.y):
            return False

        if self.do_line_segments_intersect(x1, y1, x1, y2, parent_node.x, parent_node.y, new_node.x, new_node.y):
            return False

        if self.do_line_segments_intersect(x1, y2, x2, y2, parent_node.x, parent_node.y, new_node.x, new_node.y):
            return False

        if self.do_line_segments_intersect(x2, y2, x2, y1, parent_node.x, parent_node.y, new_node.x, new_node.y):
            return False

        if self.do_line_segments_intersect(x2, y1, x1, y1, parent_node.x, parent_node.y, new_node.x, new_node.y):
            return False

        return True

    def do_line_segments_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # 二つの線分が交差しているか確認
        def orientation(x1, y1, x2, y2, x3, y3):
            val = (y2 - y1) * (x3 - x2) - (x2 - x1) * (y3 - y2)
            if val == 0:
                return 0  # 同一線上
            return 1 if val > 0 else 2  # 時計回りまたは反時計回り

        o1 = orientation(x1, y1, x2, y2, x3, y3)
        o2 = orientation(x1, y1, x2, y2, x4, y4)
        o3 = orientation(x3, y3, x4, y4, x1, y1)
        o4 = orientation(x3, y3, x4, y4, x2, y2)

        # 一般的ケース
        if o1 != o2 and o3 != o4:
            return True

        # 特殊ケース
        if o1 == 0 and self.on_line_segment(x1, y1, x2, y2, x3, y3):
            return True
        if o2 == 0 and self.on_line_segment(x1, y1, x2, y2, x4, y4):
            return True
        if o3 == 0 and self.on_line_segment(x3, y3, x4, y4, x1, y1):
            return True
        if o4 == 0 and self.on_line_segment(x3, y3, x4, y4, x2, y2):
            return True

        return False

    def on_line_segment(self, x1, y1, x2, y2, x, y):
        # 点 (x, y) が線分 (x1, y1) から (x2, y2) に存在するか確認
        return (x <= max(x1, x2) and x >= min(x1, x2) and
                y <= max(y1, y2) and y >= min(y1, y2))



    #ランダムに座標を生成
    def generate_random_point(self):
        max_attempts = 1000  # 無限ループを避けるための試行回数の上限を設定
        for _ in range(max_attempts):
            x = np.random.randint(0, self.map_width)
            y = np.random.randint(0, self.map_height)

            # ランダム座標が障害物と衝突するか確認
            if self.is_collision_free(x, y):
                return x, y

    # 最大試行回数後に衝突のない点が見つからない場合は、Noneを返す
        return None

    #一番近いノードを探す
    def find_nearest_node(self, x, y):
        #距離計算
        distances = [np.sqrt((node.x - x)**2 + (node.y - y)**2) for node in self.tree]
        #最小距離のノードを探す
        min_indices = np.where(distances == np.min(distances))[0]
        #最小距離のノードの中でランダムに選択
        min_index = np.random.choice(min_indices)
        return self.tree[min_index]

    #パス生成
    #step_sizeでwaypointの数を調整できる
    def plan_path(self, goal, waypoint_count, max_iter=10000, step_size=25, ):
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
                return self.extract_path(goal_node, waypoint_count)
            
            if len(n.children) >= waypoint_count:
                return self.extract_path(n, waypoint_count)
    

        return None

    #パスを抽出
    def extract_path(self, goal_node, waypoint_count):
        path = []
        current_node = goal_node
        waypoints_added = 0

        while current_node is not None and waypoints_added < waypoint_count:
            path.append((current_node.y, current_node.x))
            current_node = current_node.parent
            waypoints_added += 1

        return path[::-1]
    