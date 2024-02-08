import os

class Range_sg:
    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as file:
            data = [list(map(float, line.strip('[]\n').replace('e-06', 'e-6').split(','))) for line in file]
        return data

    @staticmethod
    def find_min_max(data):
        x_values = [coord[0] for coord in data]
        y_values = [coord[1] for coord in data]
        z_values = [coord[2] for coord in data]
        ox_values = [coord[3] for coord in data]
        oy_values = [coord[4] for coord in data]
        oz_values = [coord[5] for coord in data]
        ow_values = [coord[6] for coord in data]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)
        min_z = min(z_values)
        max_z = max(z_values)

        min_ox = min(ox_values)
        max_ox = max(ox_values)
        min_oy = min(oy_values)
        max_oy = max(oy_values)
        min_oz = min(oz_values)
        max_oz = max(oz_values)
        min_ow = min(ow_values)
        max_ow = max(ow_values)

        return min_x, max_x, min_y, max_y, min_z, max_z, min_ox, max_ox, min_oy, max_oy, min_oz, max_oz, min_ow, max_ow

    @classmethod
    def range_sg(cls, default_folder):
        start_file_path = os.path.join(default_folder, 'sg/start_visual.txt')
        goal_file_path = os.path.join(default_folder, 'sg/goal_visual.txt')

        # Read start_visual.txt and goal_visual.txt
        start_data = cls.read_file(start_file_path)
        goal_data = cls.read_file(goal_file_path)

        # Find min and max values for start and goal separately
        (start_min_x, start_max_x, start_min_y, start_max_y, start_min_z, start_max_z,
         start_min_ox, start_max_ox, start_min_oy, start_max_oy,
         start_min_oz, start_max_oz, start_min_ow, start_max_ow) = cls.find_min_max(start_data)

        (goal_min_x, goal_max_x, goal_min_y, goal_max_y, goal_min_z, goal_max_z,
         goal_min_ox, goal_max_ox, goal_min_oy, goal_max_oy,
         goal_min_oz, goal_max_oz, goal_min_ow, goal_max_ow) = cls.find_min_max(goal_data)

        # Store results for start and goal
        cls.s_x_range = [start_min_x, start_max_x]
        cls.s_y_range = [start_min_y, start_max_y]
        cls.s_z_range = [start_min_z, start_max_z]
        cls.s_ox_range = [start_min_ox, start_max_ox]
        cls.s_oy_range = [start_min_oy, start_max_oy]
        cls.s_oz_range = [start_min_oz, start_max_oz]
        cls.s_ow_range = [start_min_ow, start_max_ow]

        cls.g_x_range = [goal_min_x, goal_max_x]
        cls.g_y_range = [goal_min_y, goal_max_y]
        cls.g_z_range = [goal_min_z, goal_max_z]
        cls.g_ox_range = [goal_min_ox, goal_max_ox]
        cls.g_oy_range = [goal_min_oy, goal_max_oy]
        cls.g_oz_range = [goal_min_oz, goal_max_oz]
        cls.g_ow_range = [goal_min_ow, goal_max_ow]

        # Print results in the desired format
        print(f"self.s_x_range = [{cls.s_x_range[0]}, {cls.s_x_range[1]}]")
        print(f"self.s_y_range = [{cls.s_y_range[0]}, {cls.s_y_range[1]}]")
        print(f"self.s_z_range = [{cls.s_z_range[0]}, {cls.s_z_range[1]}]")
        print(f"self.s_ox_range = [{cls.s_ox_range[0]}, {cls.s_ox_range[1]}]")
        print(f"self.s_oy_range = [{cls.s_oy_range[0]}, {cls.s_oy_range[1]}]")
        print(f"self.s_oz_range = [{cls.s_oz_range[0]}, {cls.s_oz_range[1]}]")
        print(f"self.s_ow_range = [{cls.s_ow_range[0]}, {cls.s_ow_range[1]}]")

        print(f"self.g_x_range = [{cls.g_x_range[0]}, {cls.g_x_range[1]}]")
        print(f"self.g_y_range = [{cls.g_y_range[0]}, {cls.g_y_range[1]}]")
        print(f"self.g_z_range = [{cls.g_z_range[0]}, {cls.g_z_range[1]}]")
        print(f"self.g_ox_range = [{cls.g_ox_range[0]}, {cls.g_ox_range[1]}]")
        print(f"self.g_oy_range = [{cls.g_oy_range[0]}, {cls.g_oy_range[1]}]")
        print(f"self.g_oz_range = [{cls.g_oz_range[0]}, {cls.g_oz_range[1]}]")
        print(f"self.g_ow_range = [{cls.g_ow_range[0]}, {cls.g_ow_range[1]}]")

# Example usage:
default_folder = '/home/nishidalab07/github/6dimension/simulation2'
Range_sg.range_sg(default_folder)


    