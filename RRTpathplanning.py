import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

class RRT:
    def __init__(self, map_width, map_height, start):
        self.map_width = map_width
        self.map_height = map_height
        self.map = np.zeros((map_width, map_height))
        self.tree = []
        self.root = Node(start[0], start[1])
        self.tree.append(self.root)

        obstacle_rect1 = (15, 20, 30, 20)
        obstacle_rect2 = (70, 40, 20, 30)
        obstacle_rect3 = (20, 70, 30, 20)

        self.map[obstacle_rect1[1]:obstacle_rect1[1] + obstacle_rect1[3], obstacle_rect1[0]:obstacle_rect1[0] + obstacle_rect1[2]] = 1
        self.map[obstacle_rect2[1]:obstacle_rect2[1] + obstacle_rect2[3], obstacle_rect2[0]:obstacle_rect2[0] + obstacle_rect2[2]] = 1
        self.map[obstacle_rect3[1]:obstacle_rect3[1] + obstacle_rect3[3], obstacle_rect3[0]:obstacle_rect3[0] + obstacle_rect3[2]] = 1

    def add_node(self, x, y, parent):
        node = Node(x, y)
        node.parent = parent
        self.tree.append(node)
        return node

    def is_collision_free(self, x, y):
        if x < 0 or x >= self.map_width or y < 0 or y >= self.map_height:
            return False
        if self.map[int(round(y)), int(round(x))] == 1:
            return False
        return True

    def generate_random_point(self):
        x = np.random.randint(0, self.map_width)
        y = np.random.randint(0, self.map_height)
        return x, y

    def find_nearest_node(self, x, y):
        distances = [np.sqrt((node.x - x)**2 + (node.y - y)**2) for node in self.tree]
        min_index = np.argmin(distances)
        return self.tree[min_index]

    def plan_path(self, start, goal, max_iter=1000, step_size=5):
        for _ in range(max_iter):
            x_rand, y_rand = self.generate_random_point()
            nearest_node = self.find_nearest_node(x_rand, y_rand)

            x_new = nearest_node.x + step_size * np.cos(np.arctan2(y_rand - nearest_node.y, x_rand - nearest_node.x))
            y_new = nearest_node.y + step_size * np.sin(np.arctan2(y_rand - nearest_node.y, x_rand - nearest_node.x))

            if not self.is_collision_free(int(x_new), int(y_new)):
                continue

            new_node = self.add_node(int(x_new), int(y_new), nearest_node)

            if np.sqrt((new_node.x - goal[0])**2 + (new_node.y - goal[1])**2) < step_size:
                goal_node = self.add_node(goal[0], goal[1], new_node)
                return self.extract_path(goal_node)

        return None

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
