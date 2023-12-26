import numpy as np
from node import Node


class RRT:
    def __init__(self, world_map, start):
        self.tree = []
        self.map = world_map.map
        self.obstacle_rect1 = world_map.obstacle_rect1
        self.map_width = world_map.map_width
        self.map_height = world_map.map_height
        self.map_depth = world_map.map_depth  # Added map_depth
        self.root = Node(start[0], start[1], start[2])  # Added start[2]
        self.tree.append(self.root)


    def add_node(self, x, y, z, parent):  # Added z parameter
        node = Node(x, y, z)
        node.parent = parent
        parent.children.append(node)
        self.tree.append(node)
        return node

    def is_collision_free(self, x, y, z):  # Added z parameter
        if x < 0 or x >= self.map_width or y < 0 or y >= self.map_height or z < 0 or z >= self.map_depth:
            return False
        if self.map[x, y, z] == 1.0:
            return False
        return True

    def calculate_line_equation(self, parent_node, new_node):
        # 3차원 직선 방정식 계산
        x1, y1, z1 = parent_node.x, parent_node.y, parent_node.z
        x2, y2, z2 = new_node.x, new_node.y, new_node.z

        if x2 - x1 != 0:
            slope_x = (y2 - y1) / (x2 - x1)
            slope_y = (z2 - z1) / (x2 - x1)
            slope_z = (y2 - y1) / (x2 - x1) 

            intercept_x = y1 - slope_x * x1
            intercept_y = z1 - slope_y * x1
            intercept_z = y1 - slope_z * x1

            return slope_x, slope_y, slope_z, intercept_x, intercept_y, intercept_z
        else:
            # 직선이 x 축과 평행한 경우
            slope_x = float('inf')
            slope_y = 0 if y2 > y1 else float('-inf')
            slope_z = 0 if z2 > z1 else float('-inf')

            intercept_x = float('inf') if y2 > y1 else float('-inf')
            intercept_y = z1
            intercept_z = y1 if z2 > z1 else float('-inf')

            return slope_x, slope_y, slope_z, intercept_x, intercept_y, intercept_z

        

    def is_collision_free_rectangle(self, parent_node, new_node, obstacle_rect):
        x1, y1, z1 = obstacle_rect[0], obstacle_rect[2], obstacle_rect[4]
        x2, y2, z2 = obstacle_rect[1], obstacle_rect[3], obstacle_rect[5]

        # ラインセグメントが長方形の辺と交差するか確認
        if self.do_line_segments_intersect(x1, y1, z1, x2, y2, z2, parent_node.x, parent_node.y, parent_node.z, new_node.x, new_node.y, new_node.z):
            return False
        
        if self.do_line_segments_intersect(x1, y1, z1, x2, y2, z1, parent_node.x, parent_node.y, parent_node.z, new_node.x, new_node.y, new_node.z):
            return False

        if self.do_line_segments_intersect(x1, y1, z1, x2, y1, z1, parent_node.x, parent_node.y, parent_node.z, new_node.x, new_node.y, new_node.z):
            return False
        
        if self.do_line_segments_intersect(x2, y2, z2, x1, y1, z1, parent_node.x, parent_node.y, parent_node.z, new_node.x, new_node.y, new_node.z):
            return False


        
        if self.do_line_segments_intersect(x1, y2, x2, y2, parent_node.x, parent_node.y, parent_node.z, new_node.x, new_node.y, new_node.z):
            return False

        if self.do_line_segments_intersect(x2, y2, x2, y1, parent_node.x, parent_node.y, parent_node.z, new_node.x, new_node.y, new_node.z):
            return False

        if self.do_line_segments_intersect(x2, y1, x1, y1, parent_node.x, parent_node.y, parent_node.z, new_node.x, new_node.y, new_node.z):
            return False

        return True

    def do_line_segments_intersect(self, x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4):
        # 세 점이 일직선 상에 있는지 확인
        def orientation(x1, y1, z1, x2, y2, z2, x3, y3, z3):
            val = (y2 - y1) * ((z3 - z2) * (x3 - x2) - (x3 - x2) * (z3 - z2)) - (z2 - z1) * ((x3 - x2) * (y3 - y2) - (y3 - y2) * (x3 - x2)) + (x2 - x1) * ((y3 - y2) * (z3 - z2) - (z3 - z2) * (y3 - y2))

            if val == 0:
                return 0  # 세 점이 일직선 상에 있음
            return 1 if val > 0 else -1  # 시계 방향 또는 반시계 방향

        o1 = orientation(x1, y1, z1, x2, y2, z2, x3, y3, z3)
        o2 = orientation(x1, y1, z1, x2, y2, z2, x4, y4, z4)
        o3 = orientation(x3, y3, z3, x4, y4, z4, x1, y1, z1)
        o4 = orientation(x3, y3, z3, x4, y4, z4, x2, y2, z2)

        # 일반적인 경우
        if o1 != o2 and o3 != o4:
            return True

        # 특수한 경우
        if o1 == 0 and self.on_line_segment(x1, y1, x2, y2, x3, y3, z1, z2, z3, z4):
            return True
        if o2 == 0 and self.on_line_segment(x1, y1, x2, y2, x4, y4, z1, z2, z3, z4):
            return True
        if o3 == 0 and self.on_line_segment(x3, y3, x4, y4, x1, y1, z3, z4, z1, z2):
            return True
        if o4 == 0 and self.on_line_segment(x3, y3, x4, y4, x2, y2, z3, z4, z1, z2):
            return True

        return False


    def on_line_segment(self, x1, y1, z1, x2, y2, z2, x, y, z):
        # 点 (x, y) が線分 (x1, y1) から (x2, y2) に存在するか確認
        return (x <= max(x1, x2) and x >= min(x1, x2) and
                y <= max(y1, y2) and y >= min(y1, y2) and
                z <= max(z1, z2) and z >= min(z1, z2))
    
    def generate_random_point(self):
        max_attempts = 1000
        for _ in range(max_attempts):
            x = np.random.randint(0, self.map_width)
            y = np.random.randint(0, self.map_height)
            z = np.random.randint(0, self.map_depth)
            if self.is_collision_free(x, y, z):
                return x, y, z
        return None

    
    #一番近いノードを探す
    def find_nearest_node(self, x, y, z):
        #距離計算
        distances = [np.sqrt((node.x - x)**2 + (node.y - y)**2 + (node.z - z)**2) for node in self.tree]
        #最小距離のノードを探す
        min_indices = np.where(distances == np.min(distances))[0]
        #最小距離のノードの中でランダムに選択
        min_index = np.random.choice(min_indices)
        return self.tree[min_index]

    #パス生成
    #step_sizeでwaypointの数を調整できる
    def plan_path(self, goal, max_iter=10000, step_size=16):
        for _ in range(max_iter):
            #ランダムな点を生成
            x_rand, y_rand, z_rand = self.generate_random_point()
            #最も近いノードを見つける
            n = self.find_nearest_node(x_rand, y_rand, z_rand) # n : nearest_node
            
            #ノードを拡張して新しいノードを生成:step_size 分だけ移動する
            theta = np.arctan2(y_rand - n.y, x_rand - n.x)
            phi = np.arctan2(z_rand - n.z, np.sqrt((x_rand - n.x)**2 + (y_rand - n.y)**2))
            x_new = int(round(n.x + step_size * np.cos(theta)))
            y_new = int(round(n.y + step_size * np.sin(theta)))
            z_new = int(round(n.z + step_size * np.tan(phi)))  # phi는 각도로 설정

            #生成した新しいノードが障害物と衝突していない場合、ツリーに追加
            if not self.is_collision_free((x_new), (y_new), (z_new)):
                continue

            new_node = Node(x_new, y_new, z_new)

            # 正方形との衝突を確認
            if not self.is_collision_free_rectangle(n, new_node, self.obstacle_rect1):
                continue

            new_node = self.add_node(x_new, y_new, z_new, n)

            #新しいノードが目標に十分に近い場合、目標ノードをツリーに追加し、計画されたパスを返す
            if np.sqrt((new_node.x - goal[0])**2 + (new_node.y - goal[1])**2 + (new_node.z - goal[2])**2) < step_size:
                goal_node = self.add_node(goal[0], goal[1], goal[2], new_node)
                return self.extract_path(goal_node)
        return None

    #パスを抽出
    def extract_path(self, goal_node):
        path = []
        current_node = goal_node
        while current_node is not None:
            path.append((current_node.x, current_node.y, current_node.z))
            current_node = current_node.parent
        return path[::-1]
    
