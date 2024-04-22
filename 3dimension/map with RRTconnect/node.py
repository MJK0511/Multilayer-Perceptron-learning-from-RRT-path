class Node:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z  # Added z parameter
        self.parent = None
        self.children = []
