class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
    
    def __str__(self):
        return f"Node: ({self.x}, {self.y})"