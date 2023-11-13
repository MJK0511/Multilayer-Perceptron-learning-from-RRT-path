import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import time

###########################################
## node = 5 
## map px 

## RRT Algorithm
class Node:
    def __init__(self, x, y, root=None):
        self.root = root
        self.x = x
        self.y = y
        self.parent = None

    def __str__(self):
        return f"Node({self.x}, {self.y})"
    
    def distance_between(self, other_node):
        return np.linalg.norm([self.x - other_node.x, self.y - other_node.y])

class RRT:
    def __init__(self, map_width, map_height):
        # generate empty map
        self.map_width = map_width
        self.map_height = map_height
        self.map = np.zeros((map_width, map_height))
        self.tree = []
        self.root = Node(0, 0)

        # define obstacles point&size (x, y, width, height)
        obstacle_rect1 = (15, 20, 30, 20)  #left, up
        obstacle_rect2 = (70, 40, 20, 30)  #rigth, down
        obstacle_rect3 = (20, 70, 30, 20)  #left, down

        # draw obstacles # map[y,x]
        self.map[obstacle_rect1[1]:obstacle_rect1[1] + obstacle_rect1[3], obstacle_rect1[0]:obstacle_rect1[0] + obstacle_rect1[2]] = 1
        self.map[obstacle_rect2[1]:obstacle_rect2[1] + obstacle_rect2[3], obstacle_rect2[0]:obstacle_rect2[0] + obstacle_rect2[2]] = 1
        self.map[obstacle_rect3[1]:obstacle_rect3[1] + obstacle_rect3[3], obstacle_rect3[0]:obstacle_rect3[0] + obstacle_rect3[2]] = 1

        # Visualizing map
        # plt.imshow(map, cmap='Greys', extent=[0, map_width, 0, map_height])
        # plt.colorbar()
        # plt.grid()
        # plt.title("Map with Obstacles")
        # plt.show()
        
    def generate_random_node(self):
        rand_x = np.random.randint(0, self.map_width)
        rand_y = np.random.randint(0, self.map_height)
        return Node(rand_x, rand_y)
    
    def is_collision_free(self, node):
        if node.x < 0 or node.x >= self.map_width or node.y < 0 or node.y >= self.map_height or self.map[node.y, node.x] == 1:
            return False
        return True
    
    def find_nearest(self, target):
        nearest = self.root
        min_distance = nearest.distance_between(target)
        for node in nearest.connected_nodes():
            sub_tree = self(node)
            candidate = sub_tree.find_nearest(target)
            distance = candidate.distance_between(target)
            if distance < min_distance:
                nearest = candidate
                min_distance = distance
        return nearest
        

    def extend_tree(self, max_dist=0.1):
        random_node = self.generate_random_node()
        
        #現在のツリーからrandom_nodeに一番近いノードを探す
        nearest_node = min(self.tree, key=lambda node: np.linalg.norm([node.x - random_node.x, node.y - random_node.y]))

        #nearest_nodeとrandom_nodeの距離
        distance = np.linalg.norm([nearest_node.x - random_node.x, nearest_node.y - random_node.y])
        
        #距離が最大値より大きいと、random_node方向にmax_distだけ拡張した新しいノードを生成
        #そうでなければ、random_nodeを new_nodeに入れる
        if distance > max_dist:
            angle = np.arctan2(random_node.y - nearest_node.y, random_node.x - nearest_node.x)
            new_x = nearest_node.x + max_dist * np.cos(angle)
            new_y = nearest_node.y + max_dist * np.sin(angle)
            new_node = Node(int(round(new_x)), int(round(new_y)))
        else:
            new_node = random_node

        #新しいノードが衝突するか確認
        if self.is_collision_free(new_node) == True : # 衝突しないと
            new_node.parent = nearest_node
            self.tree.append(new_node) #ノードをツリーに追加            
            

    def rrt_path_planning(self, start, goal, max_iterations=1000):
        self.tree = [start] #初期ツリーはスタート点
        for _ in range(max_iterations):
            goal_node = goal
            next_node = self.generate_random_node()
            #print(f"{goal_node}")

            if self.is_collision_free(next_node):
                if next_node not in self.tree:
                    self.tree.append(next_node)

                    # 現在のツリーから目標に一番近いノードを探す
                    nearest_to_goal = self.find_nearest(goal_node)
                    #print(f"{nearest_to_goal}")
                    #探したノードが目標地点と一定距離以内であれば、最終的経路を生成しリターンする
                    if np.linalg.norm([nearest_to_goal.x - goal.x, nearest_to_goal.y - goal.y]) < 0.1:
                        path = self.construct_path(nearest_to_goal)
                        print(f"{path}")
                        return path
                
                    self.extend_tree(max_dist=0.1)
            
        return None

    def construct_path(self, node):
        path = [(node.x, node.y)]
        while node.parent is not None:
            node = node.parent
            path.insert(0, (node.x, node.y))
        return path

# Visualization
def visualize_map(rrt_instance, path=None):
    plt.figure(2)
    plt.imshow(rrt_instance.map, cmap='gray', extent=[0, 100, 0, 100])
    plt.colorbar()
    if path:
        path = np.array(path)
        plt.plot(path[:, 0], path[:, 1], 'r-')
    #save_path_to_csv(map, path)  # save CSV&Image
    plt.show()

# save to csv
def save_path_to_csv(map, path, folder_path='/home/nishidalab07/rrtpath'):
    timestamp = int(time.time())  # timestamp
    filename = f'{folder_path}/path_{timestamp}.csv'

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])  # add header
        writer.writerows(path)

    # save map image
    map_filename = f'{folder_path}/map_{timestamp}.png'
    plt.figure(figsize=(6, 6))
    plt.imshow(map, cmap='gray', extent=[0, 100, 0, 100])
    plt.colorbar()
    if path.any(): 
        path = np.array(path)
        plt.plot(path[:, 0], path[:, 1], 'r-')
    plt.title("Map with Path")
    plt.savefig(map_filename)
    plt.close()


# Example Usage:
map_width = 100
map_height = 100
start_node = Node(1, 99)
goal_node = Node(99, 1)

rrt_planner = RRT(map_width, map_height)
path = rrt_planner.rrt_path_planning(start_node, goal_node)
print(path)
visualize_map(rrt_planner, path)
