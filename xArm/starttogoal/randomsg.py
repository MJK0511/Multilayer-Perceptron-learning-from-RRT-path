import random
class Pose:
    def __init__(self, x, y, z, ox, oy, oz, ow):
        self.x = x
        self.y = y
        self.z = z
        self.ox = ox
        self.oy = oy
        self.oz = oz
        self.ow = ow

    def __str__(self):
        return f"Pose({self.x}, {self.y}, {self.z}, {self.ox}, {self.oy}, {self.oz}, {self.ow})"

class RandomCoordinatesGenerator:
    def __init__(self):
        self.s_x_range = [0.23858859849616207, 0.42161561386409746]
        self.s_y_range = [-0.07567521953277917, 0.1043463383418795]
        self.s_z_range = [0.003959400987122885, 0.1363533171784251]
        self.s_ox_range = [-0.9999999996470472, 0.9999999986023902]
        self.s_oy_range = [-7.45332503896528e-05, 5.117126820928209e-05]
        self.s_oz_range = [-9.967902634227358e-05, 6.646000930425715e-05]
        self.s_ow_range = [1.7814525185041995e-06, 6.82781290642536e-05]

        self.g_x_range = [-0.13503985056104637, 0.08296792787821027]
        self.g_y_range = [0.30938707192143766, 0.4991824927774853]
        self.g_z_range = [0.8769287119757332, 0.9952150342625153]
        self.g_ox_range = [-0.5166104801242961, -0.2974888406014125]
        self.g_oy_range = [-0.5020856914789885, -0.40115676850801835]
        self.g_oz_range = [-0.5820294437708076, -0.46204687007356215]
        self.g_ow_range = [0.49498036880538415, 0.6677746910335242]


    def generate_random_coordinates(self):
        start = Pose(
            random.uniform(self.s_x_range[0], self.s_x_range[1]),
            random.uniform(self.s_y_range[0], self.s_y_range[1]),
            random.uniform(self.s_z_range[0], self.s_z_range[1]),
            random.uniform(self.s_ox_range[0], self.s_ox_range[1]),
            random.uniform(self.s_oy_range[0], self.s_oy_range[1]),
            random.uniform(self.s_oz_range[0], self.s_oz_range[1]),
            random.uniform(self.s_ow_range[0], self.s_ow_range[1])
        )
    
        goal = Pose(
            random.uniform(self.g_x_range[0], self.g_x_range[1]),
            random.uniform(self.g_y_range[0], self.g_y_range[1]),
            random.uniform(self.g_z_range[0], self.g_z_range[1]),
            random.uniform(self.g_ox_range[0], self.g_ox_range[1]),
            random.uniform(self.g_oy_range[0], self.g_oy_range[1]),
            random.uniform(self.g_oz_range[0], self.g_oz_range[1]),
            random.uniform(self.g_ow_range[0], self.g_ow_range[1])
        )

        return start, goal

if __name__ == "__main__":
#     # 주어진 범위
#     # 객체 생성
    generator = RandomCoordinatesGenerator()

    # 랜덤 좌표 생성
    start, goal = generator.generate_random_coordinates()

    # 출력
    print("start:", start)
    print("goal:", goal)
